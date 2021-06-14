import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name()
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price',
           type=float,
           required=True,
           help='This field is required'
        )
        request_data = parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, request_data['price'])
        if not item:
            try:
                item = ItemModel(name, request_data['price'])
            except:
                return {"message": "An error occured inserting the item {test}"}, 500
        else:
            try:
                item.price = request_data['price']
            except:
                return {"message": "An error occurred updated the item"}, 500
        item.save_to_db()
        return updated_item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
