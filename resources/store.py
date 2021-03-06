from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message':'Store Not Found'}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'message': "Store with name '{}' already exits"}.format(name), 400
        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        return {'Store': [store.json() for store in StoreModel.query.all()]}
