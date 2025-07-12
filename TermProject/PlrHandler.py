from cmu_graphics import *


MOVEMENT_KEY_MAP = {
    "w": (0, -1),
    "s": (0, 1),
    "a": (-1, 0),
    "d": (1, 0)
}

def movePlayer(app, keys):
    # will go through all the possible keys and then update the plr position based off of the keys pressed

    for key in keys:
        if MOVEMENT_KEY_MAP[key] != None:
            app.playerState["position"][0] += MOVEMENT_KEY_MAP[key][0]
            app.playerState["position"][1] += MOVEMENT_KEY_MAP[key][1]


    pass

def teleportPlayer(app, newPosition):
    # will set the players position to a newPosition.

    app.playerState["position"][0] = newPosition[0]
    app.playerState["position"][1] = newPosition[1]

    

    pass