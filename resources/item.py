from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt,get_jwt_identity
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field can not be left blank!"
                        )
    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="Store_id can not be left blank!"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item not found"}, 404

    @jwt_required(fresh=True)
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "an item with name '{}' already exists.".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item."}, 500
        return item.json(), 201

    @jwt_required(fresh=True)
    def delete(self, name):
        claims=get_jwt()
        if not claims['is_admin']:
            return {"message":"Admin privilege required."},401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()
            return {"message": "item deleted"}
        return {"message": "item not found"}, 404

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]
        try:
            item.save_to_db()
        except:
            return {"message": "An Error occured during updating item"}
        return item.json(), 201


class ItemList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id=get_jwt_identity()
        items =[x.json() for x in  ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {
                'items': [item['name'] for item in items],
                'message': 'More data available if you login'
            }, 200

