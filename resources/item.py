# import os
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel


# path = os.path.dirname(os.path.abspath(__file__))
# db_path = os.path.join(path, '..', 'data.db')  # Navigate one level up
# # db = os.path.join(path, 'data.db')


class Item(Resource):

    parser = reqparse.RequestParser()  # Run request through it and check the arguments i.e. price in float
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank!')
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every item needs a stored id.')

    @jwt_required()  # Add jwt_required so that get requires JWT authentication token
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name '{name}' already exists"}, 400  # Status code for bad request

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])  # or ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500  # Status code internal service error

        return item.json(), 201  # Status code 201 for created, 202 is accepted (delaying the creation)

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])  # or ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}  # Can use as deltas instead of list
        # comprehension as well ie. list(map(lambda x: x.json(), ItemModel.query.all()))
