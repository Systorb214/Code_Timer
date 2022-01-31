from Timer import Timer
import playsound

class Alarm(Timer):

    startSound = "./Sounds/Start_coding.mp3"
    stopSound = "./Sounds/Stop_coding.mp3"
    def __init__(self, alarmTime=3600):
        self.alarmTime = alarmTime