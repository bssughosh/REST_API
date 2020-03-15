from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name': 'My Store',
        'items': [
            {
                'name': 'My Item',
                'price': 15.99
            }
        ]
    }
]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data["name"],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


@app.route('/store/<string:name>')
def get_store(name):
    for i in stores:
        if name == i['name']:
            return jsonify(i)
    return jsonify({'message': 'store not found'})


@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


@app.route('/store/<string:name>/item', methods=['POST'])
def create_item(name):
    request_data = request.get_json()
    for i in stores:
        if i['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            i['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store not found'})


@app.route('/store/<string:name>/item')
def get_item(name):
    for i in stores:
        if name == i['name']:
            return jsonify({'items': i['items']})
    return jsonify({'message': 'store not found'})


app.run(port=4999)
