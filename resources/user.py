from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()  # Capture the body from the POST auth request

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400


        # user = UserModel(data['username'], data['password'])
        # Simplify above with this as it only takes items in the parser above ie. username and password
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201
