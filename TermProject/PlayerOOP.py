import SpriteAnimations


class Player:
    def __init__(self, app):
        
        self.type = "player"
        self.position = [app.width/2, app.height/2],
        self.isMoving = False
        self.keysPressed = set()
        self.facingDirection = "right"

        self.movementSpeed = 60

        self.playerHitboxSize = {
            "width": app.width / 10,
            "height": app.height / 8
        }

        self.animationInfo = SpriteAnimations.

        pass