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
    }
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

#________________________________________ANIMATION CONTROLLER OOP_____________________________________________

class AnimationController:
    def __init__(self, animations, animationSettings):
        """
        animations: 
        {
            'idle': {
                'frames': [ImageObject1, ImageObject2],
                'priority': 0,
                'loops': True
            },
        }

        animationSettings:
        {
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
        }

        """
        self.animationStack = []
        self.animations = animations
        self.animationSettings = animationSettings
        self.currentFrame = 0
        self.frameCounter  = 0
        self.currentAnimation =  None
    
    def _getPriority(self, animationName):
        #gets the priority of a specific animation
        if animationName in self.animationSettings:
            return animationSettings[animationName]["priority"]
        else:
            return defaultAnimationSettings["priority"]

    def sortAnimations(self):
        # sorts the animation from least to greatest priority. 
        # i am doing least to greatest so then i can pop an animation once its complete and have a O(1) time complexity
        self.animationStack.sort(key=self._getPriority, reverse=False)

    def cancelAnimation(self, animationName):
        #removes any animation that is in the animation stack. this is another reason i sorted the stack from least to greatest

        try:
            self.animationStack.remove(animationName)
        except ValueError:
            #print(f"attempt to cancel Animation {animationName} when it is not in the animation stack")
            pass

    def getTopAnimation(self):
        #returns the highest priority animation
        return self.animationStack[-1] if self.animationStack else None

    def cancelRunningAnimation(self):
        # removes the current running animation in the stack(The last element in the stack). Therefore i can do stack.pop()
        if self.animationStack:
            self.animationStack.pop()
        
    def addAnimToStack(self, animationName):
        if not (animationName in self.animations): return
        if animationName in self.animationStack: return

        self.animationStack.append(animationName)
        self.sortAnimations()

    def _resetForNewAnimation(self, newAnimation):
        self.currentAnimation = newAnimation
        self.currentFrame = 0
        self.frameCounter = 0

    def getAnimationFrame(self, app):
        if self.currentAnimation == None:
            return None
        
        animationFrames = self.animations[self.currentAnimation]["frames"]

        if self.currentFrame >= len(animationFrames):
            return animationFrames[-1]
        else:
            return animationFrames[self.currentFrame]
        
    def updateAnimation(self, app):
        # this function will change the animation information, BUT will not load any actual sprite animations

        currentHighest = self.getTopAnimation()

        if not currentHighest:
            self.currentAnimation = None
            return

        if self.currentAnimation != currentHighest:
            self._resetForNewAnimation(currentHighest)

        staticAnimData = self.animations[currentHighest]

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
                    self.cancelRunningAnimation()

spriteAnimations = loadAnimations("TermProject/SpriteAnimations")