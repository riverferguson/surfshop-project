#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc
import datetime 
from werkzeug.security import generate_password_hash

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import *

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        User.query.delete()
        Product.query.delete()
        Cartitem.query.delete()
        Receipt.query.delete()



user1 = User(email='user1@gmail.com', username='user1', password=generate_password_hash('12345', method='scrypt'))
user2 = User(email='user2@gmail.com', username='user2', password=generate_password_hash('12345', method='scrypt'))
user3 = User(email='user3@gmail.com', username='user3', password=generate_password_hash('12345', method='scrypt'))

users = [user1, user2, user3]
db.session.add_all(users)
db.session.commit()



cart1 = Cartitem(quantity=1, product_id=1, receipt_id=2)
cart2 = Cartitem(quantity=1, product_id=2, receipt_id=1)
cart3 = Cartitem(quantity=1, product_id=3, receipt_id=4)
cart4 = Cartitem(quantity=1, product_id=4, receipt_id=3)
cart5 = Cartitem(quantity=1, product_id=5, receipt_id=2)

items = [cart1, cart2, cart3, cart4, cart5]
db.session.add_all(items)
db.session.commit()



p1 = Product(name='Shortboard', image='', category='surfboard', condition='used', description='surfboard', price=500.00)
p2 = Product(name='longboad', image='', category='surfboard', condition='used', description='surfboard', price=500.00)
p3 = Product(name='fcs fins', image='', category='fins', condition='used', description='fins', price=500.00)
p4 = Product(name='leash', image='', category='leash', condition='used', description='leash', price=500.00)
p5 = Product(name='midlength', image='', category='surfboard', condition='used', description='surfboard', price=500.00)

products = [p1, p2, p3, p4, p5]
db.session.add_all(products)
db.session.commit()



r1 = Receipt(user_id=1, total=1000.00, completed=True)
r2 = Receipt(user_id=2, total=1000.00, completed=True)
r3 = Receipt(user_id=3, total=1000.00, completed=False)
r4 = Receipt(user_id=2, total=1000.00, completed=True)
r5 = Receipt(user_id=1, total=1000.00, completed=True)

receipts = [r1, r2, r3, r4, r5]
db.session.add_all(receipts)
db.session.commit()