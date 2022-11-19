import os, enum

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


def create_app(test_config=None):
    # create the extension
    db = SQLAlchemy()
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    #app.config.from_mapping(
    #    SECRET_KEY='dev',
    #    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    #)

    # configure the SQLite database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize the app with the extension
    db.init_app(app)


    class Side(enum.Enum):
        buy = 1
        sell = 2

    class User(db.Model):
        __tablename__ = 'user'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        created_at = db.Column(db.DateTime(timezone=True),
                server_default=func.now())
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
        quantity = db.Column(db.Integer, nullable=False)

        def __repr__(self):
            return f'<Order: {self.side} {self.user.name} {self.security.name} {self.quantity}>'

    class Match(db.Model):
        __tablename__ = 'match'
        id = db.Column(db.Integer, primary_key=True)
        created_at = db.Column(db.DateTime(timezone=True),
                server_default=func.now())
        sell_id = db.Column(db.Integer, db.ForeignKey('order.id'))
        sell_order = db.relationship("Order", backref="match", lazy=True)
        buy_id = db.Column(db.Integer, db.ForeignKey('order.id'))
        buy_order = db.relationship("Order", backref="match", lazy=True)
        quantity = db.Column(db.Integer, nullable=False)

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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
