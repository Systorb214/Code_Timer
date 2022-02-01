from os import system
from Timer import Timer

class Stopwatch(Timer):
    
    def __init__(self):
        super().__init__()
        self.resultTime = 0
        self.stringTime = ""

    def MinutePassed(self):
        return self.counter % 60 == 0

    def Reset(self):
        self.resultTime = self.counter
        self.stringTime = self.ReadableTime(self.resultTime)
        self.counter = 0