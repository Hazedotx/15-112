"""
#pip install pillow


This game is basically a dungeon explorer. The main goal of the game is to explore the main dungeon completely, but it isnt that simple

While exploring, there is a chance you stumble into a dungeon with varying difficulty. Depending on the difficulty, the amount of enemies increases
When you beat the dungeon, you resume your exploration of the main dungeon.

There is also a chance you can find different types of weapons lying on the ground whilst exploring.
The big hammer weapon one shots all the enemies because I got tired of clearing the waves legitametely every time

I wish I had more time to add more enemy types, weapon types, a homescreen, a setting screen, an actual life system for the player, and more. 


Citations:
AI Usage_________

Utilized chat gpt for the dungeon generation logic(Used it for logic, not copy paste code). The dungeon generation logic is the logic which recursively splits chunks horizontally and vertically and then builds paths to eachother. 
Utilized chat gpt for advice on how to load in my sprite animation stuff(it told me about os)
Utilized chat gpt to learn about PIL Images.

External Sources________
used chat gpts advice to use os and researched using this website: https://www.w3schools.com/python/module_os.asp
used pillow and PIL library in order to convert 200+ shapes on my screen to a single image so my game doesnt crash:
    https://pypi.org/project/pillow/

used uuid so i could hash enemies and players uniquely. https://docs.python.org/3/library/uuid.html

used tkinter so i could pull the users display size(never ended up using it for anything because I didnt have time)

https://docs.python.org/3/library/tkinter.html

used https://www.geeksforgeeks.org/python/enumerate-in-python/ to learn about enumerate


Utilized this dungeon tileset to  make the game come to life a bit more:
I never got to add the other enemies because of a lack of time, but it is ok
https://0x72.itch.io/dungeontileset-ii





"""