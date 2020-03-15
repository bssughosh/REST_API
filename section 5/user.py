import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        con = sqlite3.connect('data.db')
        cursor = con.cursor()

        query = "SELECT * FROM users WHERE username = ?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)

        else:
            user = None

        cursor.close()
        con.close()
        return user

    @classmethod
    def find_by_userid(cls, user_id):
        con = sqlite3.connect('data.db')
        cursor = con.cursor()

        query = "SELECT * FROM users WHERE id = ?"
        result = cursor.execute(query, (user_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)

        else:
            user = None

        cursor.close()
        con.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('password', type=str, required=True, help='This field cannot be blank')

    def post(self):
        data = UserRegister.parser.parse_args()
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        user = User.find_by_username(data['username'])
        if not user:
            query = "INSERT INTO users VALUES (NULL, ?, ?)"
            cur.execute(query, (data['username'], data['password']))

            cur.close()
            con.commit()
            con.close()
            return {'message': 'User Registered'}, 201
        else:
            return {'message': 'A user with same username exists'}, 400
