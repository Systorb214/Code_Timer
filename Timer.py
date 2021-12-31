import keyboard
from time import time, gmtime, strftime
import os

timer = 0
ticker = 0
sessionTimes = []
breakTimes = []
sessionTimerRunning = True
timing = False

def ReadableTime(seconds):

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

def GetTime(stringTime):
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

toggleTimerType = "page up"
toggleTimer = "page down"

#control the timer variable and store elapsed time into lists
def ControlTimer(event):
    global sessionTimerRunning
    global timer
    global ticker
    global timing
    elapsed = time() - timer

    if event.name == toggleTimerType:
        if sessionTimerRunning:
            
            sessionTimes.append(ReadableTime(elapsed))

            sessionTimerRunning = False
        elif not sessionTimerRunning:
            
            if timer != 0: breakTimes.append(ReadableTime(elapsed))

            sessionTimerRunning = True

        timer = time()
        ticker = 0
    elif event.name == toggleTimer:
        if timing:
            if sessionTimerRunning:
                
                sessionTimes.append(ReadableTime(elapsed))

                sessionTimerRunning = False

            timing = False
        else:
            timing = True
            timer = time()
        ticker = 0

keyboard.on_press(ControlTimer)

secondTimer = time()

#intro
print(f"Push \"{toggleTimerType}\" to toggle between the session timer and the break timer.\nOnce you're \
finished coding for the day, press \"{toggleTimer}\".\nPress \"{toggleTimer}\" to begin!")

while not timing:
    continue

while timing:
    if time() > secondTimer+1:
        secondTimer = time()
        ticker += 1

        os.system("cls")
        
        activity = "Code" if sessionTimerRunning else "Break"

        print(f"{activity} time: {ReadableTime(ticker)}")

#Print the times elapsed
for i in range(len(sessionTimes)):
    
    print(f"Session {i+1}: {sessionTimes[i]}.")

for i in range(len(breakTimes)):

    print(f"Break {i+1}: {breakTimes[i]}.")

#Storing session data in files
filePath = "C:\\Users\\Clayton\\projects\\Code_Timer\\Coding_Sessions\\"

currentDate = gmtime()

currentYear = strftime("%Y", currentDate)
currentMonth = strftime("%B", currentDate)

datePath = f"{currentYear}\\{currentMonth}"

if not os.path.exists(filePath + datePath):
    os.makedirs(filePath + datePath)