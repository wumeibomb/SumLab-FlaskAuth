from app import app
from models import *

with app.app_context():
    print("Resetting and adding new data")
    db.session.query(User).delete()
    db.session.query(Decks).delete()

    user1 = User(id = 101, username = "flop123", password_h = "trUs232", equipped_card_deck = "StarterDeck")
    user2 = User(id = 102, username = "flip321", password_h = "greTahd", equipped_card_deck = "CyberDeck")
    user3 = User(id = 103, username = "trope44", password_h = "dR3enchedInmayo", equipped_card_deck = "StarterDeck")
    user4 = User(id = 104, username = "pterodactylover", password_h = "str0NG&cuTE", equipped_card_deck = "RareAnimalsDeck")

    db.session.add_all([user1, user2, user3, user4])
    db.session.commit()

    decks1 = Decks(id = 1, user_id = user1.id, sets_acquired = 1, account_worth = 10, tier = "C")
    decks2 = Decks(id = 2, user_id = user2.id, sets_acquired = 2, account_worth = 70, tier = "C")
    decks3 = Decks(id = 3, user_id = user3.id, sets_acquired = 1, account_worth = 10, tier = "C")
    decks4 = Decks(id = 4, user_id = user4.id, sets_acquired = 4, account_worth = 240, tier = "A")
    #decks: Womens history pack, Legends pack, cyber pack, galactic pack, rare animals deck, starter deck
    #worth - 110, 80, 60, 100, 90, 10 = 450, 4 tiers acheivable, C, B, A , S more decks to be added for SS to be obtained.

    db.session.add_all([decks1, decks2, decks3, decks4])
    db.session.commit()

    

