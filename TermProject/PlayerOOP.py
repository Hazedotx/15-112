from cmu_graphics import *
from PIL import Image
import SpriteAnimations
import Config



class Player:
    def __init__(self, app):

        self.app = app
        
        self.type = "player"
        self.position = [app.width/2, app.height/2]
        self.isMoving = False
        self.keysPressed = set()
        self.facingDirection = "right"

        self.animationController = SpriteAnimations.AnimationController(SpriteAnimations.spriteAnimations["player"], SpriteAnimations.animationSettings["player"])

        # adding MKM here incase i have an enemy which disorients the player
        self.MOVEMENT_KEY_MAP = {
            "w": (0, -1),
            "s": (0, 1),
            "a": (-1, 0),
            "d": (1, 0)
        }

        self.movementSpeed = 60

        self.playerHitboxSize = {
            "width": app.width / 10,
            "height": app.height / 8
        }

        self.animationInfo = SpriteAnimations


    def movePlayer(self, keys):
        # will go through all the possible keys and then update the plr position based off of the keys pressed
        # will also update the player state "isMoving"
        speedRatio = (1 / self.app.stepsPerSecond) * self.movementSpeed

        for key in keys:
            if key in self.MOVEMENT_KEY_MAP:
                self.position[0] += self.MOVEMENT_KEY_MAP[key][0] * speedRatio
                self.position[1] += self.MOVEMENT_KEY_MAP[key][1] * speedRatio

    def teleportPlayer(self, newPosition):
        # will set the players position to a newPosition.

        self.position[0] = newPosition[0]
        self.position[1] = newPosition[1]

    def drawPlayer(self):
        # make sure to update this soon.
        animationFrame = self.animationController.getAnimationFrame(self.app)

        if animationFrame == None:
            print(animationFrame)
            return
        
        spriteImage = CMUImage(animationFrame if self.facingDirection == "right" else animationFrame.transpose(Image.FLIP_LEFT_RIGHT))

        drawImage(
            spriteImage,
            self.position[0],
            self.position[1],
            align = "center",
            width = self.playerHitboxSize["width"],
            height = self.playerHitboxSize["height"]
        )
    
    def keyPressedLogic(self, key):
        self.keysPressed.add(key)

    def keyReleasedLogic(self, key):
        self.keysPressed.discard(key)

    def keysHeldLogic(self,keys):

        self.movePlayer(keys)

        if "d" in keys:
            self.facingDirection = "right"
        elif "a" in keys:
            self.facingDirection = "left"

        pass

    def movementKeyPressed(self):
        #checks if any movement keys are being held down so I can tell which animation to run
        for key in self.MOVEMENT_KEY_MAP:
            if key in self.keysPressed:
                return True

        return False
    
    def runPlayerLogic(self):
        """
        data = {}
        """

        #this function will handle player data updating
        #anything that should ever happen to the player should run through here
        #draw functions will not be ran through here. only logic which affects data
        #function will run according to what "data" parameter has in it

        self.isMoving = self.movementKeyPressed()

        self.animationController.updateAnimation(self.app)
        self.animationController.addAnimToStack("idle")

        if self.isMoving:
            self.animationController.addAnimToStack("run")
        else:
            self.animationController.cancelAnimation("run")


    pass