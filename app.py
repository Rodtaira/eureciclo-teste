from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
# from .utils import readParseFile
import pymysql 
import csv
import os 

# Init App 
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.slite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db 
db = SQLAlchemy(app)

#Init ma 
ma = Marshmallow(app)

# Utils

def readParseFile(): 
    with open("dados.txt", "r") as f:
        csv_reader = csv.DictReader(f, delimiter='\t')
        for row in csv_reader:
            print(row)
        return csv_reader


# Model

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

#Create DATABASE
db.create_all()

@app.route('/product', methods=['POST'])
def add_product():

    csv_reader = readParseFile()
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