from time import gmtime, strftime
from os import system, path, mkdir
import time
from win32gui import GetWindowText, GetForegroundWindow
import xml.etree.ElementTree as ET
from pynput import keyboard
from Timer import Timer
from playsound import playsound

class WordListener:
    """
    Provides word functionality for the keyboard listener.
    """
    consoleWindow = GetWindowText(GetForegroundWindow())
    
    def __init__(self):
        self._stringBuffer = ""
        """The string that WordInput adds characters to."""

        self._string = ""
        """the string variable's previous value."""

    @property
    def string(self):
        """The last string that was typed."""
        return self._string

    def ResetString(self):
        """Resets the string property."""
        self._string = ""
    
    def WordInput(self, key=None):
        """
    Adds pressed keys to a string.\nIf enter is pressed, set the string property.
        """
        if GetWindowText(GetForegroundWindow()) != WordListener.consoleWindow:
            return
        
        if key == keyboard.Key.enter:
            print(self._stringBuffer)

            self._string = self._stringBuffer
            self._stringBuffer = ""
        else:
            try:
                keyChar = key.char
            except:
                if key == keyboard.Key.space:
                    keyChar = ' '
                else:
                    keyChar = ''

            self._stringBuffer += keyChar

class Session:

    sessionTypes = ("Session", "Break")

    def __init__(self):
        currentDate = gmtime()

        currentYear = strftime("%Y", currentDate)
        currentMonth = strftime("%B", currentDate)
        currentDay = strftime("%d", currentDate)

        sessionsPath = "./Coding_Sessions"
        pathToCurrentYear = f"{sessionsPath}/{currentYear}/"
        self.pathToXml = pathToCurrentYear + currentMonth + ".xml"

        if path.exists(self.pathToXml):
            self.tree = ET.parse(self.pathToXml)
            self.root = self.tree.getroot()
            
        else:
            if not path.exists(sessionsPath):
                mkdir(sessionsPath)
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

        #Anything written to the xml MUST BE A STRING!
        ttElement.text = str(self.totalSessionTime)
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

        self.tree.write(self.pathToXml)


commands = WordListener()
lstnr = keyboard.Listener(on_press=commands.WordInput)

timer = Timer()
session = Session()

alarm_sounds = ["./Sounds/Start_Coding.mp3", "./Sounds/Stop_coding.mp3", "./Sounds/Look_away.mp3", "./Sounds/Look_back.mp3"]
alarm_times = [900, 3600, 1200, 20]


lstnr.start()
print(f"Type \"start\" to start the first coding session. When it's time for a break, enter \"stop\"\nWhen you are finished for the day, enter \"done\"\n\n")
while "start" not in commands.string:
    timer.Count()
timer.Reset()

t = timer.GetTime(commands.string)
if t != 0:
    alarm_times[0] = t
del t

commands.ResetString()
coding = True
status = "coding"
looking_away = False

while True:
    timer.Count()
    print("\r" + status + (". " if timer.counter % 2 == 0 else ".."), end="")

    if not looking_away and timer.counter % alarm_times[2] == 0:
        looking_away = True
        playsound(alarm_sounds[2])
    
    elif looking_away and timer.counter % alarm_times[3] == 0:
        looking_away = False
        playsound(alarm_sounds[3])

    if coding == False:
        if timer.counter % alarm_times[0] == 0:
            playsound(alarm_sounds[0])
            alarm_times[0] = 5
        
        if "start" in commands.string:
            system("cls")
            coding = True
            status = "coding"

            alarm_times[0] = timer.GetTime(commands.string)
            if alarm_times[0] == 0:
                alarm_times[0] = 3600

            commands.ResetString()

            result_time = timer.counter
            timer.Reset()

            if len(session.codeSessions) > 0:
                session.AddSessionData(False, (result_time, timer.ReadableTime(result_time)))

    elif coding == True:
        if timer.counter % alarm_times[1] == 0:
            playsound(alarm_sounds[1])
            alarm_times[1] = 5

        if "stop" in commands.string:
            system("cls")
            coding = False
            status = "taking a break"

            alarm_times[1] = timer.GetTime(commands.string)
            if alarm_times[1] == 0:
                alarm_times[1] = 900

            commands.ResetString()

            result_time = timer.counter
            timer.Reset()
            session.AddSessionData(True, (result_time, timer.ReadableTime(result_time)))

    if "done" in commands.string:
        lstnr.stop()
        if coding:
            session.AddSessionData(True, (result_time, timer.ReadableTime(result_time)))

        timer.Reset()
        
        print(f"{session}Total time spent coding today: {timer.ReadableTime(session.totalSessionTime)}.")

        session.WriteToXML()

        while timer.counter < 10:
            timer.Count()
        quit()