# services/users/project/api/models.py
from datetime import datetime
from sqlalchemy.sql import func
from project import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(225), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'active': self.active
        }

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode()



class Customers(db.Model):
    __tablename__ = 'customers'
    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name    = db.Column(db.String(150), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    orders  = db.relationship('Orders', backref='customer', lazy='dynamic')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'active': self.active,
            'orders': self.orders,
        }

    def __init__(self, name, orders):
        self.name = name
        self.orders = orders


class Product(db.Model):
    __tablename__ = 'products'
    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name    = db.Column(db.String(150), unique=True, nullable=False)
    active  = db.Column(db.Boolean(), default=True, nullable=False)
    items   = db.relationship('Item', backref='product', lazy='dynamic')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'active': self.active,
            'items': self.items,
        }

    def __init__(self, name, items):
        self.name = name
        self.items = items


class Order(db.Model):
    __tablename__ = 'orders'
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), index=True)
    date = db.Column(db.DateTime, default=datetime.now)
    items = db.relationship('Item', backref='order', lazy='dynamic', cascade='all, delete-orphan')

    def to_json(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'date': self.date,
            'items': self.items,
        }

    def __init__(self, customer_id, date, items):
        self.customer_id    = customer_id
        self.date           = date
        self.items          = items


class Item(db.Model):
    __tablename__ = 'items'
    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), index=True)
    quantity = db.Column(db.Integer)

    def to_json(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
        }

    def __init__(self, order_id, product_id, quantity):
        self.order_id    = order_id
        self.product_id  = product_id
        self.quantity    = quantity
