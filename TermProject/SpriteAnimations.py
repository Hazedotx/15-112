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
    def __init__(self, entity):
        self.entity = entity
        self.entityName = entity["type"]
        self.animationStack = []
        self.currentFrame = 0
        self.frameCounter  = 0
        self.currentAnimation =  None
    
    def _getPriority(self, animationName):
        #gets the priority of a specific animation
        if self.entityName in animationSettings and animationName in animationSettings[self.entityName]:
            return animationSettings[self.entityName][animationName]["priority"]
        return defaultAnimationSettings["priority"]

    def sortAnimations(self):
        # sorts the animation from least to greatest priority. 
        # i am doing least to greatest so then i can pop an animation once its complete and have a O(1) time complexity

        if not self.entityName in animationSettings:
            print(f"Entity Name: {self.entityName} was not found in animationSettings") 
            return
        
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
        
    def addAnimToStack(self, app, animationName):
        if not (self.entityName in app.staticInfo["spriteAnimations"]): return False
        if not (animationName in app.staticInfo["spriteAnimations"][self.entityName]): return False
        if animationName in self.animationStack: return False

        self.animationStack.append(animationName)
        self.sortAnimations()

    def _resetForNewAnimation(self, newAnimation):
        self.currentAnimation = newAnimation
        self.currentFrame = 0
        self.frameCounter = 0

    def getAnimationFrame(self, app):
        if self.currentAnimation == None:
            return None
        
        animationFrames = app.staticInfo["spriteAnimations"][self.entityName][self.currentAnimation]["frames"]

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

        staticAnimData = app.staticInfo["spriteAnimations"][self.entityName][currentHighest]

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



#pprint.pp(loadAnimations("TermProject/SpriteAnimations"))