from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

items = []

# Utility
def get_item_by_name(name):
    return next(filter(lambda x: x['name'] == name, items), None)    

# Utility
def parse_data():
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required=True, 
        help="This field cannot be left blank")
    parser.add_argument('store_id', 
        type=int, 
        required=True, 
        help="Every item needs a store id.")

    return parser.parse_args()

class Item(Resource):

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {'message': 'Item not found'}, 404  # Item not found error

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exist".format(name)}, 400
        req_data = parse_data()
        item = ItemModel(name, req_data['price'], req_data['store_id'])

        try:
            item.save()
        except:
            # Internal server error
            return {"message": "An error occured inserting the item."}, 500  

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()
            return {'message': 'Item {} is deleted'.format(name)}
        else:
            return {'message': 'No item named {} found'.format(name)}, 404

    def put(self, name):
        req_data = parse_data()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = req_data['price']
        else:
            item = ItemModel(name, req_data['price'], req_data['store_id'])

        try:
            item.save()
        except:
            return {"message": "An error occurred inserting the item"}, 500

        return item.json(), 200


class ItemList(Resource):
    def get(self):
        # 
        # alternative to List Comprehension is Lambda fnc
        #  list(map(lambda: x: x.json(), ItemModel.query.all()))
        #
        return {'items': [item.json() for item in ItemModel.query.all()]}
