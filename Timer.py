from time import time

class Timer:
    """
    Has some basic time-related methods.
    """

    def __init__(self):
        self.past = time()
        self.counter = 0

    def SecondPassed(self):
        """
        Returns true if a second has gone by.
        """
        if time() - self.past > 1:
            self.past = time()
            return True
        else:
            return False

    def Count(self):
        """If a second has passed, increments the counter and returns True."""
        if self.SecondPassed():
            self.counter += 1
            return True
        return False

    def Reset(self):
        """Resets the counter to 0."""
        self.counter = 0

    def ReadableTime(self, seconds):

        seconds = int(seconds)
        minutes = 0
        hours = 0
        while seconds >= 60:
            seconds -= 60
            minutes += 1
            
            while minutes >= 60:
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

        #If I input anything over 60 it's an accident
        if totalInt >= 60 or totalInt < 0:
            return 5
        
        minInt = totalInt * 60
        hourInt = totalInt * 3600

        if "minute" in stringTime:
            totalInt += minInt
        if "hour" in stringTime:
            totalInt += hourInt
        
        return totalInt
