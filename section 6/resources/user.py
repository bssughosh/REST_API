import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('password', type=str, required=True, help='This field cannot be blank')

    def post(self):
        data = UserRegister.parser.parse_args()
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        user = UserModel.find_by_username(data['username'])
        if not user:
            query = "INSERT INTO users VALUES (NULL, ?, ?)"
            cur.execute(query, (data['username'], data['password']))

            cur.close()
            con.commit()
            con.close()
            return {'message': 'User Registered'}, 201
        else:
            return {'message': 'A user with same username exists'}, 400
