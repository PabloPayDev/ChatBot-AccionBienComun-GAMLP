from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['meta_db_100J']

def json_serializer(data):
    if isinstance(data, ObjectId):
        return str(data)
    if isinstance(data, list):
        return [json_serializer(item) for item in data]
    if isinstance(data, dict):
        return {key: json_serializer(value) for key, value in data.items()}
    return data

@app.route('/api/data', methods=['GET'])
def get_data():
    collection = db['data']
    data = list(collection.find({}))
    return jsonify(json_serializer(data))

@app.route('/api/data', methods=['POST'])
def add_data():
    new_data = request.json
    collection = db['data']
    collection.insert_one(new_data)
    return jsonify(json_serializer(new_data)), 201

if __name__ == '__main__':
    #app.run(debug=True)
    data = [
        ['Nombre', 'Edad', 'Ciudad'],
        ['Alice', 30, 'Nueva York'],
        ['Bob', 25, 'Los Ángeles'],
        ['Charlie', 35, 'Chicago']
    ]

    df = pd.DataFrame(data[1:], columns=data[0])
    df.to_excel('datos.xlsx', index=False)
