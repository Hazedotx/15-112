from cmu_graphics import *
import Helper
import copy
import random

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
        }
    }

    app.playerSettings = {
        "fullScreenEnabled": False,
        "fps": 60
    }

    app.playerState = {
        "position": (None, None)
    }


    pass
    
def redrawAll(app):

    drawRect(app.width/2, app.height/2, app.width, app.height, align = "center", fill = "grey")

    pass

#_________________________________________KEY EVENTS____________________________________________
def onKeyPress(app,key):
    pass

def onKeyRelease(app,key):
    pass

def onKeyHold(app,keys):
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
    runApp(width = SCREEN_WIDTH, height = SCREEN_HEIGHT)

main()