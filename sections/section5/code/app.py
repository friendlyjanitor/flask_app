from flask import Flask, jsonify, render_template
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from item import Item, ItemList
from datetime import timedelta

from user import UserRegister

app = Flask(__name__)
app.secret_key = 'ryan'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
api = Api(app)

jwt = JWT(app, authenticate, identity) #auth

items = []




api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)