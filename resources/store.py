from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store=StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'mMssage':'Store not found'},404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'Message':"A store with name '{}' already exists.".format(name)},400
        store=StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"Message":"An error occured while creating store."},500
        return store.json(),201

    def delete(self, name):
        store=StoreModel.find_by_name(name)
        if store:
            store.delete()
        return {"Message":"Store deleted"},200


class StoreList(Resource):
    def get(self):
        return {'stores':[store.json() for store in StoreModel.find_all()]}
