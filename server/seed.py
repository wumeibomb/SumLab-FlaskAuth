from app import app
from models import *

with app.app_context():
    print("Rsetting data and adding new data")
    db.session.query(User).delete()
    db.session.query(Decks).delete()

    user1 = User(id = 1, username = "flop123", password = "trUs232", equipped_card_deck = "Starter Deck")
    user2 = User(id = 2, username = "flip321", password = "greTahd", equipped_card_deck = "Cyber Deck")
    user3 = User(id = 3, username = "trope44", password = "dR3enchedInmayo", equipped_card_deck = "Starter Deck")
    user4 = User(id = 4, username = "pterodactylover", password = "str0NG&cuTE", equipped_card_deck = "Rare Animals Deck")

    db.session.add_all([user1, user2, user3, user4])
    db.session.commit()

    decks1 = Decks(id = 1, user_id = user1, sets_acquired = 1, account_worth = 10, tier = "C")
    decks2 = Decks(id = 2, user_id = user2, sets_acquired = 2, account_worth = 70, tier = "C")
    decks3 = Decks(id = 3, user_id = user3, sets_acquired = 1, account_worth = 10, tier = "C")
    decks4 = Decks(id = 4, user_id = user4, sets_acquired = 4, account_worth = 240, tier = "A")
    #decks: Womens history pack, Legends pack, cyber pack, galactic pack, rare animals deck, starter deck
    #worth - 110, 80, 60, 100, 90, 10 = 450, 4 tiers acheivable, C, B, A , S more decks to be added for SS to be obtained.

    db.session.add_all([decks1, decks2, decks3, decks4])
    db.session.commit()

    

