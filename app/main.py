from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow

import csv
import os 

# Init App 
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:example@db/databasetest"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.slite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db 
db = SQLAlchemy(app)

#Init ma 
ma = Marshmallow(app)

# Model

"""Modelo do dado"""

class Order(db.Model): 
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(25))
    description = db.Column(db.String(50))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    address = db.Column(db.String(50))
    supplier = db.Column(db.String(25))

    def __init__(self, name, description, price, qty, address, supplier): 
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty
        self.address = address
        self.supplier = supplier

# Schema 

class OrderSchema(ma.Schema): 
    class Meta: 
        fields = ('id', 'name', 'description', 'price', 'qty', 'address', 'supplier')

# Init Schema 

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# Create DATABASE

db.create_all()

# Utils

""" Função responsável por ler e parsear o arquivo """

def readParseFile(): 
    with open("dados.txt", "r") as f:
        csv_reader = csv.DictReader(f, delimiter='\t')
        for row in csv_reader:
         
            name = row["Comprador"]
            #print(name)
            description = row["Descrição"]
            #print(description)
            price = row["Preço Unitário"]
            #print(price)
            qty = row["Quantidade"]
            #print(qty)
            address = row["Endereço"]
            #print(address)
            supplier = row["Fornecedor"]
            #print(supplier)

            # Obs: Tentando persistir os dados lidos, entretanto não está funcionando         
            db_order = Order(name, description, price, qty, address, supplier)
            db.session.add(db_order)
            db.session.commit()

""" Rota para fazer a leitura do arquivo e persistir os dados lidos no arquivo no banco de dados """
@app.route('/ordersFile')
def insertFileDataToDatabase(): 
    readParseFile()
    orders = Order.query.all()
    return order_schema.jsonify(orders)

""" Rota para mostrar todos os dados do banco """
@app.route('/orders', methods=['GET'])
def get_products(): 
    orders = Order.query.all()
    return render_template("home.html", orders=orders)

""" Rota para testar se esta persistindo um valor que possui os mesmos campos dos dados a serem lidos no arquivo e se os mesmos estão sendo salvos de forma correta no banco """
@app.route('/addOrder', methods=['POST'])
def add_product():

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']  
    address = request.json['address']
    supplier = request.json['supplier']

    new_order = Order(name, description, price, qty, address, supplier)
    db.session.add(new_order)
    db.session.commit()

    return order_schema.jsonify(new_order)

# Run Server

if __name__ == '__main__': 
    app.run(debug=True)