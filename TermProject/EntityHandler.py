from cmu_graphics import *

import copy

def InitAnimationInfo():
    return (
        {
        "animationStack": [],
        "currentFrame": 0,
        "frameCounter": 0,
        "currentAnimation": None
        }
        )


def InitPlayer(app, xPos, yPos):
    return {
        "type": "player",
        "position": [app.width/2, app.height/2],
        "isMoving": False,

        "movementSpeed": 60, # pixels per second

        "playerHitboxSize":{
            "width": 45,  # pixels
            "height": 45
        },

        "animationInfo": InitAnimationInfo()
    }

entitySpecificInfo = {
    "player": InitPlayer
}

def createEntity(app, entityType, xPos, yPos):
    return entitySpecificInfo[entityType](app,xPos,yPos)