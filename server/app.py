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

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_idetity,get_jwt
from models import *

app = Flask(__name__)
migrate = Migrate(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///carddecks.db"
app.config["JWY_SECRET_KEY"] = 'eu9hr01AsDIGIhugs'

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
        data = request.get_json()
        if not data.get("username") or not data.get("password"):
            return response(
                422,
                message= "No username and/or password provided"
            )

        username = data["username"]
        password = data["password"]

        #looking to see if the user has already signed up:
        existing_user = db.session.scalars(db.select(User).where(User.username == data["username"]))

        #check if it should be if not instead of if
        if existing_user:
            return response(
                422,
                message = "checckinh..."
            )

        user = User(username = username)
        user.password_hash(password)

        db.session.add(user)
        db.session.commit()

        return response(200,
                message= "eureka!",
                data= user.dictionify())


class logging_in(Resource):

    def post(self):

        username = request.get_json()['username']
        password = request.get_json()["password"]

        user = User.query.filter(User.username == username).first()

        if user and user.authenticate(password):
            token = create_access_token(identity=str(user.id))
            return response(200, message="reggaetonnn", 
                    data = {
                        "user": username,
                        "token": token
                    })
        return {'error': ['401 Unauthorized']}, 401



class card_decks(Resource):
    def get(self):
            cards = Decks.query.all()
            return jsonify({cards})

class 누구(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_idetity()
        user = db.session.get(User, int(user_id))
        return response(
            200,
            data  = {
                "user": user.dictionify()
            },
            message = "successful retrieval"
        )
    
api.add_resource(registration, '/me', endpoint = 'me')
api.add_resource(logging_in, '/<string:login>')
api.add_resource(card_decks, '/decks')

 













@app.route("/flop/<resource>", methods = ["GET"])
def get_card_decks():
    pass
#pagination will be each card deck

@app.route("/flop/<str:resource>", methods = ["POST"])
def buy_a_deck():
    pass

@app.route("/flop/<str:resource>/<int:id>", methods = ["PATCH"])
def update_deck():
    pass

@app.route("/flop/<str:resource>/<int:id>", methods = ["DELETE"])
def delete_deck():
    pass

if __name__ == "__main__":
    app.run(port= 5555, debug=True)
