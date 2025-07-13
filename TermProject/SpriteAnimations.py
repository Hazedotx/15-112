from cmu_graphics import *
from PIL import Image

import os
import pprint
import copy

defaultAnimationSettings = {
    'loops': False,
    'priority': 1,
    "framesPerSecond": 10
}

animationSettings = {

    "player": {
        "idle": {
            'loops': True,
            'priority': 1,
            "framesPerSecond": 4
        }
    }
}
# TO DO:
# this current animation Settings set up wont work when i scale up the amount of entities there will be. naming will be diffucltl
# make sure to group the animations based off the entity it is for.


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
        animationInformation = animationSettings[parentFileName][animationName] if animationName in animationSettings[parentFileName] else copy.deepcopy(defaultAnimationSettings)


        if not (parentFileName in animations):
            animations[parentFileName] = {}
        animations[parentFileName][animationName] = {}

        for key in defaultAnimationSettings:
            value = defaultAnimationSettings[key]
            animations[parentFileName][animationName][key] = animationInformation[key] if (key in animationInformation) else value

        animations[parentFileName][animationName]["frames"] = frames

    return animations

#__________________________________ANIMATION CONTROLLER BASE FUNCTIONS_______________________________________________


    
def sortAnimations(app, entity):
    # sorts from greatest to least animation priority
    entityName = entity["type"]

    def sortAnimationCondition(animationName):
        if not entityName in animationSettings:
            print(f"Entity Name: {entityName} was not found in animationSettings") 
            return 0
        
        return animationSettings[entityName][animationName]["priority"] if animationName in animationSettings[entityName] else defaultAnimationSettings["priority"]

    entity["animationInfo"]["animationStack"].sort(key = sortAnimationCondition, reversed = True)


def cancelAnimation(entity, animationName):
    #cancels any animation that is currently in the animation stack. animation doesnt have to be running for it to be canceled.
    stack = entity["animationInfo"]["animationStack"]

    try:
        stack.remove(animationName)
    except ValueError:
        print(f"attempt to cancel Animation {animationName} when it is not in the animation stack")
        pass


def cancelRunningAnimation(entity, animationName):
    #cancels whatever animation is currently running(highest priority)
    stack = entity["animationInfo"]["animationStack"]
    if stack: #this checks if the list has an element in it.
        stack.pop(0)

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
    sortAnimations(app, entity)


def getTopAnimation(entity):
    #returns the higest priority animation
    stack = entity["animationInfo"]["animationStack"]
    return stack[0] if stack else None

def resetAnimationInfo(entity, newAnimation):
    stack = entity["animationInfo"]
    stack["currentFrame"] = 0
    stack["frameCounter"] = 0
    stack["currentAnimation"] = newAnimation

#__________________________________ANIMATION CONTROLLER COMBINED FUNCTIONS_______________________________________________
# These functions will put together all the other functions and make it easy for entity logic to utilize the animation controller


def updateAnimation(app, entity):
    # this function will serve as the core logic loop for an entities animation
    # this function will change the animation information, BUT will not load any actual sprite animations

    #Logic:
        #get the current higest priority animation
        #check if this animation is still the same or a new animation
            #if the new animation is the highest, we will have to reset the current animation information to reset the current animation Info

        #we will then update the current animation frames accordingly.
            #


    animationInfo = entity["animationInfo"]
    currentHighest = getTopAnimation(entity)

    if not currentHighest:
        animationInfo["currentAnimation"] = None
        return

    if animationInfo["currentAnimation"] != currentHighest:
        resetAnimationInfo(entity, currentHighest)

    print(f"Current Highest: {currentHighest}")

    staticAnimData = app.staticInfo["spriteAnimations"][entity["type"]][currentHighest]

    animationInfo["frameCounter"] += 1

    stepsPerFrame = app.stepsPerSecond // staticAnimData["framesPerSecond"]

    if animationInfo["frameCounter"] >= stepsPerFrame:
        animationInfo["frameCounter"] = 0
        animationInfo["currentFrame"] += 1

        if animationInfo["currentFrame"] >= len(staticAnimData["frames"]):
            if animationInfo["loops"]:
                animationInfo["currentFrame"] = 0
        else:
            cancelAnimation(entity, animationInfo["currentAnimation"])

def getAnimationFrame(app, entity):
    #This function will return the current animation frame the entity is on (the image)
    

    entityName = entity["type"]
    animationInfo = entity["animationInfo"]
    currentAnimation = animationInfo["currentAnimation"]

    if currentAnimation == None: 
        return None

    currentFrame = animationInfo["currentFrame"]
    animationFrames = app.staticInfo["spriteAnimations"][entityName][currentAnimation]["frames"]

    if currentFrame >= len(animationFrames):
        return animationFrames[-1]
    else:
        return animationFrames[currentFrame]



#pprint.pp(loadAnimations("TermProject/SpriteAnimations"))