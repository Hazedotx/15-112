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

    for dirpath, dirnames, filenames in os.walk(rootFolder):
        filenames.sort()
        png_files = [f for f in filenames if f.endswith('.png')]

        if not png_files:
            continue

        animation_name = os.path.basename(dirpath).lower()
        frames = []
        for filename in png_files:
            full_path = os.path.join(dirpath, filename)
            image = Image.open(full_path)
            frames.append(image)

        animations[animation_name] = frames
        print(f"Loaded animation '{animation_name}' with {len(frames)} frames.")

    return animations

print(loadAnimations("TermProject/SpriteAnimations"))