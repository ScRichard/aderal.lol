import hashlib, os

ACCOUNTS_COLLECTION = "Users"
TOKENS_COLLECTION = "Tokens"

def get_salted_password(password :str) -> str:
    __password = ""
    for char in password:
        __password += char + os.getenv("SALTING_BETWEEN_CHARS")
    __password = os.getenv("SALTING_FOR_PASSWORD")+__password[::-1]+os.getenv("SALTING_FOR_PASSWORD")

    return hashlib.sha256(__password.encode()).hexdigest()