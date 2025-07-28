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
        "tileSize": 12, # the tile size of each grid in pixels
        "gridWidth": 80,
        "gridHeight": 60
    },

    "spriteAnimations": spriteAnimations
}

SETTINGS = {
    "fullScreenEnabled": False,
    "fps": 60,
    "volume": 0.8,
    "difficulty": "normal"
}