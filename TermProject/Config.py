import Helper
import SpriteAnimations

SCREEN_WIDTH, SCREEN_HEIGHT = Helper.grabScreenDimensions()

spriteAnimations = SpriteAnimations.spriteAnimations

STATIC_INFO = {
    "fullScreenDimensions": {
        "width": SCREEN_WIDTH,
        "height": SCREEN_HEIGHT
    },
    "spriteAnimations": spriteAnimations
}

SETTINGS = {
    "fullScreenEnabled": False,
    "fps": 60,
    "volume": 0.8,
    "difficulty": "normal"
}