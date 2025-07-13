from cmu_graphics import *
from PIL import Image

import os
import pprint
import copy

defaultAnimationSettings = {
    'loops': False,
    'priority': 1
}

animationSettings = {
    "idle": {
        'loops': True,
        'priority': 1
    }
}


def loadAnimations(rootFolder):
    """
    should return sm like this 
    {
        Player: {
            'idle': {
                'frames': [ImageObject1, ImageObject2],
                'priority': 0,
                'loops': True
            },
        }
    }
    """


    animations = {}

    for dirPath, dirNames, fileNames in os.walk(rootFolder):
        fileNames.sort()
        pngFiles = [f for f in fileNames if f.endswith('.png')]

        if not pngFiles:
            continue

        animationName = os.path.basename(dirPath).lower()
        frames = []
        for fileName in pngFiles:
            fullPath = os.path.join(dirPath, fileName)
            image = Image.open(fullPath)
            frames.append(image)

        #Logic for building final components.

        parentFileName = os.path.basename(os.path.dirname(dirPath)).lower()
        animationInformation = animationSettings[animationName] if animationName in animationSettings else copy.deepcopy(defaultAnimationSettings)


        if not (parentFileName in animations):
            animations[parentFileName] = {}
        animations[parentFileName][animationName] = {}

        for key in defaultAnimationSettings:
            value = defaultAnimationSettings[key]
            animations[parentFileName][animationName][key] = animationInformation[key] if (key in animationInformation) else value

        animations[parentFileName][animationName]["frames"] = frames

    return animations

#__________________________________ANIMATION CONTROLLER BASE FUNCTIONS_______________________________________________

def sortAnimationCondition(animationName):
    return animationSettings[animationName]["priority"] if animationName in animationSettings else defaultAnimationSettings["priority"]
    
def sortAnimations(entity):
    # sorts from greatest to least animation priority
    entity["animationInfo"].sort(key = sortAnimationCondition, reversed = True)


def cancelAnimation(entity, animationName):
    #cancels any animation that is currently in the animation stack. animation doesnt have to be running for it to be canceled.
    stack = entity["animationInfo"]["animationStack"]

    try:
        stack.remove(animationName)
        sortAnimations(entity)
    except ValueError:
        print(f"attempt to cancel Animation {animationName} when it is not in the animation stack")
        pass


def cancelRunningAnimation(entity, animationName):
    #cancels whatever animation is currently running(highest priority)
    if len(entity["animationInfo"]["animationStack"]) > 0:
        entity["animationInfo"]["animationStack"].pop()

def addAnimToStack(app, entity, animationName):

    #check if animation keyframes exist.
        # if they dont exist, return False and provide an error
        #if they exist, then add the animation name to the stack 

    entityType = entity["type"]
    stack = entity["animationInfo"]["animationStack"]

    if not (entityType in app.staticInfo["spriteAnimations"]): return False
    if not (animationName in app.staticInfo["spriteAnimations"][entityType]): return False
    if animationName in stack: return False

    stack.append(animationName)
    sortAnimations(entity)


def getPriorityAnimation(entity):
    #returns the higest priority animation
    sortAnimations(entity) # this may not be nessecary later if i change my code up a bit. 
    stack = entity["animationInfo"]["animationStack"]
    return stack[0] if stack else None

def resetAnimationInfo(entity):
    entity["animationInfo"]["animationStack"]["currentFrame"] = 0
    entity["animationInfo"]["animationStack"]["currentAnimation"] = None

#__________________________________ANIMATION CONTROLLER COMBINED FUNCTIONS_______________________________________________
# These functions will put together all the other functions and make it easy for entity logic to utilize the animation controller




pprint.pp(loadAnimations("TermProject/SpriteAnimations"))