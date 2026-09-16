# Flask Summative Lab - Backend
- This is a sumamtive lab that focuses on the production of a the backend of a flask application and its database.

LINK FOR DEPLOYED WEP PAGE: (my deployment lowkey failed?)
![alt text](image.png)

## To utilize:
 - Clone this repo, enter your IDE and access the cloned folder. Write the command pipenv shell and then open the server folder within the repo. 
 - After this, use the pipenv install command to have the required dependencies on your virtual environment.
 - The SQL Viewer extension (or adjacent) is also required for this project so please install it.
 - On this project, the database already contains the needed information to test the login.
 
## To test:
 - The original passwords for the users within the database are:
    - user flop123 - password: trUs232
    - user flip321 - password: greTahd
    - user trope44 - password: dR3enchedInmayo
    - user pterodactylover - password: str0NG&cuTE

 - The decks of cards and their prices are:
    - Starter Deck - 10
    - Womens history pack - 110
    - Legends pack - 80
    - cyber pack - 60
    - galactic pack - 100
    - rare animals deck - 90

And there are 4 tiers currently acheivable -  C, B, A, S.
## JWT Secret Key:
 - For testing purposes i'll provide the key, however note that to test the keys operation, uncommenting the jwt secret key lines in the configs.py and the app.py is important.
 - The secret key is: eu9hr01AsDIGIhugs

## Issues:
 -  No Pagination
 - WhoAmI class resource does not produce a proper output with jsonify (Object of type function not JSON serializable but I'm not sure which is the function?)
 - psycopg2 has not been used as I do not have the requirements.
psycopg2 not on my project as computer doesn't meet requirements.

