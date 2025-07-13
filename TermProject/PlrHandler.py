from cmu_graphics import *
from PIL import Image
import SpriteAnimations


MOVEMENT_KEY_MAP = {
    "w": (0, -1),
    "s": (0, 1),
    "a": (-1, 0),
    "d": (1, 0)
}

def movePlayer(app, keys):
    # will go through all the possible keys and then update the plr position based off of the keys pressed
    # will also update the player state "isMoving"
    speedRatio = (1 / app.stepsPerSecond) * app.player["movementSpeed"]

    for key in keys:
        if key in MOVEMENT_KEY_MAP:
            app.player["position"][0] += MOVEMENT_KEY_MAP[key][0] * speedRatio
            app.player["position"][1] += MOVEMENT_KEY_MAP[key][1] * speedRatio




def teleportPlayer(app, newPosition):
    # will set the players position to a newPosition.

    app.player["position"][0] = newPosition[0]
    app.player["position"][1] = newPosition[1]


def drawPlayer(app):
    animationFrame = SpriteAnimations.getAnimationFrame(app,app.player)

    if animationFrame == None:
        print(animationFrame)
        return
    
    spriteImage = CMUImage(animationFrame if app.player["facingDirection"] == "right" else animationFrame.transpose(Image.FLIP_LEFT_RIGHT))

    drawImage(
        spriteImage,
        app.player["position"][0],
        app.player["position"][1],
        align = "center",
        width = app.player["playerHitboxSize"]["width"],
        height = app.player["playerHitboxSize"]["height"]
    )

def keyPressedLogic(app, key):
    app.player["keysPressed"].add(key)


def keyReleasedLogic(app, key):
    app.player["keysPressed"].discard(key)

def keysHeldLogic(app,keys):

    movePlayer(app,keys)

    if "d" in keys:
        app.player["facingDirection"] = "right"
    elif "a" in keys:
        app.player["facingDirection"] = "left"

    pass

def movementKeyPressed(app):
    #checks if any movement keys are being held down so I can tell which animation to run
    keysPressed = app.player["keysPressed"]

    for key in MOVEMENT_KEY_MAP:
        if key in keysPressed:
            return True

    return False

def runPlayerLogic(app, data):
    """
    data = {}
    """

    #this function will handle player data updating
    #anything that should ever happen to the player should run through here
    #draw functions will not be ran through here. only logic which affects data
    #function will run according to what "data" parameter has in it

    app.player["isMoving"] = movementKeyPressed(app)


    SpriteAnimations.updateAnimation(app,app.player)
    SpriteAnimations.addAnimToStack(app, app.player, "idle")

    if app.player["isMoving"]:
        SpriteAnimations.addAnimToStack(app, app.player, "run")
    else:
        SpriteAnimations.cancelAnimation(app, app.player, "run")



 

