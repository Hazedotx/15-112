from cmu_graphics import *

class LoadingScreenManager:
    def __init__(self, app):
        self.app = app
        self.loadingText = ""

        self.isActive = False

        self.duration = 0
        self.startTick = 0
        self.onComplete = None # this is gonna be a callback ;)
        self.onCompleteParams = None # this will be sent through the callback

    def startLoadingScreen(self, message, duration, callback, callbackParams = []):
        '''
        duration is in seconds.
        callback is for when the loading screen is done
        message is the message obviously
        callback params is a table which gets unpacked and then sent
        '''

        if self.isActive:
            print("Attempt to start new loading screen whilst one is already active")
            return

        self.loadingText = message
        self.duration = duration
        self.onComplete = callback
        self.onCompleteParams = callbackParams
        self.startTick = self.app.globalStates["totalTicks"]
        self.isActive = True

    def runLogic(self):
        if not self.isActive:
            return
    
        elapsedTime = (self.app.globalStates["totalTicks"] - self.startTick) / self.app.stepsPerSecond

        if elapsedTime >= self.duration:
            self.loadingComplete()
            
    def loadingComplete(self):
        if self.onComplete:
            if self.onCompleteParams:
                #unpack the params and send em through
                self.onComplete(*self.onCompleteParams)
            else:
                self.onComplete()

        self.isActive = False
        self.onComplete = None
        self.onCompleteParams = None
        self.loadingText = ""

    def draw(self):
        if not self.isActive:
            return 
        
        drawRect(self.app.width/2, self.app.height/2, self.app.width, self.app.height, fill = "black", align = "center")
        drawLabel(self.loadingText, self.app.width/2, self.app.height/2, size = 24, bold = True, fill = "white")

    

