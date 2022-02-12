from Timer import Timer

class Stopwatch(Timer):
    
    def __init__(self):
        super().__init__()
        self.resultTime = 0
        self.stringTime = ""

    def Count(self, status=""):
        
        if super().Count() and status != "":

            status += (". " if self.counter % 2 == 0 else "..")

            print(status, end='\r')
            return True
        return False
        
    def MinutePassed(self):
        return self.counter % 60 == 0

    def Reset(self):
        self.resultTime = self.counter
        self.counter = 0
        self.stringTime = self.ReadableTime(self.resultTime)