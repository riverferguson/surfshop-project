from sqlalchemy_serializer import SerializerMixin

from config import *
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy



class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    customer = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    receipts = db.relationship('Receipt', backref='user')
    cart_items = association_proxy('receipts', 'cart_items')
    
    def __repr__(self):
        return f'<User {self.id}: {self.username}'
    
    
class Cartitem(db.Model, SerializerMixin):
    __tablename__ = "cartitems"
    
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    product_id =  db.Column(db.Integer, db.ForeignKey('products.id'))
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipts.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    
    def __repr__(self):
        return f'<Cartitem {self.id}'
    
    
class Product(db.Model, SerializerMixin):
    __tablename__ = "products"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    category = db.Column(db.String)
    condition = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    cart_items = db.relationship('Cartitem', backref='product', cascade='all')
    
    serlize_only = (name, image, category, condition, description, price)
    
    
    def __repr__(self):
        return f'<Product {self.id}'
    
    
class Receipt(db.Model, SerializerMixin):
    __tablename__ = "receipts"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    total = db.Column(db.Float)
    completed = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    cart_items = db.relationship('Cartitem', backref='receipt')
    products = association_proxy('cart_items', 'product')
    
    
    def __repr__(self):
        return f'<Review {self.id}'
       

