from cmu_graphics import *

import Helper
import SpriteAnimations
import Config

import EntityLogic.Player as Player
import EntityLogic.Skeleton1 as Skeleton1
import WeaponLogic.Sword as Sword

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

    app.player = Player.Player(app)
    app.skeleton = Skeleton1.Skeleton(app, [app.width/2 - 150, app.height/2])
    app.playerSword = Sword.Sword(app)

    app.allEntities = { #entities are anything which have custom logic/behavior built into them.
        "Enemies": set(),
        "Players": set(),
        "NonLiving": set()
    }

    app.allEntities["Enemies"].add(app.skeleton)
    app.allEntities["Players"].add(app.player)
    app.allEntities["NonLiving"].add(app.playerSword)

    applySettings(app)


    pass

def updateEntities(functionName):
    for entityList in app.allEntities:
        for entity in entityList:
            possibleMethod = getattr(entity, functionName, None)
            if callable(possibleMethod):
                possibleMethod()

    
def redrawAll(app):

    drawRect(app.width/2, app.height/2, app.width, app.height, align = "center", fill = "grey")

    #drawRect(app.player.position[0],app.player.position[1], app.player.playerHitboxSize["width"],app.player.playerHitboxSize["height"], fill = None, border = "black", align = "center")
    #app.player.drawPlayer()
    #app.skeleton.drawSkeleton()

    updateEntities("draw")

    pass

def onStep(app):
    app.globalStates["totalTicks"] += 1
    #app.player.runPlayerLogic()
    #app.skeleton.runSkeletonLogic()

    updateEntities("runLogic")









#_________________________________________KEY EVENTS____________________________________________
def onKeyPress(app,key):
    app.player.keyPressedLogic(key)
    pass

def onKeyRelease(app,key):
    app.player.keyReleasedLogic(key)
    pass

def onKeyHold(app,keys):
    app.player.keysHeldLogic(keys)
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