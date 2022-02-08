from os import system
from Timer import Timer

class Stopwatch(Timer):
    
    def __init__(self):
        super().__init__()
        self.resultTime = 0
        self.stringTime = ""

    def Count(self, status=""):
        
        if super().Count() and status != "":
            dots = "."
            if self.counter % 2 == 0:
                dots = ".."

            system("cls")
            print(status + dots)
            return True
        return False
        

    def MinutePassed(self):
        return self.counter % 60 == 0

    def Reset(self):
        super().Reset()
        self.resultTime = self.counter
        self.stringTime = self.ReadableTime(self.resultTime)