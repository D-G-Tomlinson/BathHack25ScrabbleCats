from flask import Flask, request, abort, jsonify
import random
import datetime

import rules

MAX_ROUNDS = 10
BETWEEN = 5
class Round:
    length = 15
    def __init__(self,prev_val):
        if prev_val==MAX_ROUNDS:
            self.rule=None
            self.num=None
            self.finished=None
            return
        self.num = prev_val + 1
        self.rule = rules.generate_rule(self.num).to_tuple()
        self.finished = None
    def finish(self):
        self.finished=datetime.datetime.now()
    def ready_j(self):
        fin = self.finished != None
        return {"rule":self.rule,"num":self.num,"length":Round.length,"finished":fin}

games = {}


class Game:
    def __init__(self,player1):
        self.code = random.randint(10000,99999)
        while self.code in games:
            self.code = random.randint(10000,99999)
        self.player_scores = {player1:(0,1)}
        self.r = None
    def start(self):
        self.r = Round(0)
    def guess(self, player, in_round, score):
        if player not in self.player_scores:
            abort(404, description="that player is not in this game")
        if in_round!=self.r.num:
            print(f"Round is {self.r.num}, player round is {in_round}")
            abort(403, description=f"Round is {self.r.num}, player round is {in_round}")
        p_vals = self.player_scores[player]
        if in_round!=p_vals[1]:
            abort(403, description="already guessed or summat")
        self.player_scores[player] = (p_vals[0] + score, p_vals[1]+1)
        if self.test_all_players(self.r.num+1):
            self.next_round(player)
        
    def test_all_players(self,val):
        ready = True
        for _,r in self.player_scores.values():
            if r!=(val):
                ready = False
        return ready
    def next_round(self,player):
        if self.r.num==MAX_ROUNDS:
            self.r = Round(MAX_ROUNDS)
            self.player_finished(player)
        else:
            self.r.finish()
    def ready_j(self):
        r = None if self.r == None else self.r.ready_j()
        return {"code":self.code,
                "players":self.player_scores,
                "round":r}
    def player_finished(self,player):
        if player in self.player_scores:
            self.player_scores[player]=(self.player_scores[player][0],-1)
            if self.test_all_players(-1):
                games.pop(self.code)
        else:
            abort(403, description="that player don't exist lol")
    
def get_game(game_code):
    try:
        game_code = int(game_code)
    except:
        abort(403,description="thats not an integer")
    if game_code not in games:
        abort(403, description="that game doesn't exist")
    return games[game_code]
    
        
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello from David's Flask!"

@app.delete('/game')
def delete_game():
    global games    
    todel=request.args.get("delete")
    if todel == None:
        games = {}
        return "Success",200    
    try:
        todel = int(todel)        
        games.pop(todel)
        return "Success",200
    except:
        abort(403, description="that game doesn't exist")
@app.delete('/game/leave')
def remove_player():
    g = get_game(request.args.get("game_code"))
    userid = str(request.args.get("userid"))
    if userid not in g.player_scores:
        abort(403, description="youre not in")
    g.player_scores.pop(userid)
    if len(g.player_scores)==0:
        games.pop(g.code)
    return "Success",200
    

@app.get('/game')
def get_games():
    return jsonify({"games":list(games.keys())}),200

@app.patch('/game/guess')
def submit_guess():
    try:
        game_code=request.args.get("game_code")
        player=request.args.get("userid")
        in_round=int(request.args.get("round"))
        score=int(request.args.get("score"))        
    except:
        abort(403, description="error taking in arguments")
    g = get_game(game_code)
    g.guess(player,in_round,score)
    return jsonify({"game_data":g.ready_j()}),200

@app.patch('/game/join')
def join_game():
    g = get_game(request.args.get("game_code"))
    userid = str(request.args.get("userid"))
    if g.r!=None:
        abort(403, description="game is running")
    if userid in g.player_scores:
        abort(403, description="youre already in")
    if len(g.player_scores)>=5:
        abort(403, description="too many in lobby")
    g.player_scores[userid]=(0,1)
    return jsonify({"game_data":g.ready_j()}),200

@app.patch('/game/start')
def start_game():
    g = get_game(request.args.get("game_code"))
    g.start()
    return jsonify({"game_data":g.ready_j()}),200

@app.get('/game/arewethereyet')
def get_update():
    g = get_game(request.args.get("game_code"))
    r = g.r
    if r!=None:
        if r.finished!=None:
            if (datetime.datetime.now()-r.finished).total_seconds()>5:
                g.r = Round(r.num)
        elif r.rule==None and r.num==None:
            userid = request.args.get("userid")
            g.player_finished(userid)
    return jsonify({"game_data":g.ready_j()}),200

@app.post('/game')
def new_game():
    userid = str(request.args.get("userid"))
    if userid == None:
        abort(400, description="no userid provided")
    ng = Game(userid)
    code=ng.code
    games[code]=ng
    return jsonify({"game_data":ng.ready_j()}),201
