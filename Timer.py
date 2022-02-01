from time import time

class Timer:
    """
    Has some basic time-related methods.
    """

    def __init__(self):
        self._past = time()
        self.counter = 0

    def SecondPassed(self):
        """
        Returns true if a second has gone by.
        """
        if time() - self._past > 1:
            self._past = time()
            return True
        else:
            return False

    def Count(self):
        if self.SecondPassed():
            self.counter += 1

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
            raise TypeError(stringTime)

        totalInt = 0
        temp = ""
        for char in stringTime:
            if char.isdigit():
                temp += char
            elif temp != "":
                totalInt = int(temp)
                break
        
        minInt = totalInt * 60
        hourInt = totalInt * 3600

        if "minute" in stringTime:
            totalInt += minInt
        if "hour" in stringTime:
            totalInt += hourInt
        
        if totalInt != 0:
            return totalInt
        else:
            print("Hint: type something like \"30 minutes\" or \"2 hours.\"")
