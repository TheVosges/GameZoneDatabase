from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api, reqparse
import json
import requests
from cryptography.fernet import Fernet

BASE = "http://127.0.0.1:5000/"

app = Flask(__name__)
api = Api(app)



#################### USERS TABLE #######################################################################################
gamzeZoneApiUsersParser = reqparse.RequestParser()
gamzeZoneApiUsersParser.add_argument("email", type=str, help="Email of user trying to register", required=True)
gamzeZoneApiUsersParser.add_argument("password", type=str, help="Password of user trying to register", required=True)
gamzeZoneApiUsersParser.add_argument("type", type=str, help="Type of request (ADD_USER)", required=True)
class GameZoneApiUsers(Resource):


    def get(self, id="all"):
        with open('users.bin', 'rb') as file:
            data = file.read()
        fernet = keyLoader()
        decMessage = json.loads(fernet.decrypt(data))
        if id != "all":
            if "&" in id:
                return checkLogin(id.split("&")[0], id.split("&")[1])
            else:
                try:
                    return decMessage[id]
                except json.decoder.JSONDecodeError:
                    return "No data for this id", 402
        else:
            try:
                return decMessage
            except KeyError:
                return "Data not found", 401

    #
    def post(self, id = "all"):
        args = gamzeZoneApiUsersParser.parse_args()
        response = requests.get(BASE + "users")
        jsonObj = response.json()
        if (args['type'] == "ADD_USER"):
            if args['email'] in response.json().keys():
                return "This email already exists"
            else:
                newUserID = response.json()[list(response.json().keys())[-1]]["user_id"]
                dict = {"user_id" : str(int(newUserID)+1), "password" : args['password']}
                jsonObj[args['email']] = dict
                fernet = keyLoader()
                encMess = fernet.encrypt(json.dumps(jsonObj).encode())
                with open('users.bin', 'wb') as file:
                    file.write(encMess)

#################### USERS_GAMES TABLE #################################################################################
gamzeZoneApiUsersGamesParser = reqparse.RequestParser()
gamzeZoneApiUsersGamesParser.add_argument("user_id", type=str, help="User identification number", required=True)
gamzeZoneApiUsersGamesParser.add_argument("game_id", type=str, help="Game id from http://api.steampowered.com/ISteamApps/GetAppList/v0001", required=True)
gamzeZoneApiUsersGamesParser.add_argument("type", type=str, help="Type of request (ADD)", required=True)
class GameZoneApiGames(Resource):

    def get(self, id="all"):
        with open('users_games.json', 'r') as file:
            data = file.read()
        jsonObj = json.loads(data)

        if id != "all":
            try:
                return jsonObj[id]
            except json.decoder.JSONDecodeError:
                return "No data for this id", 402
        else:
            try:
                return jsonObj
            except KeyError:
                return "Data not found", 401

    def post(self, id = "all"):
        args = gamzeZoneApiUsersGamesParser.parse_args()
        response = requests.get(BASE + "users_games/" + str(id))
        jsonObj = response.json()
        if (args['type'] == "ADD"):
            if int(args['game_id']) in jsonObj:
                return "This game already is added"
            else:
                jsonObj.append(int(args['game_id']))
                with open("users_games.json", "r") as jsonFile:
                    data = json.load(jsonFile)
                data[str(id)] = jsonObj

                with open("users_games.json", "w") as jsonFile:
                    json.dump(data, jsonFile)



#USERS TABKE
api.add_resource(GameZoneApiUsers, '/users', '/users/<string:id>', endpoint='user')
#USERS_GAMES TABLE
api.add_resource(GameZoneApiGames, '/users_games', '/users_games/<string:id>', endpoint='users')


def checkLogin(email, passowrd):
    try:
        response = requests.get(BASE + "users/" + email).json()
        if response['password'] == passowrd:
            return response['user_id']
        else:
            return 0
    except:
        return 0

def keyLoader():
    with open('key.bin', 'r') as keyFile:
        key = keyFile.read()
    fernet = Fernet(key)
    return fernet


if __name__ == '__main__':
    app.run(debug=True)

# curl -H "Content-Type: application/json" -X POST -d "{ \"name\":\"xyz\", \"address\":\"address_xyz\" }"  http://127.0.0.1:5000
