"""
    Launches the Flask app
"""
import os
from os.path import join, dirname
from settings import db, app, socketio
from inventory import get_user_inventory, get_asc_inventory, get_dsc_inventory, search_bar, filter_by_type
from progress import saveProgress, loadProgress
from achievements import init_achievements, update_achievement, get_achievement_reward, get_all_achievements
import models
import flask
# tests

# game logic
import game.game
import game.game_io
from game.game import game
from game.game_io import deconstruct_player
from game.player import Player


# For shop, checks if item has been purchased.
item = 0
# Used to check if user bought item again.
times = 1

def player_info():
    """ Send playerinfo to js. Currently sends dummy data. """
    player_info = {
        "user_party": ["player1", "player2", "player10"],
        "user_inventory": ["coins", "sword", "shield"],
        "user_chatlog": [
            "welcome to the world",
            "attack",
            "user attacks, hitting the blob for 10pts",
        ],
    }
    if item == 1:
        x = player_info["user_inventory"]
        global times
        if times == 0:
            x.extend(["Health Pack"])
            times += 1
        else:
            x.extend(["Health Pack"] * times)
            times += 1

        print(x)
        player_info["user_inventory"] = x
    socketio.emit("player info", player_info)

userlist = [1]
idlist = [""]

@socketio.on("google login")
def google_login(data):
    """ Google Login """
    # idinfo contains dictionary of user info
    userdat = data["UserInfo"]
    profiledat = userdat["profileObj"]
    em = profiledat["email"]
    all_email = [username.email for username in db.session.query(models.username).all()]
    if em not in all_email:
        user = models.username(email=em)
        db.session.add(user)
        db.session.commit()
        init_achievements(em)
    userid = db.session.query(models.username).filter_by(email=em).first()
    userlist.append(userid.id)
    
    #Used to distinguish users, for database user calls 
    flask.session["user_id"] = em
    idlist.append(em)
    
    
    #check if user has character
    socketio.emit("has character", False)

def send_party(): 
    #TODO get party from database 
    
    #DUMMY DATA
    user_party=["player1", "player2", "player10"]
    socketio.emit('user party', user_party)
    
def send_chatlog():
    #TODO get chatlog from database
    
    #DUMMY DATA
    user_chatlog=[
            "welcome to the world",
            "attack",
            "user attacks, hitting the blob for 10pts"
    ]
    socketio.emit('user chatlog', user_chatlog)


@socketio.on("user input")
def parse_user_input(data):
    """ Parse user inputs in order to interact with game logic """
    print(
        data["input"]
    )


@socketio.on("get party")
def get_party():
    send_party()
    
@socketio.on("get inventory")
def get_inventory():
    inventory = get_user_inventory()
    send_inventory(inventory)

def send_inventory(inventory):
    socketio.emit('user inventory', inventory)

@socketio.on("get chatlog")
def get_chatlog():
    #TODO get chatlog from database
    
    #DUMMY DATA
    user_chatlog=[
            "welcome to the world",
            "attack",
            "user attacks, hitting the blob for 10pts"
    ]
    send_chatlog()
    
@socketio.on("get shop")
def get_shop():
    #TODO get chatlog from database
    USER = flask.session["user_id"]
    user= db.session.query(models.username).filter_by(email=USER).first()
    character = db.session.query(models.character).filter_by(user_id=user.id).first()
    money = character.money
    db.session.commit()
    #DUMMY DATA
    user_shop={
            'money': money,
            'shop': [['car',250],['dog',100]]
    }
    send_shop(user_shop)

def send_shop(user_shop):
    socketio.emit('user shop', user_shop)

# Test atm for the shop
@socketio.on("item purchased")
def item_purchased(data):
    """ Purchase item """
    cost = data['cost']
    item = data['item']
    print(item)
    print(cost)
    USER = flask.session["user_id"]
    user= db.session.query(models.username).filter_by(email=USER).first()
    character = db.session.query(models.character).filter_by(user_id=user.id).first()
    character.money = character.money - int(cost)
    money = character.money 
    db.session.commit()
    # player_info()
    update_achievements('item')
    

@socketio.on("user new character")
def character_creation(data):
    """ Create character """
    player = Player()
    player.id = data["name"]
    player.gen = data["gen"]
    player.character_class = data["classType"]
    # data includes character attributes: name, gender and character class
    if data["classType"] == "Jock":
        player.make_jock()
    elif data["classType"] == "Bookworm":
        player.make_bookworm()
    elif data["classType"] == "NEET":
        player.make_neet()
    USER = userlist[-1]
    email = db.session.query(models.username).filter_by(id=USER).first()
    userid = email.id
    dbplayer = models.character(
        user_id=userid,
        character_class=data["classType"],
        character_name=data["name"],
        gender=data["gen"],
        strength=player.strength,
        dex=player.dex,
        con=player.con,
        intel=player.intel,
        cha=player.cha,
        luck=player.luk,
        max_health=player.max_health,
        health=player.health,
        max_mana=player.max_mana,
        mana=player.mana,
        money=player.money,
    )
    db.session.add(dbplayer)
    db.session.commit()


def update_achievements(key,num=1):
    update_achievement(flask.session["user_id"],key,num)
    
    
@socketio.on("get achievements")
def get_achievements():
    """ get achievements """
    achievements = get_all_achievements(flask.session["user_id"])
    socketio.emit('achievement', achievements)


def send_reward():
   return 0 

@socketio.on("get reward")
def get_reward(data):
    get_achievement_reward(flask.session["user_id"],data["id"])
    send_reward()
    
# ======================================================================================
@app.route("/")
def about():
    """ main page """
    return flask.render_template("landing_page.html")

#=======================================================================================

@app.route("/character_selection.html")
def char_select():
    """ main page """
    return flask.render_template("character_selection.html")

#=======================================================================================

@app.route("/login.html")
def index():
    """ main page """
    return flask.render_template("index.html")

# ======================================================================================
@app.route("/character_creation.html")
def char_create():
    """ character creation page """
    return flask.render_template("character_creation.html")


# =======================================================================================
@app.route("/main_chat.html")
def main():
    """ main chat window """
    return flask.render_template("main_chat.html")
    

#=========================================================================================
@app.route("/options.html")
def options():
    """ main chat window """
    #saveProgress()
    print(idlist[-1] + " YOOOOO")
    return flask.render_template("options.html")


# =======================================================================================
@app.route("/achievement_menu.html")
def achievement_menu():
    """ achievement menu page """
    return flask.render_template("achievement_menu.html")


# =======================================================================================
# RUNS ON THIS HOST AND PORT
if __name__ == "__main__":
    socketio.run(
        app,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True
    )