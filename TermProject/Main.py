from cmu_graphics import *

import Helper
import SpriteAnimations
import Config
import DungeonGen

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

    app.dungeonGenerator = DungeonGen.DungeonGenerator(
        app,
        Config.STATIC_INFO["DungeonConfig"]["gridHeight"], 
        Config.STATIC_INFO["DungeonConfig"]["gridWidth"]
    )

    app.dungeonGenerator.generate()
    app.dungeonGenerator.convertDungeonToImage()
    
    app.player = Player.Player(app)
    app.skeleton = Skeleton1.Skeleton(app, [app.width/2 - 150, app.height/2])
    app.playerSword = Sword.Sword(app)

    app.allEntities = { #entities are anything which have custom logic/behavior built into them.
        "enemies": set(),
        "players": set(),
        "nonLiving": set()
    }

    app.gcEntities = {
        "enemies": set(),
        "players": set(),
        "nonLiving": set()
    }

    app.allEntities["enemies"].add(app.skeleton)
    app.allEntities["players"].add(app.player)
    app.allEntities["nonLiving"].add(app.playerSword)

    applySettings(app)


    pass

def gcEntities(app):
    # garbage collects entities after the entity logic is all completed.
    for EntityType in app.gcEntities:
        for entity in app.gcEntities[EntityType]:
            app.allEntities[EntityType].remove(entity)
        app.gcEntities[EntityType].clear()

def updateEntities(app, functionName, Params = None):
    # params will be a list which gets unpacked and passed
    for entitySetName in app.allEntities:
        for entity in app.allEntities[entitySetName]:
            possibleMethod = getattr(entity, functionName, None)
            if callable(possibleMethod) and Params != None:
                possibleMethod(*Params)
            elif callable(possibleMethod):
                possibleMethod()

    
def redrawAll(app):

    drawRect(app.width/2, app.height/2, app.width, app.height, align = "center", fill = "grey")

    #drawRect(app.player.position[0],app.player.position[1], app.player.playerHitboxSize["width"],app.player.playerHitboxSize["height"], fill = None, border = "black", align = "center")
    #app.player.drawPlayer()
    #app.skeleton.drawSkeleton()

    app.dungeonGenerator.draw()
    updateEntities(app, "draw")

    pass

def onStep(app):
    app.globalStates["totalTicks"] += 1
    #app.player.runPlayerLogic()
    #app.skeleton.runSkeletonLogic()

    updateEntities(app, "runLogic")
    gcEntities(app)









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
    updateEntities(app, "onMouseMove", [mouseX, mouseY])
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