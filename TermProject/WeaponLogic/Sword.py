from cmu_graphics import *
from PIL import Image
import SpriteAnimations
import Config
import math
import uuid



class Sword:
    def __init__(self, app):

        self.id = uuid.uuid4()

        self.app = app
        self.type = "sword"

        self.center = self.app.player.position
        self.position = [app.width/2, app.height/2]
        self.lastMousePosition = [app.width/2, app.height/2]

        self.attackDamage = 10
        self.swordSpeed = 10 # has to be going faster than 10 __/s in order for it do deal damage to enemies
        self.lastAttack = 0 # this will track the cooldown state for the sword
        self.clampRadius = 5 # the radius the sword traces around

        self.animationController = SpriteAnimations.AnimationController(
            SpriteAnimations.spriteAnimations["sword"], 
            SpriteAnimations.animationSettings["sword"]
        )

        self.animationController.addAnimToStack("default")

        self.hitboxSize = {
            "width": app.width / 10,
            "height": app.height / 8
        }

    def __eq__(self, other):
        if not isinstance(other, Sword): return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)


    def hitEnemies(self): # I dont think this breaks MVC rules bc i am not drawing anything. js checking hitbox
        hitList = set()

        for enemy in self.app.allEntities["Enemies"]:
            if self.animationController.currentImage.hitsShape(enemy.animationController.currentImage):
                hitList.add(enemy)

        #return a list of enemies the sword hit.
        return hitList

    def onMouseMove(self, mouseX, mouseY):
        # this code will take the last mouse x position and mouse y position, compute the change within the last frame and this frame
        # it will use that to calculate the speed of the sword. 
        #if the speed of the sword is fast enough, it will be able to deal damage to enemies.

        deltaX = self.position[0] - mouseX
        deltaY = self.position[1] - mouseY
        deltaXY = math.sqrt(deltaX**2 + deltaY**2)

        angle = math.atan((mouseX - self.center) / (mouseY - self.center))
        self.position[0] = self.center + self.clampRadius * math.cos(angle)
        self.position[1] = self.center + self.clampRadius * math.sin(angle)

        if self.swordSpeed <= deltaXY:
            print("Can hurt enemy")
            for enemy in self.hitEnemies():
                enemy.takeDamage(self.swordSpeed // 10)


        

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
            height = self.hitboxSize["height"]
        )

    pass