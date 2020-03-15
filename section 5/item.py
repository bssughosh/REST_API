from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank")

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            try:
                return item
            except:
                return {'message': 'An Error Occured'}, 500
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "SELECT * FROM items WHERE name=?"
        res = cur.execute(query, (name,))
        row = res.fetchone()
        cur.close()
        con.close()
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        if Item.find_by_name(name):
            return {'message': 'An item already exists with the name {}'.format(name)}, 400

        request_data = Item.parser.parse_args()
        item = {'name': name, 'price': request_data['price']}
        try:
            Item.insert(item)
        except:
            return {'message': 'An Error Occured'}, 500
        return item, 201

    @classmethod
    def insert(cls, item):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cur.execute(query, (item['name'], item['price']))

        cur.close()
        con.commit()
        con.close()

    def delete(self, name):
        if Item.find_by_name(name):
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
        item = Item.find_by_name(name)
        updated_item = {'name': name, 'price': request_data['price']}
        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return {'message': 'An Error Occured'}, 500
        else:

            try:
                Item.update(updated_item)
            except:
                return {'message': 'An Error Occured'}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cur.execute(query, (item['price'], item['name']))

        cur.close()
        con.commit()
        con.close()


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
