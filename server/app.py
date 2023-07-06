#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, jsonify, session, abort, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource
from functools import wraps
import ipdb

# Local imports
from config import *
from models import User, Product, Receipt, Cartitem

# Views go here!
@app.route('/')
def home():
    return 'welcome to the home page'

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        product_owner = session.get('user_id')
        prdouct_to_delete = db.session.get(Product, kwargs)
        if not session['user_id'] or product_owner != prdouct_to_delete.user_id:
            return make_response({'error': 'Unauthorized'}, 401)
        return func(*args, **kwargs)
    return decorated_function

class SignUp(Resource):
    
    def post(self):
        email = request.get_json()['email']
        username = request.get_json()['username']
        password = request.get_json()['password']
    
        if owner := User.query.filter_by(username= username).first():
            return make_response('That user already exists. Try logging in')
    
        new_user = User(email=email, username=username, password=generate_password_hash(password, method='scrypt'))
        
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id

        return make_response('New owner created.')
        
api.add_resource(SignUp, '/signup')

class SignIn(Resource):
    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']
        
        existing_user = User.query.filter_by(username=username).first()
        
        if not existing_user or not check_password_hash(existing_user.password, password):
            return make_response('Username or password was incorrect. Please try again.', 404)
        
        session['user_id'] = existing_user.id
        return make_response(existing_user.to_dict())
        
api.add_resource(SignIn, '/signin')

class CheckSession(Resource):
    def get(self):
        if user := User.query.filter(User.id == session.get('user_id')).first():
            return user.to_dict()
        else:
            return make_response({'message': '401: Not Authorized'}, 401)

api.add_resource(CheckSession, '/check_session')

class SignOut(Resource):
    def delete(self):
        session['user_id'] = None
        return make_response({'message': '204: No Content'}, 204)

api.add_resource(SignOut, '/signout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
