from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from bson import json_util, ObjectId
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

#mongo_uri = 'mongodb+srv://pixewin621:ovJNAOJLYEnk8SOE@cluster0.6qnu0z7.mongodb.net/?retryWrites=true&w=majority'   
mongo_uri = 'mongodb+srv://sora:Ue29WzfsCBJWXT7P@cluster0.6qnu0z7.mongodb.net/?retryWrites=true&w=majority' 
db_name = 'youkaicg'
collection_name = 'cards'

client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/products', methods=['GET'])
def get_products():
    collection = db['products']
    results = list(collection.find().limit(40))
    return json.loads(json_util.dumps(results))

@app.route('/api/banlist', methods=['GET'])
def get_banlist():
    results = list(collection.find({"banlist":{"$exists": True}},{"cardnumber": 1,"name":1,"banlist": 1,"_id": 0}))
    return json.loads(json_util.dumps(results))
    
@app.route('/api/erratas', methods=['GET'])
def get_erratas():
    results = list(collection.find({"errata": True},{"cardnumber": 1,"name":1,"_id": 0}))
    return json.loads(json_util.dumps(results))

@app.route('/api/alters', methods=['GET'])
def get_alters():
    results = list(collection.find({"alt_arts": {"$exists": True}}))
    return json.loads(json_util.dumps(results))

@app.route('/api/youkaicg/code/<code_part>', methods=['GET'])
def get_documents_by_code_part(code_part):
    try:
        query = {'cardnumber': {'$regex': f'.*{code_part}.*'}}
        results = list(collection.find(query))
        if results:
            return json.loads(json_util.dumps(results))
        else:
            return jsonify({'error': 'Nenhum documento encontrado'}), 404
    except errors.PyMongoError as e:
        return jsonify({'error': f'Erro de banco de dados: {str(e)}'}), 500

@app.route('/api/youkaicg/keyword/<key>', methods=['GET'])
def get_documents_by_keyword(key):
    try:
        query = {'keywords':key}
        results = list(collection.find(query))
        if results:
            return json.loads(json_util.dumps(results))
        else:
            return jsonify({'error': 'Nenhum documento encontrado'}), 404
    except errors.PyMongoError as e:
        return jsonify({'error': f'Erro de banco de dados: {str(e)}'}), 500

@app.route('/api/youkaicg/wizard', methods=['GET'])
def get_wizard_deck():
    color = request.args.get('color')
    key = request.args.get('key')
    try:
        query = {'color': color, 'keywords': key}
        results = list(collection.find(query))
        if results:
            return json.loads(json_util.dumps(results))
        else:
            return jsonify({'error': 'Nenhum documento encontrado'}), 404
    except errors.PyMongoError as e:
        return jsonify({'error': f'Erro de banco de dados: {str(e)}'}), 500

@app.route('/api/youkaicg/<cardnumber>', methods=['GET'])
def get_document_by_cardnumber(cardnumber):
    try:
        result = collection.find_one({'cardnumber': cardnumber})   
        if result:
            return json.loads(json_util.dumps(result))
        else:
            return jsonify({'error': 'Documento não encontrado'}), 404
    except errors.PyMongoError as e:
        return jsonify({'error': f'Erro de banco de dados: {str(e)}'}), 500

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, world!'})

@app.route('/api/greet', methods=['POST'])
def greet():
    data = request.get_json()

    if 'name' in data:
        return jsonify({'message': f'Hello, {data["name"]}!'})
    else:
        return jsonify({'error': 'Name not provided'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
