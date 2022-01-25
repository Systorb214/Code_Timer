from os import system, path, mkdir
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

    sessionTypes = ("Session", "Break")

    def __init__(self):
        currentDate = gmtime()

        currentYear = strftime("%Y", currentDate)
        currentMonth = strftime("%B", currentDate)
        currentDay = strftime("%d", currentDate)

        self.path = f"C:\\Users\\Clayton\\projects\\Code_Timer\\Coding_Sessions\\{currentYear}\\"
        self.filename = self.path + currentMonth + ".xml"

        dataFound = False
        if path.exists(self.filename):
            
            self.tree = ET.parse(self.filename)
            self.root = self.tree.getroot()
            dataFound = True
            
        else:
            if not path.exists(self.path):
                mkdir(self.path)

            self.root = ET.Element("Data")
            self.tree = ET.ElementTree(self.root)
            

        self.day = None
        #Linear search is faster than a binary search, because to do the latter, a list must first be created using the iter method.
        #Use findall instead?
        for ele in self.tree.iterfind("./Day"):
            stripped = ele.text.strip().strip("\\n")
            if stripped == currentDay:
                self.day = ele
                break
        
        if self.day == None:
            self.day = ET.Element("Day")
            self.day.text = currentDay
            self.root.append(self.day)
        else:
            dataFound = True

        self.codeSessions = {}
        self.breakSessions = {}

        #Loading found session data into dictionaries
        if dataFound:
            for ele in self.day.iter():
                if ele == self.day or ele.tag == "IntData" or ele.tag == "StringData":
                    continue

                data = (int(ele.find("./IntData").text), ele.find("./StringData").text)

                if ele.tag == Session.sessionTypes[0]:
                    self.codeSessions[ele.tag] = data

                elif ele.tag == Session.sessionTypes[1]:
                    self.breakSessions[ele.tag] = data

    def __str__(self):
        sessionStr = ""
        for count, time in self.codeSessions.items():
            sessionStr += f"{count}: {time[1]}\n"
        for count, time in self.breakSessions.items():
            sessionStr += f"{count}: {time[1]}\n"

        return sessionStr

    def AddSessionData(self, type, data):
        codeCount = len(self.codeSessions) + 1
        breakCount = len(self.breakSessions) + 1

        if type == Session.sessionTypes[0]:
            self.codeSessions[f"{Session.sessionTypes[0]}_{codeCount}"] = data
        elif type == Session.sessionTypes[1]:
            self.breakSessions[f"{Session.sessionTypes[0]}_{breakCount}"] = data
        else:
            raise TypeError(type)

    def WriteToXML(self):
        session = self.codeSessions
        for i in range(2):
            for count, time in session.items():
                sessionTime = ET.Element(count[:-2])
                sessionTime.text = count
                self.day.append(sessionTime)

                stringData = ET.Element("StringData")
                intData = ET.Element("IntData")

                sessionTime.append(stringData)
                sessionTime.append(intData)
                stringData.text = time[1]
                intData.text = str(time[0])
            
            session = self.breakSessions
        
        self.tree.write(self.filename)

class Stopwatch(Timer):
    
    def __init__(self):
        super().__init__()
        self.coding = True
        self.counter = 0
        self.totalCodeTime = 0

        self.stringTime = ""
        self.session = Session()

    def Count(self, print=True):
        if self.SecondPassed():
            self.counter += 1
            self.stringTime = self.ReadableTime(self.counter)
            if print:
                self.PrintElapsed()

    def PrintElapsed(self):
        system("cls")
        print(("coded for " if self.coding else "rested for ") + self.stringTime)

    def Control(self, type):
        if type == "code":

            self.coding = True

            if len(self.session.codeSessions) > 0:
                self.session.AddSessionData("Break", (self.counter, self.stringTime))

            self.counter = 0
        elif type == "break":

            self.coding = False

            self.session.AddSessionData("Session", (self.counter, self.stringTime))

            self.totalCodeTime += self.counter
            self.counter = 0
        else:
            raise TypeError(type)

    def End(self):
        #Append extra code session data
        if self.coding:
            self.session.AddSessionData("code", (self.counter, self.stringTime))

        self.counter = 0
        
        print(f"{self.session}Total time spent coding today: {self.ReadableTime(self.totalCodeTime)}.")

        self.session.WriteToXML()

        while self.counter < 10:
            self.Count(False)

stopWatch = Stopwatch()
start = "start"
stop = "stop"

#intro
while input(f"Type \"{start}\" to start the first coding session. When it's time for a break, enter \"{stop}\"\nWhen you are finished for the day, enter \"done.\"\n\n") != start:
    system("cls")

commands = WordListener()

lstnr = keyboard.Listener(on_press=commands.WordInput)

lstnr.start()
while True:
    stopWatch.Count()

    if commands.words[start]:
        stopWatch.Control("code")
        commands.words[start] = False

    elif commands.words[stop]:
        stopWatch.Control("break")
        commands.words[stop] = False

    elif commands.words["done"]:
        lstnr.stop()
        stopWatch.End()
        quit()