from cmu_graphics import *
from PIL import Image
import SpriteAnimations
import HealthBarOOP
import Config
import uuid


class Player:
    def __init__(self, app):

        self.id = uuid.uuid4()

        self.app = app
        
        self.type = "player"
        self.position = [app.width/2, app.height/2]
        self.isMoving = False
        self.keysPressed = set()
        self.facingDirection = "right"

        self.HealthBar = HealthBarOOP.HealthBar(self.app,self)
        self.health = 100
        self.maxHealth = 100

        self.playerHotbar = [] # this will be the player inventory
        self.currentItem = None
        self.currentItemIndex = -1

        self.app.allEntities["players"].add(self)

        self.animationController = SpriteAnimations.AnimationController(SpriteAnimations.spriteAnimations["player"], SpriteAnimations.animationSettings["player"])

        # adding MKM here incase i have an enemy which disorients the player
        self.MOVEMENT_KEY_MAP = {
            "w": (0, -1),
            "s": (0, 1),
            "a": (-1, 0),
            "d": (1, 0)
        }

        self.movementSpeed = 120

        self.visualHitboxSize = {
            "width": 50,
            "height": 70
        }

        self.hitboxSize = {
            "width": 50 * 1,
            "height": 70 * 1
        }



        self.animationInfo = SpriteAnimations

        self.changePlayerState("InitalizePlayer")

    def __eq__(self, other):
        if not isinstance(other, Player): return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)


    def movePlayer(self, keys):
        # will go through all the possible keys and then update the plr position based off of the keys pressed
        # will also update the player state "isMoving"
        speedRatio = (1 / self.app.stepsPerSecond) * self.movementSpeed

        dx = 0
        dy = 0

        for key in keys:
            if key in self.MOVEMENT_KEY_MAP:
                dx += self.MOVEMENT_KEY_MAP[key][0]
                dy += self.MOVEMENT_KEY_MAP[key][1]

        newX, newY = self.position[0] + dx * speedRatio, self.position[1] + dy * speedRatio
        dungeonArena = self.app.dungeonManager.activeDungeonArena

        if dungeonArena != None and dungeonArena.enabled == True and dungeonArena.dungeon != None:
            if dungeonArena.dungeon.isPositionValid(self, (newX, newY)):
                self.position[0] = newX
                self.position[1] = newY
            elif dungeonArena.dungeon.isPositionValid(self, (self.position[0], newY)):
                self.position[1] = newY
            elif dungeonArena.dungeon.isPositionValid(self, (newX, self.position[1])):
                self.position[0] = newX



    def teleportPlayer(self, newPosition):
        # will set the players position to a newPosition.

        self.position[0] = newPosition[0] + self.visualHitboxSize["width"] / 2 - 7 # - 7 is bc of the non visible hitbox increasing the size of the width so it looks off
        self.position[1] = newPosition[1]

    def changePlayerState(self, newState):
        if newState == "InitalizePlayer":
            self.movementSpeed = 0
        elif newState == "ArenaInProgress":
            self.movementSpeed = 120
        elif newState == "ArenaFinished":
            self.movementSpeed = 0

    def equipItem(self, itemIndex):
        '''
        item index represents the index in the inventory
        '''

        listIndex = itemIndex - 1

        if not (0 <= listIndex < len(self.playerHotbar)):
            return 
        
        if self.currentItemIndex == itemIndex:
            if self.currentItem != None:
                self.currentItem.equipped = False
            self.currentItem = None
            self.currentItemIndex = -1
        else:
            
            if self.currentItem != None:
                self.currentItem.equipped = False

            newItem = self.playerHotbar[listIndex]
            newItem.equipped = True

            self.currentItemIndex = itemIndex
            self.currentItem = newItem


    def addItemToHotbar(self, item):

        for existingItem in self.playerHotbar:
            if existingItem.type == item.type:
                item.cleanUp()
                return

        self.playerHotbar.append(item)

    def removeItemFromHotbar(self, item):
        item.cleanUp()
        index = self.playerHotbar.remove(item)


    def draw(self):
        # make sure to update this soon.
        animationFrame = self.animationController.getAnimationFrame(self.app)

        if animationFrame == None:
            #print(animationFrame)
            return
        
        spriteImage = CMUImage(animationFrame if self.facingDirection == "right" else animationFrame.transpose(Image.FLIP_LEFT_RIGHT))

        drawImage(
            spriteImage,
            self.position[0],
            self.position[1],
            align = "center",
            width = self.visualHitboxSize["width"],
            height = self.visualHitboxSize["height"]
        )

        self.HealthBar.drawHp()
    
    def keyPressedLogic(self, key):
        if not key.isalpha():
            self.equipItem(int(key))

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
    
    def takeDamage(self, damageAmount):
        self.health = max(self.health - damageAmount,0)
        print("make playet take damage")
    

    def runLogic(self):
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