from cmu_graphics import *
from PIL import Image as PILImage, ImageDraw
import random
import Config
import copy
import os

tileMap = {
    1: "defaultWall", # this is generated as the base for dungeon generation
    2: "defaultFloor",# this is generated as the base for dungeon generation

    #everything beneath here is generated on a second loop
    # walls

    3: "wall_edge_bottom_left",
    4: "wall_edge_bottom_right",
    5: "wall_edge_left",
    6: "wall_edge_right",
    7: "wall_edge_top_left",
    8: "wall_edge_top_right",
    9: "wall_edge_mid_left",
    10: "wall_edge_mid_right",

    # floors

    11: "floor_1",
    12: "floor_2",
    13: "floor_3",
    14: "floor_4",
    15: "floor_5",
    16: "floor_6",
    17: "floor_7",
    18: "floor_8"
}


# this was made with the help of chast gpt bc i didnt even know this was a thing. here is the prompt I inputted:
# "since i want to create bsp dungeon generator, guide me through the entire logical proccess."
# it just explained me all the logic steps i needed and thats how i got this foundation

class Node:
    def __init__(self, y, x, height, width):
        self.y = y
        self.x = x
        self.height = height
        self.width = width
        self.leftChild = None
        self.rightChild = None

class Room:
    def __init__(self, y, x, height, width):
        self.y = y
        self.x = x
        self.height = height
        self.width = width

    def center(self):
        return self.y + self.height // 2, self.x + self.width // 2

class DungeonGenerator:
    def __init__(self, app, gridHeight, gridWidth):
        self.gridHeight = gridHeight
        self.gridWidth = gridWidth
        self.grid = [[1 for _ in range(gridWidth)] for _ in range(gridHeight)]
        self.dungeonImage = None
        self.root = None
        self.rooms = []
        self.app = app
        self.spriteImages = {}

    def loadSprites(self):
        # took this from my sprite animations.py logic and slightly altered it.
        ts = Config.STATIC_INFO["DungeonConfig"]["tileSize"]
        spriteFolderPath = "TermProject/MapSprites"

        for tileId, tileName in tileMap.items():
            if "default" in tileName:
                continue

            filePath = f"{spriteFolderPath}/{tileName}.png"
            sprite = PILImage.open(filePath).convert("RGBA")
            if sprite.size != (ts, ts):
                sprite = sprite.resize((ts, ts))
            self.spriteImages[tileId] = sprite
            #print(f"Sprite Image {tileId} was not found in the MapSprites Folder")

    def recursivelySplit(self, node, depth):
        minSize = 10
        maxDepth = 4

        if depth >= maxDepth or (node.height < minSize and node.width < minSize):
            return

        splitHorizontal = random.choice([True, False])

        if node.width > node.height * 1.5:
            splitHorizontal = False
        elif node.height > node.width * 1.5:
            splitHorizontal = True

        if splitHorizontal:
            if node.height < minSize * 2: return
            splitY = random.randint(minSize, node.height - minSize)
            node.leftChild = Node(node.y, node.x, splitY, node.width)
            node.rightChild = Node(node.y + splitY, node.x, node.height - splitY, node.width)
        else:
            if node.width < minSize * 2: return
            splitX = random.randint(minSize, node.width - minSize)
            node.leftChild = Node(node.y, node.x, node.height, splitX)
            node.rightChild = Node(node.y, node.x + splitX, node.height, node.width - splitX)

        self.recursivelySplit(node.leftChild, depth + 1)
        self.recursivelySplit(node.rightChild, depth + 1)

    def createRooms(self, node):
        if node.leftChild or node.rightChild:
            if node.leftChild:
                self.createRooms(node.leftChild)
            if node.rightChild:
                self.createRooms(node.rightChild)
        else:
            roomHeight = random.randint(5, node.height - 2) if node.height > 7 else 5
            roomWidth = random.randint(5, node.width - 2) if node.width > 7 else 5

            roomY = node.y + random.randint(1, node.height - roomHeight - 1) if node.height - roomHeight > 2 else node.y + 1
            roomX = node.x + random.randint(1, node.width - roomWidth - 1) if node.width - roomWidth > 2 else node.x + 1

            for y in range(roomY, roomY + roomHeight):
                for x in range(roomX, roomX + roomWidth):
                    if y < self.gridHeight and x < self.gridWidth:
                        self.grid[y][x] = 0
            self.rooms.append(Room(roomY, roomX, roomHeight, roomWidth))

    def createCorridors(self, node):
        if node.leftChild is None or node.rightChild is None:
            return

        leftRoom = self.getRandomRoomFromNode(node.leftChild)
        rightRoom = self.getRandomRoomFromNode(node.rightChild)

        if leftRoom and rightRoom:
            y1, x1 = leftRoom.center()
            y2, x2 = rightRoom.center()

            if random.random() < 0.5:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    if y1 < self.gridHeight and x < self.gridWidth: self.grid[y1][x] = 0
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    if y < self.gridHeight and x2 < self.gridWidth: self.grid[y][x2] = 0
            else:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    if y < self.gridHeight and x1 < self.gridWidth: self.grid[y][x1] = 0
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    if y2 < self.gridHeight and x < self.gridWidth: self.grid[y2][x] = 0
        
        self.createCorridors(node.leftChild)
        self.createCorridors(node.rightChild)
    
    def getRandomRoomFromNode(self, node):
        if not self.rooms:
            return None

        possibleRooms = []
        nodesToVisit = [node]

        while nodesToVisit:
            currentNode = nodesToVisit.pop()
            if currentNode.leftChild is None and currentNode.rightChild is None:
                for room in self.rooms:
                    if (room.x >= currentNode.x and room.x + room.width <= currentNode.x + currentNode.width and
                        room.y >= currentNode.y and room.y + room.height <= currentNode.y + currentNode.height):
                        possibleRooms.append(room)
                        break
            else:
                if currentNode.leftChild:
                    nodesToVisit.append(currentNode.leftChild)
                if currentNode.rightChild:
                    nodesToVisit.append(currentNode.rightChild)
        
        return random.choice(possibleRooms) if possibleRooms else None

    def generate(self):
        self.root = Node(0, 0, self.gridHeight, self.gridWidth)
        self.recursivelySplit(self.root, 0)
        self.createRooms(self.root)
        self.createCorridors(self.root)
        return self.grid
    

    def formatDungeon(self):
        
        gridCopy = copy.deepcopy(self.grid)

        def getTile(y, x):
            if 0 <= y < self.gridHeight and 0 <= x < self.gridWidth:
                return gridCopy[y][x]
            return None

        for y in range(self.gridHeight):
            for x in range(self.gridWidth):
                currentTile = getTile(y, x)

                if currentTile == 1:
                    isFloorAbove = getTile(y - 1, x) in (0, 2)
                    isFloorBelow = getTile(y + 1, x) in (0, 2)
                    isFloorLeft = getTile(y, x - 1) in (0, 2)
                    isFloorRight = getTile(y, x + 1) in (0, 2)

                    if isFloorBelow and isFloorRight:
                        self.grid[y][x] = 7
                    elif isFloorBelow and isFloorLeft:
                        self.grid[y][x] = 8
                    elif isFloorAbove and isFloorRight:
                        self.grid[y][x] = 3
                    elif isFloorAbove and isFloorLeft:
                        self.grid[y][x] = 4
                    
                    elif isFloorRight:
                        self.grid[y][x] = 5
                    elif isFloorLeft:
                        self.grid[y][x] = 6

                    elif isFloorBelow:
                        self.grid[y][x] = 9
                    elif isFloorAbove:
                        self.grid[y][x] = 10
                    
                elif currentTile == 0:
                    self.grid[y][x] = random.randint(11, 18)


                    
    # EXTERNAL FUNCTIONS FROM LIKE MAIN_________

    def convertDungeonToImage(self):
        # this will be used to convert the entire dungeon into a single reuseable image
        # this is because drawing 2000+ shapes every frame is simply too much to handle lol
        # this will use PIL images and then uh convert it to a CMU Image
        ts = Config.STATIC_INFO["DungeonConfig"]["tileSize"]
        gridWidth = Config.STATIC_INFO["DungeonConfig"]["gridWidth"]
        gridHeight = Config.STATIC_INFO["DungeonConfig"]["gridHeight"]
        
        mapSizeX = ts * gridWidth
        mapSizeY = ts * gridHeight

        pilImage = PILImage.new("RGB", (mapSizeX, mapSizeY))
        drawContext =  ImageDraw.Draw(pilImage)
        #https://www.geeksforgeeks.org/python/enumerate-in-python/
        # also used PIL Docs

        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                drawX, drawY = x * ts, y * ts

                sprite = self.spriteImages.get(tile)
                if sprite:
                    drawX, drawY = x * ts, y * ts
                    pilImage.paste(sprite, (drawX, drawY), sprite)
                else:
                    drawContext.rectangle([drawX, drawY, drawX + ts, drawY + ts], fill="black")

        self.dungeonImage = CMUImage(pilImage)

    def draw(self):
        drawImage(self.dungeonImage, 0, 0)
        

    

