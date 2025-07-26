from cmu_graphics import *
from PIL import Image
import SpriteAnimations
import Config
import math
import uuid
import Helper


class Sword:
    def __init__(self, app):

        self.id = uuid.uuid4()

        self.app = app
        self.type = "sword"

        self.center = self.app.player.position
        self.position = [app.width/2, app.height/2]
        self.swordAngle = 90,
        self.attackCoolDown = 0.1
        self.lastAttack = 0

        self.mousePosition = [app.width/2, app.height/2]
        self.lastMousePosition = [app.width/2, app.height/2]

        self.attackDamage = 5
        self.swordSpeed = 500 # has to be going faster than 10 __/s in order for it do deal damage to enemies
        self.clampRadius = 50 # the radius the sword traces around

        self.animationController = SpriteAnimations.AnimationController(
            SpriteAnimations.spriteAnimations["sword"], 
            SpriteAnimations.animationSettings["sword"]
        )

        self.animationController.addAnimToStack("default")

        self.hitboxSize = {
            "width": 2 * 12,
            "height": 3 * 12
        }

    def __eq__(self, other):
        if not isinstance(other, Sword): return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)


    def hitEnemies(self): # I dont think this breaks MVC rules bc i am not drawing anything. js checking hitbox
        hitList = set()

        for enemy in self.app.allEntities["enemies"]:
            if Helper.getColliding(
                self.position[0],self.position[1],self.hitboxSize["width"],self.hitboxSize["height"],
                enemy.position[0],enemy.position[1],enemy.hitboxSize["width"],enemy.hitboxSize["height"]
            ):
                hitList.add(enemy)

        return hitList

    def onMouseMove(self, mouseX, mouseY):
        # this code will take the last mouse x position and mouse y position, compute the change within the last frame and this frame
        # it will use that to calculate the speed of the sword. 
        #if the speed of the sword is fast enough, it will be able to deal damage to enemies.

        self.lastMousePosition[0] = self.mousePosition[0]
        self.lastMousePosition[1] = self.mousePosition[1]

        self.mousePosition[0] = mouseX
        self.mousePosition[1] = mouseY


    def runLogic(self):
        self.animationController.updateAnimation(self.app)

        deltaX = self.lastMousePosition[0] - self.mousePosition[0]
        deltaY = self.lastMousePosition[1] - self.mousePosition[1]
        deltaXY = math.sqrt(deltaX**2 + deltaY**2)

        self.swordAngle = math.atan2(self.mousePosition[1] - self.center[1], self.mousePosition[0] - self.center[0])
        self.position[0] = self.center[0] + self.clampRadius * math.cos(self.swordAngle)
        self.position[1] = self.center[1] + self.clampRadius * math.sin(self.swordAngle)

        speedPerSecond = deltaXY * self.app.stepsPerSecond
        currentTime = self.app.globalStates["totalTicks"]
        cooldownInTicks = self.attackCoolDown * self.app.stepsPerSecond

        if (speedPerSecond >= self.swordSpeed) and ((currentTime - self.lastAttack) >= cooldownInTicks):
            #checks the cooldown and how fast the sword is going
            #print("attack")
            for enemy in self.hitEnemies():
                enemy.takeDamage(self.attackDamage)

                print(enemy.type, enemy.health)
            self.lastAttack = currentTime
            
            


    def draw(self):
        # make sure to update this soon.
        animationFrame = self.animationController.getAnimationFrame(self.app)

        if animationFrame == None:
            return
        
        spriteImage = CMUImage(animationFrame)

        self.animationController.currentImage = drawImage(
            spriteImage,
            self.position[0],
            self.position[1],
            align = "center",
            width = self.hitboxSize["width"],
            height = self.hitboxSize["height"],
            rotateAngle = 90 + math.degrees(self.swordAngle)
        )

    pass