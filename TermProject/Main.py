from cmu_graphics import *

import Helper
import PlrHandler
import SpriteAnimations
import EntityHandler

import copy
import random

#pip install pillow

SCREEN_WIDTH, SCREEN_HEIGHT = Helper.grabScreenDimensions()

def applySettings(app):

    if app.playerSettings["fullScreenEnabled"]:
        app.width = SCREEN_WIDTH
        app.height = SCREEN_HEIGHT
    
    app.stepsPerSecond = app.playerSettings["fps"]

    pass

def onAppStart(app):

    app.staticInfo = {
        "fullScreenDimensions" : {
            "width" : SCREEN_WIDTH, 
            "height" : SCREEN_HEIGHT
        },

        "spriteAnimations": SpriteAnimations.loadAnimations("TermProject/SpriteAnimations")
    }

    app.playerSettings = {
        "fullScreenEnabled": False,
        "fps": 60
    }

    app.globalStates = {
        "totalTicks": 0
    }

    app.player = EntityHandler.createEntity(app,"player",app.width/2,app.height/2)


    applySettings(app)


    pass
    
def redrawAll(app):

    drawRect(app.width/2, app.height/2, app.width, app.height, align = "center", fill = "grey")

    drawRect(app.player["position"][0],app.player["position"][1], app.player["playerHitboxSize"]["width"],app.player["playerHitboxSize"]["height"], fill = None, border = "black", align = "center")
    PlrHandler.drawPlayer(app)

    pass

def onStep(app):
    app.globalStates["totalTicks"] += 1
    PlrHandler.runPlayerLogic(app,None)




#_________________________________________KEY EVENTS____________________________________________
def onKeyPress(app,key):
    PlrHandler.keyPressedLogic(app,key)
    pass

def onKeyRelease(app,key):
    PlrHandler.keyReleasedLogic(app,key)
    pass

def onKeyHold(app,keys):
    PlrHandler.keysHeldLogic(app,keys)
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