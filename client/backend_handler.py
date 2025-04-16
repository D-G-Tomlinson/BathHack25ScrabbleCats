#Backend Handler

import requests
import json
from Rules.rules import *

url = "https://dgt.eu.pythonanywhere.com/"

#Hello World
def get():
    x = requests.post(url+"get")
    return json.load(x.text)

#Delete a specific game
def delete_game(game_code):
    x = requests.delete(url+"game?delete="+str(game_code))

#Delete all games
def delete_games():
    x = requests.delete(url+"game")

#Get existing games
#Returns a list of game codes (int)
def get_games():
    x = requests.get(url+"game")
    j = json.loads(x.text)
    return j["games"]

#Join an existing game
#(No return value)
def join(game_code, userid, game):
    x = requests.patch(url+"game/join?game_code="+str(game_code)+"&userid="+userid)
    game.update(x.text)

#Starts game
#Returns GameState
def start_game(game_code,game):
    x = requests.patch(url+"game/start?game_code="+str(game_code))
    game.update(x.text)

#Submit guess
def submit_guess(game_code, userid, roundid, score, game):
    x = requests.patch(url+"game/game_code="+str(game_code)+"&userid="+userid+"&round="+str(roundid)+"&score="+str(score))
    game.update(x.text)

#Do this every second or so to check game state
#Returns GameState
def check_game_state(game_code, userid, game):
    x = requests.get(url+"game/arewethereyet?game_code="+str(game_code)+"&userid="+userid)
    game.update(x.text)

#Create a new game and joins it
#Returns game code
def create_game(userid, game):
    x = requests.post(url+"game?userid="+userid)
    game.update(x.text)
    


class GameState():

    def __init__(self, json_text=None):
        if json_text != None:
            self.update(json_text)
        
    #Get Game Code (int)
    def get_game_code(self):
        return self.game_code

    #Get score from named player
    def get_player_score(self, userid):
        return self.players[userid][0]

    #Get current round id
    def get_current_roundid(self):
        return self.round["num"]

    #Get current rule (returns Rule object)
    def get_current_rule(self):
        rule_info = self.round["rule"]
        rule = create_rule(rule_info[0], rule_info[1], rule_info[2], rule_info[3])
        return rule

    #Get list of players (should work)
    def get_list_of_players(self):
        return self.players.keys()

    def update(self, json_text):
        j = json.loads(json_text)
        game_data = j["game_data"]
        self.game_code = game_data["code"]
        self.players = game_data["players"]
        self.round = game_data["round"]
        


        
