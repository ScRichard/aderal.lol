import pymongo, os
from dotenv import load_dotenv
import urllib.parse
import base64
import config
from datetime import datetime
import secrets

load_dotenv()

# Bezpečnosť na prvom mieste
def getPassword():

    passwordbs64 = os.getenv("PASSWORD_D_BS64")

    base64_bytes = base64.b64decode(passwordbs64.encode("ascii"))
    base64_string = base64_bytes.decode("ascii")

    __passwd = ""

    # Remove salting
    base64_string = base64_string[4:]
    for i in range(len(base64_string)):
        if i % 2 == 1:
            continue
        __passwd += base64_string[i]
    return urllib.parse.quote(__passwd, safe="")

class Handler:
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(os.getenv('MONGODB_URI').replace("<password>", getPassword()))
        except Exception as e:
            print(e)
            return

        self.connection = db = self.client.test

        self.users = self.connection[config.ACCOUNTS_COLLECTION]
        self.tokens = self.connection[config.TOKENS_COLLECTION]


    def is_username_valid(self, username):

        return self.users.find_one({"username": username}) == None
    def add_user(self, username : str, password : str):
        self.users.insert_one({
            "username": username,
            "password": password,
            "role_id": 0,
            "access_cookie": {
                "token": None,
                "created": None
            }
        })

    def update_access_cookie(self, username : str):
        self.users.find_one_and_update({"username": username}, {"$set": {
            "access_cookie": {
                "token": secrets.token_hex(10),
                "created": str(datetime.now())
            }
        }})
    def get_all_users(self):
        return self.users.find()

    def is_token_used_and_update(self, username : str, token : str) -> bool:
        result = self.tokens.find_one({ "token": token })

        if result:
            if result["is_used"]:
                return True

            self.tokens.update_one({"token": token}, { "$set":
                                                           {
                                                               "is_used": True,
                                                               "used_at": str(datetime.now()),
                                                               "name": username
                                                           }
                                                        })
            return False
        return True

    def generate_tokens(self, size):
        tokens = []
        for i in range(size):
            tokens.append( {
                "token": secrets.token_hex(32),
                "is_used": False,
                "used_at": None,
                "name": None
            })

        self.tokens.insert_many(tokens)