import os
from platform import system
import xml.etree.ElementTree as ET
from pynput import keyboard
from time import gmtime, strftime
from Timer import Timer

class WordListener:
    
    def __init__(self):
        self.string = ""
        self.words = {"start" : False, "stop" : False, "done" : False}
    
    def WordInput(self, key=None):
        if key == keyboard.Key.enter:
            print(self.string)

            if self.string in self.words.keys():
                self.words[self.string] = True

            self.string = ""
        else:
            try:
                keyCh = key.char
            except:
                if key == keyboard.Key.space:
                    keyCh = ' '
                else:
                    keyCh = ''

            self.string += keyCh

class Session:

    sessionTypes = ("code", "break")

    def __init__(self):
        currentDate = gmtime()

        currentYear = strftime("%Y", currentDate)
        currentMonth = strftime("%B", currentDate)
        currentDay = strftime("%d", currentDate)

        self.path = f"C:\\Users\\Clayton\\projects\\Code_Timer\\Coding_Sessions\\{currentYear}\\"

        dataFound = False
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        try:
            self.tree = ET.parse(self.path + currentMonth)
            self.root = self.tree.getroot()
            dataFound = True
        except:
            self.root = ET.Element("Data")
            self.tree = ET.ElementTree(self.root)

        self.day = self.tree.find(currentDay)
        if self.day == None:
            self.day = ET.Element(currentDay)
            self.root.append(self.day)
        else:
            dataFound = True

        self.codeSessions = {}
        self.breakSessions = {}

        #Loading found session data into dictionaries
        if dataFound:
            for ele in self.day.iter():
                type = ele.get("type")
                data = (int(ele.find("IntData").text), ele.find("StringData").text)

                if type == Session.sessionTypes[0]:
                    self.codeSessions[ele.tag] = data

                elif type == Session.sessionTypes[1]:
                    self.breakSessions[ele.tag] = data

    def __str__(self):
        sessionStr = ""
        for i in self.codeSessions.values():
            sessionStr += i[1] + "\n"
        for i in self.breakSessions.values():
            sessionStr += i[1] + "\n"

        return sessionStr

    def AddSession(self, type, data):
        codeCount = len(self.codeSessions) + 1
        breakCount = len(self.breakSessions) + 1

        if type == Session.sessionTypes[0]:
            self.codeSessions[f"Session {codeCount}"] = data
        elif type == Session.sessionTypes[1]:
            self.breakSessions[f"Break {breakCount}"] = data
        else:
            raise TypeError(type)

class Stopwatch(Timer):
    
    def __init__(self):
        super().__init__()
        self.coding = False
        self.counter = 0
        self.stringTime = ""
        self.session = Session()

    def Count(self):
        if self.SecondPassed():
            self.counter += 1
            self.stringTime = self.ReadableTime(self.counter)
            self.PrintElapsed()

    def PrintElapsed(self):
        os.system("cls")
        print(("coded for " if self.coding else "rested for ") + self.stringTime)

    #control the timer variable and store elapsed time into lists
    def Control(self, type):
        if type == "code":

            self.coding = True

            if len(self.session.codeSessions) > 0:
                self.session.AddSession("break", (self.counter, self.stringTime))

            self.counter = 0
        elif type == "break":

            self.coding = False

            self.session.AddSession("code", (self.counter, self.stringTime))

            self.counter = 0
        else:
            raise TypeError(type)


stopWatch = Stopwatch()

#intro
while input("Type \"start\" to start the first coding session. When it's time for a break, enter \"stop.\"\nWhen you are finished for the day, enter \"done.\"\n\n") != "start":
    os.system("cls")

commands = WordListener()

lstnr = keyboard.Listener(on_press=commands.WordInput)

lstnr.start()
while True:
    stopWatch.Count()

    if commands.words["start"]:
        stopWatch.Control("code")
        commands.words["start"] = False

    elif commands.words["stop"]:
        stopWatch.Control("break")
        commands.words["stop"] = False
        
    elif commands.words["done"]:
        lstnr.stop()
        quit()


    


# while not timing:
#     continue

# while timing:
#     if time() > secondTimer+1:
#         secondTimer = time()
#         ticker += 1

#         os.system("cls")
        
#         activity = "Code" if sessionTimerRunning else "Break"

#         print(f"{activity} time: {ReadableTime(ticker)}")

# #Print the times elapsed
# print("Total time spent coding today: " + ReadableTime(totalTime))

# print(self.session)

# input("\nPress enter to quit")

#Storing session data in files
# for count, timed in sessionTimes.items():
#     sessionTime = ET.Element(count)
#     dayElement.append(sessionTime)

#     stringData = ET.Element("StringData")
#     intData = ET.Element("IntData")

#     sessionTime.append(stringData)
#     sessionTime.append(intData)
#     stringData.text = timed[1]
#     intData.text = str(timed[0])

# tree.write(filePath + currentMonth + ".xml")