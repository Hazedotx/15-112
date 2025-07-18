from cmu_graphics import *
from PIL import Image
import SpriteAnimations
import Config


class Skeleton:
    def __init__(self, app):
        self.app = app
        self.type = "skeleton"
        self.position = [app.width/2, app.height/2]
        
        self.