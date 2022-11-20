import enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import UniqueConstraint, Index
from sqlalchemy.sql import func

db = SQLAlchemy()


class Side(enum.Enum):
    buy = 1
    sell = 2

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
            server_default=func.now())
    __table_args__ = (UniqueConstraint('name', name='name_uc'),)
    def __repr__(self):
        return f'<User {self.name}>'

class Security(db.Model):
    __tablename__ = 'security'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Security {self.name}>'

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True),
            server_default=func.now())
    side = db.Column(db.Enum(Side), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref="order", lazy=False)
    security_id = db.Column(db.Integer, db.ForeignKey('security.id'))
    security = db.relationship("Security", backref="order", lazy=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    u_idx = db.Column(db.String(100), nullable=False, index=True, unique=True)

    def __repr__(self):
        return f'<Order: {self.side} {self.user} {self.security} {self.quantity}>'

# Index('uuid', Order.user_id, Order.side, Order.security_id, Order.quantity, Order.price)


class Match(db.Model):
    __tablename__ = 'match'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True),
            server_default=func.now())
    sell_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    buy_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Match: {self.sell_order.user.name} {self.buy_order.user.name} {self.sell_order.security.name} {self.quantity}>'

class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True),
            server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref="record", lazy=False)
    payload = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Order: {self.user.name} {self.payload}>'
