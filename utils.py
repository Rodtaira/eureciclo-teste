
def readParseFile(): 
    with open("dados.txt", "r") as f:
        csv_reader = csv.DictReader(f, delimiter='\t')
        return csv_reader
