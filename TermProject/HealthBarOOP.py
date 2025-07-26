from cmu_graphics import *
from PIL import Image
import SpriteAnimations
import Config
import math
import uuid
import Helper


class HealthBar():

    def __init__(self, app, entity):
        self.app = app
        self.entity = entity
        self.hpBarSize = (30, 15)
        self.disabled = False
    
    def getHp(self):
        if self.disabled: return 0.001
        return max(0.00001, self.entity.health)
    
    def drawHp(self):
        if self.disabled: return
        if self.entity.health == self.entity.maxHealth: return
        xPos = self.entity.position[0] + self.entity.hitboxSize["width"]/2
        yPos = self.entity.position[1] - self.entity.hitboxSize["height"]
        drawRect(xPos, yPos, self.hpBarSize[0], self.hpBarSize[1], align = "right-top", fill = "red"),
        drawRect(xPos, yPos, self.hpBarSize[0] * (self.getHp()/self.entity.maxHealth), self.hpBarSize[1], align = "right-top", fill = "green"),

    def clearReferences(self):
        #used for garbage collecting an entity whenever they die and I need to remove references.
        self.entity = None
        self.disabled = True