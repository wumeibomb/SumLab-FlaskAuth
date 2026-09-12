from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError, validates_schema
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
crypt = Bcrypt(app)

#classes here are for creating the database and storing the db info as well as validatin through the schema
#migrations

class User(db.Model):
    __tablename__ = "UserInfo"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(88), unique = True, nullable = False)
    password = db.Column(db.String(256), nullable = False)
    equipped_card_deck = db.Column(db.String(500)) #LIKELY CHANGE

    decks = db.relationship('Decks', backref= 'user')

    #function to store password in its hashed form  
    @password.setter
    def password_hash(self, password):
        password_hashing = crypt.generate_password_hash(
            password.encode('utf-8')
        )
        self.password = password_hashing.decode('utf-8')
    

    def dictionify(self):
        {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "card_deck": self.equipped_card_deck
        }

class Decks(db.Model):
    __tablename__ = "decks"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('UserInfo.id'))
    sets_acquired = db.Column(db.String(300))
    account_worth = db.Column(db.Integer)#ingame currency not real money nyeheh
    tier = db.Column(db.String(200))#the user tier, either C, B , A, S, SS

    user = db.relationship('User', backref = 'decks')

    def dictionify(self):
        {
            "id": self.id,
            "user_id": self.user_id,
            "sets_acquired": self.sets_acquired,
            "account_worth": self.account_worth,
            "tier": self.tier
        }

#schema:

class UserSchema(Schema):
    id = fields.Int(dump_only = True)
    username = fields.String() 
    equipped_card_deck = fields.String()

    decks = fields.List(fields.Nested(lambda:DeckSchema(exclude=("user",))))

class DeckSchema(Schema):
    id = fields.Int(dump_only = True)
    sets_acquired = fields.String()
    account_worth = fields.Int()
    tier = fields.String()

    user  = fields.Nested(UserSchema(exclude=("decks",)))