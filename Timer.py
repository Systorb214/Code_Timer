from time import time

class Timer:
    """
    Has some basic time-related methods.
    """

    def __init__(self):
        self._past = time()

    def Update(self):
        self._past = time()

    def SecondPassed(self):
        """
        Returns true if a second has gone by.
        """
        if time() - self._past > 1:
            self.Update()
            return True
        else:
            return False

    def ReadableTime(self, seconds):

        seconds = int(seconds)
        minutes = 0
        hours = 0
        while seconds > 60:
            seconds -= 60
            minutes += 1
            
            while minutes > 60:
                minutes -= 60
                hours += 1

        info = ""
        
        if hours > 0:

            info += f"{hours} hours"

            if minutes > 0:
                info += f" and {minutes} minutes"
        elif minutes > 0:

            info += f"{minutes} minutes"

            if seconds > 0:
                info += f" and {seconds} seconds"
        else:
            info += f"{seconds} seconds"

        return info

    def GetTime(self, stringTime):
        """
        Gets a time (in seconds) from the string parameter. input something like "30 minutes" or "2 hours."
        """
        if type(stringTime) != str:
            return None
        intTime = 0
        temp = ""
        for char in stringTime:
            if char.isdigit():
                temp += char
            elif temp != "":
                intTime = int(temp)
                break

        if "minute" in stringTime:
            intTime *= 60
        elif "hour" in stringTime:
            intTime *= 3600
        
        if intTime != 0:
            return intTime
        else:
            print("Hint: type something like \"30 minutes\" or \"2 hours.\"")
