"""
    Launches the Flask app
"""
import os
from os.path import join, dirname
from settings import db, app, socketio
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


# ===================================================================================

# For shop, checks if item has been purchased.
item = 0
# Used to check if user bought item again.
times = 1
#plesae

# function that marks and saves progress,
#  either inserting a new character into database or updating an existing one.
def saveProgress():
    """ Saves the user's progress to the database """
    FLAG = "INSERT"
    USER = userlist[-1]
    all_character = [
        character.character_name
        for character in db.session.query(models.character).all()
    ]
    all_userid = [
        user_id.user_id for user_id in db.session.query(models.character).all()
    ]
    dict = {}
    for i in range(len(all_character)):
        dict[all_userid[i]] = all_character[i]

    USER = userlist[-1]
    email = db.session.query(models.username).filter_by(id=USER).first()
    key = email.id
    characterList = db.session.query(models.character).filter_by(user_id=key)

    player = Player()
    # needs to pick character by user choice
    for char in characterList:
        if char.character_name == "popo":
            player = char

    statslist = deconstruct_player(player)

    for x, y in dict.items():
        if USER == x and statslist[0] == y:
            FLAG = "UPDATE"
            break
        else:
            FLAG = "INSERT"

    if FLAG == "INSERT":
        init_achievements()
        chara = models.character(
            user_id=USER,
            character_name=statslist[0],
            strength=statslist[1],
            dex=statslist[2],
            con=statslist[3],
            intel=statslist[4],
            cha=statslist[5],
            luck=statslist[6],
            max_health=statslist[7],
            health=statslist[8],
            max_mana=statslist[9],
            mana=statslist[10],
            money=statslist[11],
            checkpoint=statslist[12],
            gender=statslist[13],
            character_class=statslist[14],
        )
        db.session.add(chara)
        db.session.commit()
    elif FLAG == "UPDATE":
        chara = (
            db.session.query(models.character)
            .filter_by(user_id=USER, character_name=statslist[0])
            .first()
        )
        chara.strength = statslist[1]
        chara.dex = statslist[2]
        chara.con = statslist[3]
        chara.intel = statslist[4]
        chara.cha = statslist[5]
        chara.luck = statslist[6]
        chara.max_health = statslist[7]
        chara.health = statslist[8]
        chara.max_mana = statslist[9]
        chara.mana = statslist[10]
        chara.money = statslist[11]
        chara.checkpoint = statslist[12]
        chara.gender = statslist[13]
        chara.character_class = statslist[14]
        db.session.commit()
    else:
        print("weird error")

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
    userid = db.session.query(models.username).filter_by(email=em).first()
    userlist.append(userid.id)

    #Used to distinguish users, for database user calls 
    flask.session["user_id"] = em
    
    #check if user has character
    
def send_party(): 
    #TODO get party from database 
    
    #DUMMY DATA
    user_party=["player1", "player2", "player10"]
    socketio.emit('user party', user_party)


def get_user_inventory(): 
    #TODO get log from database
    if "user_id" in flask.session:
        items = []
        for x, a, i in models.db.session.query(models.username, models.character, models.inventory).\
        filter(models.username.email == flask.session["user_id"]).\
        filter(models.character.user_id == models.username.id).\
        filter(models.inventory.character_id == models.character.id):
                items.append(i.items)
        
        return items
    else: 
        return([
            "error",    #replace this with error
        ])
    
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
    print(flask.session["user_id"])
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


# Test atm for the shop
@socketio.on("item purchased")
def item_purchased():
    """ Purchase item """
    global item
    item = 1
    player_info()



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

def init_achievements():
    USER = userlist[-1]
    email = db.session.query(models.username).filter_by(id=USER).first()
    userid = email.id
    achievements = models.achievements(
        user_id=userid,
        win_id='wins',
        win_title='King of the land',
        win_description='Reach the final end state three times to claim your custom prize.',
        wins='0',
        win_f='3',
        win_prize = '0',
        damage_id = 'damage',
        damage_title = 'Soul Seeker',
        damage_description = 'Deal damage to your oppenents in battle. Deal 300 points of damage to claim a valueable reward.',
        damage_dealt = '0',
        damage_f = '300',
        damage_prize = '0',
        items_id = 'items',
        item_title = 'Living Lavish',
        item_description = 'Find items around the map or buy items from the shop. Obtain 2 items to claim a valueable reward.',
        items = '0',
        item_f = '2',
        item_prize = '0',
        money_id = 'money',
        money_title = 'Money Laundering',
        money_description = 'Be on the look out for money. Collect $300 to claim a valueable reward.',
        moneys = '0',
        money_f = '300',
        money_prize = '0'
    )
    db.session.add(achievements)
    db.session.commit()
    
@socketio.on("get achievements")
def get_achievement():
    """ get achievements """
    #TODO get achievements from database
    USER = userlist[-1]
    email = db.session.query(models.username).filter_by(id=USER).first()
    userid = email.id
    a_info = (db.session.query(models.achievements).filter_by(user_id=userid).first())
    achievement=[
        [
            a_info.win_id,
            a_info.win_title,
            a_info.win_description,
            a_info.wins,
            a_info.win_f,
            a_info.win_prize
        ],
        [
            a_info.damage_id,
            a_info.damage_title,
            a_info.damage_description,
            a_info.damage_dealt,
            a_info.damage_f,
            a_info.damage_prize
        ],
        [
            a_info.items_id,
            a_info.item_title,
            a_info.item_description,
            a_info.items,
            a_info.item_f,
            a_info.item_prize
        ],
        [
            a_info.money_id,
            a_info.money_title,
            a_info.money_description,
            a_info.moneys,
            a_info.money_f,
            a_info.money_prize
        ]
    ]
    socketio.emit('achievement', achievement)
    
# ======================================================================================
@app.route("/")
def about():
    """ main page """
    return flask.render_template("landing_page.html")

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
    saveProgress()
    return flask.render_template("main_chat.html")
    

#=========================================================================================
@app.route("/options.html")
def options():
    """ main chat window """
    #saveProgress()
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
