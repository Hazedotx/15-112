from cmu_graphics import *
from PIL import Image as PILImage, ImageDraw
import random
import Config
import copy
import os

tileMap = {
    0: "defaultFloor",
    1: "defaultRock",# its just rock.
    2: "floor_1",
    3: "floor_2",
    4: "floor_3",
    5: "floor_4",
    6: "floor_5",
    7: "floor_6",
    8: "floor_7",
    9: "floor_8",
    10: "wall_edge_bottom_left",
    11: "wall_edge_bottom_right",
    12: "wall_edge_left",
    13: "wall_edge_mid_left",
    14: "wall_edge_mid_right",
    15: "wall_edge_right",
    16: "wall_edge_top_left",
    17: "wall_edge_top_right",
    18: "wall_edge_tshape_bottom_left",
    19: "wall_edge_tshape_bottom_right",
    20: "wall_edge_tshape_left",
    21: "wall_edge_tshape_right",
    22: "wall",
    23: "wall_top"
    
}


# the dungeon generation LOGIC(not code) made with the help of chast gpt bc i didnt even know this was a thing. here is the prompt I inputted:
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
        self.gridLayer = [[set() for _ in range(gridWidth)] for _ in range(gridHeight)]

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

        def getDefaultTile(y, x):
            #defaultWall or defaultFloor
            if 0 <= y < self.gridHeight and 0 <= x < self.gridWidth:
                return tileMap.get(self.grid[y][x],None)
            return None
            

        for y in range(self.gridHeight):
            for x in range(self.gridWidth):
                TileUp = getDefaultTile(y - 1, x)
                TileDown = getDefaultTile(y + 1, x)
                TileDownLeft = getDefaultTile(y + 1, x - 1)
                TileLeft = getDefaultTile(y, x - 1)
                TileRight = getDefaultTile(y, x + 1)
                TileCurr = getDefaultTile(y,x)

                if TileCurr == "defaultRock":

                    floorUp = (TileUp == "defaultFloor")
                    floorDown = (TileDown == "defaultFloor")
                    floorLeft = (TileLeft == "defaultFloor")
                    floorRight = (TileRight == "defaultFloor")

                    if floorDown:
                        #I am using sets so i can layer tiles and shit 
                        self.gridLayer[y][x].add(22) # add the wall
                        self.gridLayer[y - 1][x].add(23) # add the top part on the wall

                        # logic for checking if the wall is a corner piece
                        if not floorLeft:
                            self.gridLayer[y][x].add(13)
                        elif not floorRight:
                            self.gridLayer[y][x].add(14)


                    
                    

                    
                elif TileCurr == "defaultFloor":

                    rockUp = (TileUp == "defaultRock")
                    rockDown = (TileDown == "defaultRock")
                    rockLeft = (TileLeft == "defaultRock")
                    rockRight = (TileRight == "defaultRock")

                    if rockDown:
                        self.gridLayer[y][x].add(23)
                        self.gridLayer[y + 1][x].add(22)
                    elif rockLeft:
                        self.gridLayer[y][x].add(13)
                    elif rockRight:
                        self.gridLayer[y][x].add(14)


                    self.gridLayer[y][x].add(random.randint(2,9))




                    
    # EXTERNAL FUNCTIONS FROM LIKE MAIN_________

    def convertDungeonToImage(self):
        ts = Config.STATIC_INFO["DungeonConfig"]["tileSize"]
        gridWidth = Config.STATIC_INFO["DungeonConfig"]["gridWidth"]
        gridHeight = Config.STATIC_INFO["DungeonConfig"]["gridHeight"]
        mapSizeX = ts * gridWidth
        mapSizeY = ts * gridHeight

        baseFloorSprite = self.spriteImages.get(31) # this will be used to fill the gap in the t-shape stuff

        drawOrder = [
            2, 3, 4, 5, 6, 7, 8, 9, # Base Floors
            22,# Base Wall

            23,# Wall Top
            10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21 # wall edges
        ]


        finalPilImage = PILImage.new("RGBA", (mapSizeX, mapSizeY))

        for y, row in enumerate(self.gridLayer):
            for x, assetIdSet in enumerate(row):
                
                tileImage = PILImage.new("RGBA",(ts, ts), (0,0,0,0))

                drawX, drawY = x * ts, y * ts

                for tileId in drawOrder:
                    if tileId in assetIdSet:
                        spriteToDraw = self.spriteImages.get(tileId)
                        if spriteToDraw:
                            tileImage = PILImage.alpha_composite(tileImage,spriteToDraw)

                finalPilImage.paste(tileImage,(drawX,drawY), tileImage)
            
        
        self.dungeonImage = CMUImage(finalPilImage)

    def draw(self):
        drawImage(self.dungeonImage, 0, 0)

        

    

