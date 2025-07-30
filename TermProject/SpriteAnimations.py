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
            "framesPerSecond":8 
        },
        "run": {
            'loops': True,
            'priority': 2,
            "framesPerSecond":8
        }
    },

    "skeleton": {
        "idle": {
            'loops': True,
            'priority': 1,
            "framesPerSecond":8 
        },
        "walk": {
            'loops': True,
            'priority': 2,
            "framesPerSecond":8
        },
        "damage": {
            'loops': False,
            'priority': 3,
            "framesPerSecond":8
        },

        "attack": {
            'loops': False,
            'priority': 4,
            "framesPerSecond":8 
        },
        "death": {
            'loops': False,
            'priority': 5,
            "framesPerSecond":8
        },
    },

    "sword": {
        "default": {
            'loops': True,
            'priority': 1,
            'framesPerSecond': 1
        }
    },

    "axe": {
        "default": {
            'loops': True,
            'priority': 1,
            'framesPerSecond': 1
        }
    },

    "bighammer": {
        "default": {
            'loops': True,
            'priority': 1,
            'framesPerSecond': 1
        }
    },


}

spriteAnimations = None

# TO DO:
#turn the animation controller into objects. each animation controller will hold the animations that 
#want to be played for that entities specific animation


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


    #I used chat gpt to figure out how to navigate folders and stuff. I look at the os libary as well

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
spriteAnimations = loadAnimations("TermProject/SpriteAnimations")

#________________________________________ANIMATION CONTROLLER OOP_____________________________________________

class AnimationController:
    # Animation controller inspired by some of the stuff I have made in roblox studio.
    def __init__(self, animations, animationSettings):
        self.animationStack = []
        self.animations = animations
        self.animationSettings = animationSettings
        self.currentFrame = 0
        self.frameCounter  = 0
        self.currentAnimation = None
    
    def getPriority(self, animationObject):
        animationName = animationObject['name']

        if animationName in self.animationSettings:

            return self.animationSettings[animationName]["priority"]
        else:
            return defaultAnimationSettings["priority"]

    def sortAnimations(self):
        # sorts the animation based off the priority
        self.animationStack.sort(key=self.getPriority, reverse=False)

    def cancelAnimation(self, animationName):
        # removes the animation from the animation stack 
        self.animationStack = [anim for anim in self.animationStack if anim['name'] != animationName]



    def getTopAnimation(self):
        #returns the highest priority animation
        return self.animationStack[-1] if self.animationStack else None

    def cancelRunningAnimation(self):
        if self.animationStack:
            self.animationStack.pop()
        
    def addAnimToStack(self, animationName):
        if not (animationName in self.animations): return
        if any(anim['name'] == animationName for anim in self.animationStack): return

        self.animationStack.append({
            'name': animationName,
            'onComplete': None
        })
        self.sortAnimations()
        
    def playAnimationOnce(self, animationName, onComplete=None):
        if not (animationName in self.animations): return
        
        self.animationStack.append({
            'name': animationName,
            'onComplete': onComplete
        })
        self.sortAnimations()

    def resetForNewAnimation(self, newAnimation):
        # resets the animation info 
        self.currentAnimation = newAnimation
        self.currentFrame = 0
        self.frameCounter = 0

    def getAnimationFrame(self, app):
        # gets the current animation frame 
        if self.currentAnimation == None:
            return None
        
        animationName = self.currentAnimation['name']
        animationFrames = self.animations[animationName]["frames"]

        if self.currentFrame >= len(animationFrames):
            return animationFrames[-1]
        else:
            return animationFrames[self.currentFrame]
        
    def updateAnimation(self, app):
        # updates the current animation that is running. 
        currentHighest = self.getTopAnimation()

        if not currentHighest:
            self.currentAnimation = None
            return

        if self.currentAnimation != currentHighest:
            self._resetForNewAnimation(currentHighest)

        currentAnimationName = self.currentAnimation['name']
        staticAnimData = self.animations[currentAnimationName]

        self.frameCounter += 1
        
        stepsPerFrame = app.stepsPerSecond // staticAnimData["framesPerSecond"]
        if stepsPerFrame < 1:
            stepsPerFrame = 1

        if self.frameCounter >= stepsPerFrame:
            self.frameCounter = 0
            self.currentFrame += 1

            if self.currentFrame >= len(staticAnimData["frames"]):
                if staticAnimData.get("loops", False):
                    self.currentFrame = 0
                else:
                    # run the callback in order to clean up anything the sprite has after the animation finifhes
                    callback = self.currentAnimation.get('onComplete')
                    if callback:
                        callback()
                    self.cancelRunningAnimation()