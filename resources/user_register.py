import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

def parse_data():
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
        type=str, 
        required=True, 
        help="This field cannot be left blank")
    parser.add_argument('password', 
        type=str, 
        required=True, 
        help="This field cannot be left blank")
    return parser.parse_args()

class UserRegister(Resource):
    def post(self):
        req_data = parse_data()
        if UserModel.find_by_username(req_data['username']):
            return {"message": "User '{}' already exist.".format(req_data['username'])}, 400

        user = UserModel(**req_data)
        user.save()

        return {"message": "User '{}' created successfully.".format(req_data['username'])}, 201
