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
    "knightidle": {
        'loops': True,
        'priority': True
    }
}


def loadAnimations(rootFolder):
    """
    should return sm like this 
    {
        'knightidle': {
            'frames': [ImageObject1, ImageObject2],
            'priority': 0,
            'loops': True
        },
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


def cancelAnimation(entity, animationName):

    animationIndex = entity["animationInfo"]["animationStack"].index(animationName)

    if animationIndex != -1:
        entity["animationInfo"]["animationStack"].pop(animationIndex)


def addAnimToStack(entity, animationName):

    #check if animation keyframes exist.
        # if they dont exist, return False and provide an error
        #if they exist, then add the animation name to the stack 

    animationIndex = entity["animationInfo"]["animationStack"].index(animationName)

    if animationIndex != -1:
        entity["animationInfo"]["animationStack"].append(animationName)

    
def sortAnimations(entity):

    # sort the animations based off the priority found when indexing animationSettings. 

    pass

def getPriorityAnimation(entity):




    pass
    

def resetAnimationInfo(entity):
    entity["animationInfo"]["animationStack"]["currentFrame"] = 0
    entity["animationInfo"]["animationStack"]["currentAnimation"] = None


pprint.pp(loadAnimations("TermProject/SpriteAnimations"))