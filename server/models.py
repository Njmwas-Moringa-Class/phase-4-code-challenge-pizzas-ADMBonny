from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }

class Pizza(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    ingredients = db.Column(db.String(256), nullable=False)
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza', cascade="all, delete-orphan")

    def to_dict(self, include_restaurant_pizzas=False):
        pizza_dict = {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients
        }
        if include_restaurant_pizzas:
            pizza_dict['restaurant_pizzas'] = [rp.to_dict() for rp in self.restaurant_pizzas]
        return pizza_dict

class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    @validates('price')
    def validate_price(self, key, price):
        if not 1 <= price <= 30:
            raise ValueError("Price must be between 1 and 30")
        return price

    def to_dict(self):
        return {
            'id': self.id,
            'pizza_id': self.pizza_id,
            'restaurant_id': self.restaurant_id,
            'price': self.price,
            'pizza': self.pizza.to_dict(),
            'restaurant': self.restaurant.to_dict()
        }