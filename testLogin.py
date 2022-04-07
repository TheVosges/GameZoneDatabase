import json
import requests
from cryptography.fernet import Fernet

import main

BASE = "http://127.0.0.1:5000/"


class NormalUser:

    def __init__(self):
        self.userId = None

    def addUser(self):
        print(requests.post(BASE + "users", {"email" : "test@gmail.com", "password" : "test", "type" : "ADD_USER"}))

    def checkLogin(self, email, passowrd):
        response = requests.get(BASE + "users/" + email + "&" + passowrd)
        if int(response.json()) != 0:
            self.userId = int(response.json())
            print("Zalogowano")
        else:
            print("Błędny email lub hasło")

    def getAllLikedGames(self):
        response = requests.get(BASE + "users_games/" + str(self.userId)).json()
        self.liked_games = response
        return response

    def addLikedGame(self, gameId):
        print(requests.post(BASE + "users_games/" + str(self.userId), {"user_id": str(self.userId), "game_id": str(gameId), "type": "ADD"}).json())


if __name__ == '__main__':
    # email = input("Please provide email: ")
    # password = input("Please provide password: ")
    user = NormalUser()
    email = "test@test.com"
    password = "test123"
    user.checkLogin(email, password)
    print(user.getAllLikedGames())
    user.addLikedGame(112)
    # user.addUser()