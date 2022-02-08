from Timer import Timer
from playsound import playsound

class Alarm(Timer):

    def __init__(self, alarmSound, alarmTime=3600):
        super().__init__()
        self.alarmTime = alarmTime
        self.alarmSound = alarmSound

    def Count(self):
        """If a second has passed, increments the counter. Returns True if the alarm has gone off."""
        if self.SecondPassed():
            self.counter += 1

            if self.counter > self.alarmTime:
                playsound(self.alarmSound)
                return True
            
        return False