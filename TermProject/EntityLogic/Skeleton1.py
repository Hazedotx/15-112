from cmu_graphics import *
from PIL import Image
import SpriteAnimations
import Config
import math

class Skeleton:
    def __init__(self, app, startPosition):
        self.app = app
        
        self.type = "skeleton"
        self.position = startPosition
        self.facingDirection = "left"

        self.state = "idle" 
        
        self.aggroRadius = 250 
        
        self.attackRadius = 50 

        self.movementSpeed = 45 
        self.health = 100
        self.attackDamage = 10

        self.attackCooldown = 1.5 # 
        self.timeSinceLastAttack = self.attackCooldown 

        self.animationController = SpriteAnimations.AnimationController(
            SpriteAnimations.spriteAnimations["skeleton"], 
            SpriteAnimations.animationSettings["skeleton"]
        )
        self.skeletonHitboxSize = {
            "width": app.width / 12,
            "height": app.height / 9
        }

    def getDistanceToPlayer(self):
        return math.sqrt((self.position[0] - self.app.player.position[0])**2 + (self.position[1] - self.app.position[1])** 2)

    def updateState(self):

        distanceFromPlr = self.getDistanceToPlayer()
        attackCooldownOver = (self.timeSinceLastAttack >= self.attackCooldown)

        if (distanceFromPlr <= self.attackRadius) and (attackCooldownOver):
            self.state = "attacking"
        elif distanceFromPlr <= self.aggroRadius and self.state != "attacking":
            self.state == "chasing"
        elif distanceFromPlr > self.aggroRadius and self.state != "attacking":
            self.state = "idle"

        pass

    def moveTowardsPlayer(self):

        playerPos = app.player.Position
        skeletonPos = self.position

        dx = playerPos[0] - skeletonPos[0]
        dy = playerPos[0] - skeletonPos[1]

        distance = math.hypot(dx, dy)

        if distance > 0:
            normDx = dx / distance
            normDy = dy / distance

            speedPerStep = self.movementSpeed * (1 / self.app.stepsPerSecond)

            self.position[0] += normDx * speedPerStep 
            self.position[1] += normDy * speedPerStep

            if dx > 1:
                self.facingDirection = "right"
            elif dx < -1:
                self.facingDirection = "left"


    def attackPlayer(self):

        self.timeSinceLastAttack = 0

        self.animationController.playAnimationOnce(
            "attack",
            onComplete=self.onAttackAnimationComplete
        )

        if self.getDistanceToPlayer() <= self.attackRadius:
            self.app.player.takeDamage(self.attackDamage)
        pass

    def onAttackAnimationComplete(self):
        self.state = "idle"
        pass

    def takeDamage(self, amount):

        self.health -= amount

        if self.health <= 0:
            self.onDeath()

        pass

    def cleanUp():
        # this is gonna be used to clean up the data for the skeleton once it dies
        pass

    def onDeath(self):
        self.animationController.playAnimationOnce("death", onComplete=self.cleanUp)


    def runSkeletonLogic(self):

        if self.state == "dying":
            self.animationController.updateAnimation(self.app)
            return
        
        self.timeSinceLastAttack += (1 / self.app.stepsPerSecond)

        self.updateState()

        if self.state == "chasing":
            self.moveTowardsPlayer()
        elif self.state == "attacking":
            self.attackPlayer()
        
        self.animationController.addAnimToStack("idle")

        if self.state == "chasing":
            self.animationController.addAnimToStack("walk")
        else:
            self.animationController.updateAnimation(self.app)


    def drawSkeleton(self):
            animationFrame = self.animationController.getAnimationFrame(self.app)

            if animationFrame is None:
                return
            
            if self.facingDirection == "left":
                spriteImage = CMUImage(animationFrame.transpose(Image.FLIP_LEFT_RIGHT))
            else:
                spriteImage = CMUImage(animationFrame)

            drawImage(
                spriteImage,
                self.position[0],
                self.position[1],
                align="center",
                width=self.skeletonHitboxSize["width"],
                height=self.skeletonHitboxSize["height"]
            )