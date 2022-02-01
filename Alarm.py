from Timer import Timer
from playsound import playsound

class Alarm(Timer):

    startSound = "./Sounds/Start_coding.mp3"
    stopSound = "./Sounds/Stop_coding.mp3"
    def __init__(self, alarmTime=3600):
        self.alarmTime = alarmTime

    def CheckTime(self):
        pass
            