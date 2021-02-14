from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # Tell SqlAlchemy the db will run locally with app
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Create an encrypt a key
app.secret_key = 'jose'
api = Api(app)

# Create the DB with a Flask decorator <-- moved to run.py

jwt = JWT(app, authenticate, identity)  # /auth --> Authenticate the JWT token i.e. POST http://http:127.0.0.1/auth
# with body request with username and password

api.add_resource(Store, '/store/<string:name>')  # http://127.0.0.1:5000/store/<name>
api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/item/<name>
api.add_resource(ItemList, '/items')  # http://127.0.0.1:5000/items
api.add_resource(StoreList, '/stores')  # http://127.0.0.1:5000/stores

api.add_resource(UserRegister, '/register')  # http://127.0.0.1:5000/register

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)  # debug=True allows you to get HTML page for troubleshooting
