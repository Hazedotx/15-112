from cmu_graphics import *

import Helper
import SpriteAnimations
import EntityHandler
import Config
import PlayerOOP

import copy
import random

from SpriteAnimations import spriteAnimations as spriteAnimations

#pip install pillow

def applySettings(app):

    if Config.SETTINGS["fullScreenEnabled"]:
        app.width = Config.SCREEN_WIDTH
        app.height = Config.SCREEN_HEIGHT
    
    app.stepsPerSecond = Config.SETTINGS["fps"]

    pass

def onAppStart(app):

    app.globalStates = {
        "totalTicks": 0
    }

    app.player = PlayerOOP.Player(app)

    applySettings(app)


    pass
    
def redrawAll(app):

    drawRect(app.width/2, app.height/2, app.width, app.height, align = "center", fill = "grey")

    drawRect(app.player["position"][0],app.player["position"][1], app.player["playerHitboxSize"]["width"],app.player["playerHitboxSize"]["height"], fill = None, border = "black", align = "center")
    app.player.drawPlayer(app)

    pass

def onStep(app):
    app.globalStates["totalTicks"] += 1
    app.player.runPlayerLogic(app,None)




#_________________________________________KEY EVENTS____________________________________________
def onKeyPress(app,key):
    app.player.keyPressedLogic(app,key)
    pass

def onKeyRelease(app,key):
    app.player.keyReleasedLogic(app,key)
    pass

def onKeyHold(app,keys):
    app.player.keysHeldLogic(app,keys)
    pass

#_________________________________________MOUSE EVENTS____________________________________________

def onMouseMove(app,mouseX,mouseY):
    pass

def onMousePress(app, mouseX, mouseY):
    pass

def onMouseDrag(app, mouseX, mouseY):
    pass

def onMouseRelease(app, mouseX, mouseY):
    pass

#________________________________________INITALIZE GAME____________________________________________

def main():
    runApp()

main()