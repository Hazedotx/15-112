from cmu_graphics import *
from PIL import Image


MOVEMENT_KEY_MAP = {
    "w": (0, -1),
    "s": (0, 1),
    "a": (-1, 0),
    "d": (1, 0)
}

def movePlayer(app, keys):
    # will go through all the possible keys and then update the plr position based off of the keys pressed
    speedRatio = (1 / app.stepsPerSecond) * app.player["movementSpeed"]
    for key in keys:
        if key in MOVEMENT_KEY_MAP:

            app.player["position"][0] += MOVEMENT_KEY_MAP[key][0] * speedRatio
            app.player["position"][1] += MOVEMENT_KEY_MAP[key][1] * speedRatio


    pass

def teleportPlayer(app, newPosition):
    # will set the players position to a newPosition.

    app.player["position"][0] = newPosition[0]
    app.player["position"][1] = newPosition[1]


def drawPlayer(app):
    animationInfo = app.player["animationInfo"]
    currentAnimationName = animationInfo["currentAnimation"]
    animationFrames = app.staticInfo["spriteAnimations"][currentAnimationName]


    spriteImage = CMUImage(animationFrames[animationInfo["currentFrame"]])

    drawImage(
        spriteImage,
        app.player["position"][0],
        app.player["position"][1],
        align = "center",
        width = app.player["playerHitboxSize"]["width"],
        height = app.player["playerHitboxSize"]["height"]
    )


    pass

def updateAnimations(app):

    

    pass