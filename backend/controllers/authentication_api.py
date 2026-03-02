from flask_restful import Resource # type: ignore
from flask import request,jsonify,make_response # type: ignore
from flask_security import login_user,utils,auth_token_required, roles_required # type: ignore

from controllers.user_datastore import user_datastore # type: ignore
from controllers.database import db # type: ignore

class LoginAPI(Resource):
    def post(self):
        login_credentials = request.get_json()
        
        if not login_credentials:
            result = {
                'message': 'No input data provided'
            }
            return make_response(jsonify(result),400)
        
        email = login_credentials.get('email', None)
        password = login_credentials.get('password', None)
        
        if email is None or password is None:
            result = {
                'message': 'Email and password are required'
            }
            return make_response(jsonify(result),400)
        
        user = user_datastore.find_user(email=email)
        
        if not user:
            result = {
                'message': 'User not found'
            }
            return make_response(jsonify(result),404)
        
        if not utils.verify_password(password, user.password):
            result = {
                'message': 'Invalid password'
            }
            return make_response(jsonify(result),401)
        
        auth_token = user.get_auth_token()    # got this method from the UserMixin class in flask_security
        
        utils.login_user(user)  # this will set the user as the current user in the session
        
        response = {
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'auth_token': auth_token
            }
        }
        return make_response(jsonify(response),200)
    
    
class LogoutAPI(Resource):
    @auth_token_required
    # @roles_required(['admin','user'])
    def post(self):
        utils.logout_user()
        
        response = {
            'mesaage':'Logged out succesfully'
        }
        return make_response(jsonify(response),200)
    
    
class RegisterAPI(Resource):
    def post(self):
        creds = request.get_json()
        
        if not creds:
            result = {
                'message': 'No input data provided'
            }
            return make_response(jsonify(result),400)

        email = creds.get('email', None)
        password = creds.get('password', None)
        
        if not email or not password:
            result = {
                'message': 'Email and password are required'
            }
            return make_response(jsonify(result),400)
        
        if user_datastore.find_user(email=email):
            result = {
                'message': 'User already exists'
            }
            return make_response(jsonify(result),400)
        
        user_role = user_datastore.find_role('user')
        
        user_datastore.create_user(email=email,password=password,roles=[user_role])
        
        db.session.commit()
        
        response = {
            'message': 'User registered successfully'
        }
        return make_response(jsonify(response),201)