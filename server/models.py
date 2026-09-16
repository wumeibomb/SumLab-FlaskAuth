from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError, validates_schema
from flask_migrate import Migrate
from sqlalchemy.ext.hybrid import hybrid_property

from configs import db, bcrypt


#classes here are for creating the database and storing the db info as well as validatin through the schema
#migrations

class User(db.Model):
    __tablename__ = "UserInfo"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(88),unique = True, nullable = False)
    password_h = db.Column(db.String(256), nullable = False)
    equipped_card_deck = db.Column(db.String(500), default = "Starter Deck") 

    decks = db.relationship('Decks', back_populates= 'user')

    #function to store password in its hashed form  
    @hybrid_property
    def password_hash(self):
        raise Exception('Password hashes may not be viewed.')
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8')
        )
        self.password_h = password_hash.decode('utf-8')

    def check_dat_password(self, password):
        return bcrypt.check_password_hash(self.password_h, password.encode('utf-8'))
    

    def dictionify(self): #remember the return statement (TT)
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password_h,
            "card_deck": self.equipped_card_deck
        }

    def __repr__(self):
        return f'<User {self.username}, ID: {self.id}>'

class Decks(db.Model):
    __tablename__ = "Decks"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('UserInfo.id'))
    sets_acquired = db.Column(db.String(300), default = 1)
    account_worth = db.Column(db.Integer, default = 10)#ingame currency not real money nyeheh
    tier = db.Column(db.String(100), default = "C")#the user tier, either C, B , A, S, SS

    user = db.relationship('User', back_populates = 'decks')

    def dictionify(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "sets_acquired": self.sets_acquired,
            "account_worth": self.account_worth,
            "tier": self.tier
        }
    def __repr__(self):
            return f'<Decks  ID: {self.id} SETS: {self.sets_acquired} TIER: {self.tier}>'

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