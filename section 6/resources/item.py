from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            try:
                return item.json()
            except:
                return {'message': 'An Error Occurred'}, 500
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'An item already exists with the name {}'.format(name)}, 400

        request_data = Item.parser.parse_args()
        item = ItemModel(name, request_data['price'])
        try:
            item.insert()
        except:
            return {'message': 'An Error Occurred'}, 500
        return item.json(), 201

    def delete(self, name):
        if ItemModel.find_by_name(name):
            con = sqlite3.connect('data.db')
            cur = con.cursor()

            query = "DELETE FROM items WHERE name=?"
            cur.execute(query, (name,))

            cur.close()
            con.commit()
            con.close()
            return {'message': 'Item Deleted'}
        else:
            return {'message': 'Item not found'}

    def put(self, name):
        request_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, request_data['price'])
        if item is None:
            try:
                updated_item.insert()
            except:
                return {'message': 'An Error Occurred'}, 500
        else:

            try:
                updated_item.update()
            except:
                return {'message': 'An Error Occurred'}, 500
        return updated_item


class ItemList(Resource):
    def get(self):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "SELECT * FROM items"
        res = cur.execute(query)
        items = []

        for row in res:
            items.append({'name': row[0], 'price': row[1]})

        cur.close()
        con.close()

        return {'items': items}
