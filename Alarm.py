from Timer import Timer

class Alarm(Timer):
    def __init__(self, alarmTime=3600):
        self.alarmTime = alarmTime