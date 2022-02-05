from Timer import Timer
from playsound import playsound

class Alarm(Timer):

    def __init__(self, alarmSound, alarmTime=3600):
        self.alarmTime = alarmTime
        self.alarmSound = alarmSound

    def CheckTime(self):
        if self.counter > self.alarmTime:
            playsound(self.alarmSound)
            