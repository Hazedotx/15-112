import Helper
import SpriteAnimations

SCREEN_WIDTH, SCREEN_HEIGHT = Helper.grabScreenDimensions()

spriteAnimations = SpriteAnimations.spriteAnimations

STATIC_INFO = {
    "fullScreenDimensions": {
        "width": SCREEN_WIDTH,
        "height": SCREEN_HEIGHT
    },

    "DungeonConfig": {
        "tileSize": 36, # the tile size of each grid in pixels
        "gridWidth": 40, # the map grid width my screen can handle. 
        "gridHeight": 23 # the map grid height my screen can handle
    },

    "spriteAnimations": spriteAnimations
}

SETTINGS = {
    "fullScreenEnabled": False,
    "fps": 60,
    "volume": 0.8,
    "difficulty": "hard"
}