"""
    Handles the game logic
"""
import inspect
import os
import sys
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from progress import save_progress, load_progress
# local imports
from .game_io import prompt_in, send_out
from .scenario import scenario, start_scenario

# COMBAT COMBAT COMBAT
def combat(player, enemy):
    """ Simulates combat between the player and the enemy """
    send_out("Player " + player.id + " begins combat with " + enemy.id)
    send_out(
        "Player "
        + player.id
        + " starts at "
        + str(player.health)
        + "/"
        + str(player.max_health)
    )
    send_out(
        "Player "
        + enemy.id
        + " starts at "
        + str(enemy.health)
        + "/"
        + str(enemy.max_health)
    )
    while not player.is_dead() and not enemy.is_dead():
        # Prompt player aciton
        action = prompt_in()
        # Determine faster speed, Pokemon style
        if enemy.speed > player.speed:
            # Enemies go first
            send_out(enemy.attack("melee", player))
            if "attack" in action:
                send_out(player.attack("melee", enemy))
            else:
                continue  # we don't handle other actions right now
        else:
            # players go first
            if "attack" in action:
                send_out(player.attack("melee", enemy))
                send_out(enemy.attack("melee", player))
            else:
                continue  # we don't handle other actions right now
    winner = player.id
    if player.is_dead():
        winner = enemy.id
    send_out("Combat has ended! " + winner + " has won!")


def game(userlist, char_name):
    """ Runs the game, given a user """
    # try to load progress, otherwise start scenario
    player = load_progress(userlist, char_name) #unsure if im calling this right
    if(player != None):
        state_tuple = (player, player.checkpoint)
    else:
        # player character
        player = start_scenario(userlist[-1])
        save_progress([player])  # move to within the game
        # this tuple is shaped: "Player, String" where string is the area
        state_tuple = scenario(player, "intro")
    while state_tuple[1] != "end":
        save_progress([state_tuple[0]])
        state_tuple = scenario(state_tuple[0], state_tuple[1])
    print("game has reached endstate")
    return
