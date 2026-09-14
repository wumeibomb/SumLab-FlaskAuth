#login, logout and sessions. 
#signing up and its authentication 
#authenticate the usernames as unidentical to those already in db
#create seed for db
#figure out pagination?? and do CRUD endpoints
#check session route
#1-authenticate2-sessionobjectholdauthentications3-sessioncookieforeachrequest4-logoutclearsession
#userowneddresource is card decks. app is a solitaire game that has users and their respective card decks are stored and
#that is the resource. card decks, acquireddate, usage rate, win rate, loss rate, equip
#protection to ensure account isn't hacked.
#create-post = Buying a card deck, update = upgrade cards two tiers, get cards = displaying crd decks, delete = selling card decks

from flask import Flask, request, jsonify, json
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from models import *
from configs import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///carddecks.db"
app.config["JWY_SECRET_KEY"] = 'eu9hr01AsDIGIhugs'

migrate = Migrate(app, db) #remember the db

jwt = JWTManager(app)
db.init_app(app)
api = Api(app)


def response(code, message, data):
    return jsonify({
        "message" : message,
        "data": data
    }), code

class registration(Resource):

    def post(self):
        data = request.get_json() or {}

        if not data.get("username") or not data.get("password"):
            return jsonify({
                "message": "No Username or Password Provided"
            })

        username = data["username"]
        password = data["password"]

        #looking to see if the user has already signed up:
        existing_user = db.session.scalars(db.select(User).where(User.username == username))

        existing_user_output = {
            "message": "An account is already under this name, try another",
        }
        #check if it should be if not instead of if
        if not existing_user:
            return jsonify(existing_user_output)

        user = User(username= username)
        user.password_hash = password
        print(user.username)

        db.session.add(user)
        db.session.commit()

        get_data = {
            "message": "Created New Account!",
            "Username": f"{user.username}"
        }

        return jsonify(get_data)


class logging_in(Resource):

    def post(self):

        username = request.get_json()['username']
        password = request.get_json()["password"]

        user = User.query.filter(User.username == username).first()

        if user and user.authenticate(password):
            TOKEN = create_access_token(identity=str(user.id))
            
            return response(200, message="reggaetonnn", 
                    data = {
                        "user": username,
                        "token": TOKEN
                    })
        return {'error': ['401 Unauthorized, You may not have an account or are Unauthorized']}, 401



class card_decks(Resource):

    def get(self):
        cards = db.session.scalars(db.select(Decks)).all()
        print(cards)
            #return jsonify(response(200, data= {
             #   "cards": cards
            #},#. message= "SUCCESSS"))
        get_data = {
            "cards": [eachDeck.dictionify() for eachDeck in cards],
            "message": "successful retrieval"
        }
        return jsonify(get_data)
        
            

class 누구(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return UserSchema().dump(user), 200
    
api.add_resource(registration, '/me', endpoint = 'me')
api.add_resource(logging_in, '/login')
api.add_resource(card_decks, '/decks')

if __name__ == "__main__":
    app.run(port = 5555, debug= True)