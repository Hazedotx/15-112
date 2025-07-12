from cmu_graphics import *
import Helper
import copy
import random

SCREEN_WIDTH, SCREEN_HEIGHT = Helper.grabScreenDimensions()

def onAppStart(app):

    app.settings = {
        ["screenDimensions"] : {
            "width" : app.width, 
            "height" : app.height
        }
    }


    pass
    
def redrawAll(app):
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