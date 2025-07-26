from cmu_graphics import *
from PIL import Image
import SpriteAnimations
import HealthBarOOP
import Config
import math
import uuid

class Skeleton:
    def __init__(self, app, startPosition):
        self.app = app

        self.id = uuid.uuid4()

        self.type = "skeleton"
        self.position = startPosition
        self.facingDirection = "left"

        self.state = "idle" 

        self.HealthBar = HealthBarOOP.HealthBar(self.app,self)
        
        self.aggroRadius = 250 
        self.attackRadius = 50 

        self.movementSpeed = 45 
        self.health = 100
        self.maxHealth = 100

        self.attackDamage = 10

        self.attackCooldown = 1.5
        self.timeSinceLastAttack = self.attackCooldown 

        self.animationController = SpriteAnimations.AnimationController(
            SpriteAnimations.spriteAnimations["skeleton"], 
            SpriteAnimations.animationSettings["skeleton"]
        )
        self.hitboxSize = {
            "width": app.width / 12,
            "height": app.height / 9
        }

    def __eq__(self, other):
        if not isinstance(other, Skeleton): return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)


    def getDistanceToPlayer(self):
        player_pos = self.app.player.position
        dx = self.position[0] - player_pos[0]
        dy = self.position[1] - player_pos[1]
        return math.sqrt(dx**2 + dy**2)

    def updateState(self):
        if self.state in ["attacking", "dying"]:
            return

        distanceFromPlr = self.getDistanceToPlayer()
        attackCooldownOver = (self.timeSinceLastAttack >= self.attackCooldown)

        if distanceFromPlr <= self.attackRadius and attackCooldownOver:
            self.attackPlayer()
        elif distanceFromPlr <= self.aggroRadius:
            self.state = "chasing"
        else:
            self.state = "idle"

    def moveTowardsPlayer(self):
        playerPos = self.app.player.position
        skeletonPos = self.position

        dx = playerPos[0] - skeletonPos[0]
        dy = playerPos[1] - skeletonPos[1]

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
        self.state = "attacking"
        self.timeSinceLastAttack = 0

        self.animationController.playAnimationOnce(
            "attack",
            onComplete=self.onAttackAnimationComplete
        )
        if self.getDistanceToPlayer() <= self.attackRadius:
            # self.app.player.takeDamage(self.attackDamage)
            pass

    def onAttackAnimationComplete(self):
        self.state = "idle"

    def takeDamage(self, amount):
        if self.state == "dying": return
        self.health -= amount
        if self.health <= 0:
            self.onDeath()

    def cleanUp(self):
        self.app.gcEntities["enemies"].add(self)
        self.HealthBar.clearReferences()
        print("Skeleton cleanup called.")

    def onDeath(self):
        self.state = "dying"
        self.animationController.playAnimationOnce("death", onComplete=self.cleanUp)

    def runLogic(self):
        if self.state == "dying":
            self.animationController.updateAnimation(self.app)
            return
        
        self.timeSinceLastAttack += (1 / self.app.stepsPerSecond)

        self.updateState() 

        if self.state == "chasing":
            self.moveTowardsPlayer()
        
        self.animationController.addAnimToStack("idle")
        if self.state == "chasing":
            self.animationController.addAnimToStack("walk")
        else:
            self.animationController.cancelAnimation("walk")
        
        self.animationController.updateAnimation(self.app)

    def draw(self):
        animationFrame = self.animationController.getAnimationFrame(self.app)
        if animationFrame is None:
            return
        
        if self.facingDirection == "left":
            spriteImage = CMUImage(animationFrame.transpose(Image.FLIP_LEFT_RIGHT))
        else:
            spriteImage = CMUImage(animationFrame)

        self.HealthBar.drawHp()

        drawImage(
            spriteImage,
            self.position[0],
            self.position[1],
            align = "center",
            width = self.hitboxSize["width"],
            height = self.hitboxSize["height"]
        )
