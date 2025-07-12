import os
from PIL import Image


def loadAnimations(rootFolder):
    """
    should return sm like this so i dont have to  manually define the images every time :skull:
    {
        'idle': [ImageObject1, ImageObject2],
        'run': [ImageObject3, ImageObject4]
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