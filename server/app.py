#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, session, abort, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource
from functools import wraps
#import ipdb

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

class Products(Resource):
    def get(self):
        product = [p.to_dict() for p in Product.query.all()]
        return make_response(product, 200)
    
    def post(self):
        # if session.get('user_id'):
        #     found_user = User.query.filter(User.id == session.get('user_id')).first()
        #     if found_user.customer == False:
                new = request.get_json()
                
                new_product = Product(
                    name = new['name'],
                    image = new['image'],
                    category = new['category'],
                    condition = new['condition'],
                    description = new['description'],
                    price = new['price']
                )
                
                db.session.add(new_product)
                db.session.commit()
                
                return make_response(new_product.to_dict(), 201)
            # return {'error': 'Unauthorized'}, 401
        
api.add_resource(Products, '/products')

class ProductsByID(Resource):
    def get(self, id):
        product = Product.query.filter(Product.id==id).first()
        return make_response(product.to_dict(), 200)
    
    def patch(self, id):
        if session.get('user_id'):
            found_user = User.query.filter(User.id == session.get('user_id')).first()
            if found_user.customer == False:
                data = request.get_json()
                update = Product.query.filter_by(id=id).first()
                
                for key in data:
                    setattr(update, key, data[key])
                    
                db.session.add(update)
                db.session.commit()
                return make_response(update.to_dict(), 200)
            return {'error': 'Unauthorized'}, 401
        return {'error': 'Unauthorized'}, 401
    
    def delete(self, id):
        to_delete = Product.query.filter(Product.id==id).first()
        db.session.delete(to_delete)
        db.session.commit()
        
        return make_response({'message': 'Product successfully deleted.'}, 204)
    
api.add_resource(ProductsByID, '/products/<int:id>')


class Cartitems(Resource):
    def get(self):
        if session.get('user_id'):
            cart_items = Cartitem.query.join(Receipt.cart_items).filter(Receipt.user_id == session.get('user_id')).all()
            cart_items_dict = [item.to_dict() for item in cart_items]
            return make_response(cart_items_dict, 200)
        
    def post(self):
        if session.get('user_id'):
            found_user = User.query.filter(User.id == session.get('user_id')).first()
            if found_user:
                new = request.get_json()
                cart_item = Cartitem(
                    quantity = new['quantity'],
                    product_id = new['product_id'],
                    receipt_id = new['receipt_id']
                )
                
                db.session.add(cart_item)
                db.session.commit()
                
                return make_response(cart_item.to_dict(), 201)
            return {'error': 'Unauthorized'}, 401
        
api.add_resource(Cartitems, '/cartitems')


class CartitemByID(Resource):
    def patch(self, id):
        if session.get('user_id'):
            found_user = User.query.filter(User.id == session.get('user_id')).first()
            if found_user:
                data = request.get_json()
                update = Cartitem.query.filter_by(id=id).first()
                
                if update:
                    for attr in data:
                        setattr(update, attr, data[attr])
                    db.session.add(update)
                    db.session.commit()
                    return make_response(update.to_dict(), 200)
                else:
                    return {'error':'Item not found'}, 404
            return {'error': 'Unauthorized'}, 401
        return {'error': 'Unauthorized'}, 401
    
    def delete(self, id):
        to_delete = Cartitem.query.filter(Cartitem.id==id).first()
        db.session.delete(to_delete)
        db.session.commit()
        
        return make_response({'message': 'item successfully deleted.'})
    
api.add_resource(CartitemByID, '/cartitems/<int:id>')

class Receipts(Resource):

    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user.customer == True:
            receipt = Receipt.query.filter(Receipt.user_id == session.get('user_id')).all()
            if receipt:
                receipts = [item.to_dict() for item in receipt]
                print(receipts)
                return make_response(receipts, 200)
        else:
            all_receipts = [receipt.to_dict() for receipt in Receipt.query.all()]
            return make_response(all_receipts, 200)
            
        return {'error': 'Not Found'}, 404
    
    
    def post(self):
        
        new = request.get_json()
        print(new)
        new_receipt = Receipt()
       
        new_receipt.user_id = new['user_id']
        new_receipt.total = 0.00
        new_receipt.completed = False
        
        db.session.add(new_receipt)
        db.session.commit()
        return make_response(new_receipt.to_dict(), 201)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
