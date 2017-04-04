# ---------------------------------
# Libraries
# ---------------------------------
import serial
import time
import math
# ---------------------------------
# Setup
# ---------------------------------

# ---------------------------------
# Variables
# ---------------------------------
# Flags for tracking current tasks
flags = ["Initialized:False","Light On:False","Ping"]
# boolean flags for main code
comsUp = False
lightOn = False
# timing variables
t1 = 0
t2 = 0
# opens serial communication to arduino
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=None)
time.sleep(2) #sink up time for arduino
# ---------------------------------
# Functions for setting up
# ---------------------------------
def intializeCom():
    """Initializes Log file and checks serial coms
    """
    # inializes the log file for pi
    text_file = open("log.txt", "w")
    text_file.write("Raspberry Pi Log file for Robotic Arm Control \n\n")
    text_file.close()
    return boolArduCom(0)
# ---------------------------------
# Functions used when up and running
# ---------------------------------
def flipLightSwitch():
    """Changes the current state of the light
    """
    return boolArduCom(1)

# ---------------------------------
# helper functions
# ---------------------------------
def boolArduCom(flag):
    """Sends and recieves messages with arduino sends flag statments
       to beging certain functions
       :param flag:
       :return: bool
    """
    arduino.write(flags[flag])
    # waits for response from arduino
    while arduino.inWaiting() == 0:
        time.sleep(.1)
    # formates the data recieved and edits the flag array
    flags[flag] = (arduino.readline().rstrip('\r\n'))
    precursor, statement = flags[flag].split(':')
    # looks at the end part of the string sent which will always be a bool
    if statement == 'True':
        logCurrentInfo(flag)
        return True
    elif statement == 'False':
        logCurrentInfo(flag)
        return False
    else:
        return False

def pingArdu():
    """ Pings the arduino for current arduino status
        Alters:
        :return:
    """
    arduino.write("Ping")
    # waits for response from arduino
    while arduino.inWaiting() == 0:
        time.sleep(.1)
    dataRequested = (arduino.readline().rstrip('\r\n'))
    lightOn = dataRequested.split(',')
    logCurrentInfo(2)
    return

def logCurrentInfo(flag):
    """Logs data after a communication sequence
    """
    # logs data to an a pre intialized Log.txt file
    text_file = open("log.txt", "a")
    text_file.write(flags[flag] + " \n")
    text_file.close()
    return

# ---------------------------------
# Main Function
# ---------------------------------
# Intialization for communication
comsUp = intializeCom()
t1 = time()
while comsUp:
    t2 = time()
    if (t2-t1) >= 60: #exicute every minute
        lightOn = flipLightSwitch()
        t1 = time()
    