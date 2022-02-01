from time import gmtime, strftime
from os import path, mkdir
import xml.etree.ElementTree as ET
from pynput import keyboard
from Stopwatch import Stopwatch, system
from Alarm import Alarm

class WordListener:
    """
    Provides word functionality for the keyboard listener.
    """
    
    def __init__(self):
        self.string = ""
        """The string that WordInput adds characters to."""

        self.words = {"start" : False, "stop" : False, "done" : False}
        """Words to listen for."""
    
    def WordInput(self, key=None):
        """
    Adds pressed keys to a string.\nIf enter is pressed and the string matches one of the word listener's words, set that word's value to true.
        """
        if key == keyboard.Key.enter:
            print(self.string)

            if self.string in self.words.keys():
                self.words[self.string] = True

            self.string = ""
        else:
            try:
                keyChar = key.char
            except:
                if key == keyboard.Key.space:
                    keyChar = ' '
                else:
                    keyChar = ''

            self.string += keyChar

    def WordFound(self, word):
        """
        Returns True if the command has been typed.
        """
        if word in self.words.keys():
            if self.words[word] == True:
                self.words[word] = False
                return True

            return False
        else:
            raise ValueError(word)

class Session:

    sessionTypes = ("Session", "Break")

    def __init__(self):
        currentDate = gmtime()

        currentYear = strftime("%Y", currentDate)
        currentMonth = strftime("%B", currentDate)
        currentDay = strftime("%d", currentDate)

        pathToCurrentYear = f"~/Coding_Sessions/{currentYear}/"
        self.pathToXml = pathToCurrentYear + currentMonth + ".xml"

        if path.exists(self.pathToXml):
            self.tree = ET.parse(self.pathToXml)
            self.root = self.tree.getroot()
            
        else:
            if not path.exists(pathToCurrentYear):
                mkdir(pathToCurrentYear)

            self.root = ET.Element("Data")
            self.tree = ET.ElementTree(self.root)

        self.day = None
        dayFound = False
        #searching for the current day in the xml
        for ele in self.tree.iterfind("./Day"):
            stripped = ele.text.strip().strip("\\n")
            if stripped == currentDay:
                self.day = ele
                dayFound = True
                break
        
        #If there is no day element equal to the current day, create a new one.
        if self.day == None:
            self.day = ET.Element("Day")
            self.day.text = currentDay
            self.root.append(self.day)
            
        self.codeSessions = {}
        self.breakSessions = {}

        self.codeCount = 0
        self.breakCount = 0
        self.totalSessionTime = 0

        #Getting session and break count
        if dayFound:
            for ele in self.day.iter():
                if ele.tag == Session.sessionTypes[0]:
                    self.codeCount += 1
                    self.totalSessionTime += int(ele.find("IntData").text)

                elif ele.tag == Session.sessionTypes[1]:
                    self.breakCount += 1

    def __str__(self):
        sessionStr = ""
        for count, time in self.codeSessions.items():
            sessionStr += f"{count}: {time[1]}\n"
        for count, time in self.breakSessions.items():
            sessionStr += f"{count}: {time[1]}\n"

        return sessionStr

    def AddSessionData(self, codeSession, data):

        if codeSession:
            self.codeCount += 1
            self.totalSessionTime += data[0]
            self.codeSessions[f"{Session.sessionTypes[0]}_{self.codeCount}"] = data
        else:
            self.breakCount += 1
            self.breakSessions[f"{Session.sessionTypes[1]}_{self.breakCount}"] = data

    def WriteToXML(self):
        #Append the total time of all sessions to the day element
        ttElement = ET.Element("TotalTime")
        ttElement.text = self.totalSessionTime
        self.day.append(ttElement)

        #Loop over the code sessions
        session = self.codeSessions
        for i in range(2):
            for count, time in session.items():
                #Add the session element
                sessionTime = ET.Element(Session.sessionTypes[i])
                sessionTime.text = count
                self.day.append(sessionTime)

                #StringData is the session time in string format
                stringData = ET.Element("StringData")
                #IntData is the session time in int format
                intData = ET.Element("IntData")
                stringData.text = time[1]
                intData.text = str(time[0])

                sessionTime.append(stringData)
                sessionTime.append(intData)
            
            #Switch to break sessions and loop over those
            session = self.breakSessions
        
        #BUG: This isn't working
        self.tree.write(self.pathToXml)


stopWatch = Stopwatch()
session = Session()
coding = False

#intro
while input(f"Type \"start\" to start the first coding session. When it's time for a break, enter \"stop\"\nWhen you are finished for the day, enter \"done\"\n\n") != "start":
    system("cls")

commands = WordListener()

lstnr = keyboard.Listener(on_press=commands.WordInput)

print("Beginning session!")
lstnr.start()
while True:
    stopWatch.Count()
    if stopWatch.MinutePassed():
        stopWatch.ReadableTime(stopWatch.counter)

    if commands.WordFound("start"):
        if coding:
            continue
        coding = True
        stopWatch.Reset()
        print("Beginning session!")

        if len(session.codeSessions) > 0:
            session.AddSessionData(False, (stopWatch.resultTime, stopWatch.stringTime))

    elif commands.WordFound("stop"):

        coding = False
        stopWatch.Reset()
        print("Taking a break...")
    
        session.AddSessionData(True, (stopWatch.resultTime, stopWatch.stringTime))

    elif commands.WordFound("done"):
        lstnr.stop()
        if coding:
            session.AddSessionData(True, (stopWatch.resultTime, stopWatch.stringTime))

        stopWatch.Reset()
        
        print(f"{session}Total time spent coding today: {stopWatch.ReadableTime(session.totalSessionTime)}.")

        session.WriteToXML()

        while stopWatch.counter < 10:
            stopWatch.Count()
        quit()