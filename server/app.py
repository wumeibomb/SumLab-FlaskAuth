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

from flask import Flask, request, jsonify, json, render_template
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
from models import *
from configs import db
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///carddecks.db"
app.config["JWT_SECRET_KEY"] = 'eu9hr01AsDIGIhugs'

migrate = Migrate(app, db) #remember the db

jwt = JWTManager(app)
db.init_app(app)
api = Api(app)


@app.before_request
def logged_in_questionmark():
    accessable_list = [
        "me",
        "login"
    ]
    if (request.endpoint) not in accessable_list and (not verify_jwt_in_request()):
        return {"ERRORRORORORR": "401 Unauthorized, You may not have an account or are Unauthorized"}


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
        
        test = UserSchema().dump(user)

        db.session.add(user)
        db.session.commit()

        TOKEN = create_access_token(identity = str(user.id))
        return jsonify({
                "token": TOKEN,
                "user": test,
                "message": "Successfully created a new account" 
            })
    

class logging_in(Resource):
    

    def post(self):
        #not me using two different methods to get the resource...
        username = request.get_json()['username']
        password = request.get_json()["password"]


        user = User.query.filter(User.username == username).first()
        decks = Decks.query.filter(Decks.user_id == user.id).first()

        if user and user.check_dat_password(password):
            TOKEN = create_access_token(identity=str(user.id))
            if decks == None:
                return jsonify({
                    "error": "User not available, Sign Up?"
                })
            
            return jsonify({
                "username": user.username,
                "token": TOKEN,
                "_message": f"Welcome...{user.username}, ready to play?",
                "equipped_deck": user.equipped_card_deck,
                "sets_aquired": decks.sets_acquired,
                "tier": decks.tier
            })       
        return {'error': '401 Unauthorized, You may not have an account or are Unauthorized'}, 401

class add_decks(Resource): #this is like to update the decks acquired and account status
    def post(self):
        data = request.get_json()

        decks = Decks(
            user_id = get_jwt_identity(),
            sets_acquired = data.get("sets_acquired"),
            account_worth = data.get("account_worth"),
            tier = data.get("tier")
        )

        db.session.add(decks)
        db.session.commit()


class card_decks(Resource):
    def get(self):
        
        cards = db.session.scalars(db.select(Decks)).all()
        print(cards)
            
        get_data = {
            "cards": [eachDeck.dictionify() for eachDeck in cards],
            "message": "successful retrieval"
        }
        return jsonify(get_data)
        
            

class 누구(Resource): #this is the CheckSession alternative, WhoAmI"
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return UserSchema().dump(user), 200
    
api.add_resource(registration, '/register', endpoint = 'register')
api.add_resource(logging_in, '/login', endpoint = 'login')
api.add_resource(card_decks, '/decks', endpoint = 'decks')
api.add_resource(add_decks, "/stats-upgrade", endpoint = 'stats-upgrade')
api.add_resource(누구, "/me", endpoint = 'me')


if __name__ == "__main__":
    app.run(port = 5555, debug= True)