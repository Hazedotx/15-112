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
    moved = False
    for key in keys:
        if key in MOVEMENT_KEY_MAP:
            moved = True
            app.player["position"][0] += MOVEMENT_KEY_MAP[key][0] * speedRatio
            app.player["position"][1] += MOVEMENT_KEY_MAP[key][1] * speedRatio

    app.player["isMoving"] = moved

    pass

def teleportPlayer(app, newPosition):
    # will set the players position to a newPosition.

    app.player["position"][0] = newPosition[0]
    app.player["position"][1] = newPosition[1]


def drawPlayer(app):
    animationFrame = SpriteAnimations.getAnimationFrame(app,app.player)

    if animationFrame == None:
        print(animationFrame)
        return
    
    spriteImage = CMUImage(animationFrame)

    drawImage(
        spriteImage,
        app.player["position"][0],
        app.player["position"][1],
        align = "center",
        width = app.player["playerHitboxSize"]["width"],
        height = app.player["playerHitboxSize"]["height"]
    )

def runStepLogic(app):

    pass

def runPlayerLogic(app, data):
    """
    data = {}
    """

    #this function will handle player data updating
    #anything that should ever happen to the player should run through here
    #draw functions will not be ran through here. only logic which affects data
    #function will run according to what "data" parameter has in it

    SpriteAnimations.updateAnimation(app,app.player)
    SpriteAnimations.addAnimToStack(app, app.player, "idle")

    if app.player["isMoving"]:
        #SpriteAnimations.addAnimToStack(app, app.player, "run")
        pass




