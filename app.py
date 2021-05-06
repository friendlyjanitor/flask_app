from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = [
    {
        'name': 'Test Item',
        'price': .99
    }
]


class Item(Resource):
    def get(self, name):
        for item in items:
            if name == item['name']:
                return item
        return {'Item': None}, 404

    def post(self, name):
        request_data = request.get_json()
        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)