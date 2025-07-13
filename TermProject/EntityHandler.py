from cmu_graphics import *

import copy


def InitPlayer(app, xPos, yPos):
    return {
        "type": "player",
        "position": [app.width/2, app.height/2],

        "movementSpeed": 60, # pixels per second

        "playerHitboxSize":{
            "width": 45,  # pixels
            "height": 45
        },

        "animationInfo": {
            "animationStack": [],
            "currentFrame": 0,
            "currentAnimation": None
        }
    }

entitySpecificInfo = {
    "player": InitPlayer
}

def createEntity(app, entityType, xPos, yPos):
    return entitySpecificInfo[entityType](app,xPos,yPos)