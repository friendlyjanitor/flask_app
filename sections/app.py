from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'ryan'
api = Api(app)

jwt = JWT(app, authenticate, identity) #auth

items = []


class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'Item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        parser = reqparse.RequestParser()
        request_data = parser.parse_args()
        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price',
           type=float,
           required=True,
           help='This field is required'
        )
        request_data = parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if not item:
            item = {'name': name, 'price': request_data['price']}
            items.append(item)
        else:
            item.update(request_data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)