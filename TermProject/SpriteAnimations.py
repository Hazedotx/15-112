import os
from PIL import Image

settings = {
    "knightidle": {
        'loops': True,
        'priority': True
    }
}


def loadAnimations(rootFolder):
    """
    should return sm like this 
    {
        'knightidle': {
            'frames': [ImageObject1, ImageObject2],
            'priority': 0,
            'loops': True
        },
    }
    """


    animations = {}

    for dirPath, dirNames, fileNames in os.walk(rootFolder):
        fileNames.sort()
        pngFiles = [f for f in fileNames if f.endswith('.png')]

        if not pngFiles:
            continue

        animationName = os.path.basename(dirPath).lower()
        frames = []
        for fileName in pngFiles:
            fullPath = os.path.join(dirPath, fileName)
            image = Image.open(fullPath)
            frames.append(image)

        animations[animationName] = frames

    return animations

print(loadAnimations("TermProject/SpriteAnimations"))