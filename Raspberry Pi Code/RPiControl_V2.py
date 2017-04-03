# Required python Libraries
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
flags = ["Initialized:False"]
# boolean flags for main code
comsUp = False
calibrated = False
wireFound = False
# position variables
parallel_pos = [0, 0]  # steps
perpendicular_pos = [0, 0]  # steps
angle = 0  # degrees
# constants
offsetForHook = 30
halfCard = 22
lengthCar = 80
# opens serial communication to arduino
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=None)
time.sleep(2)
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
    # formates the data recieved
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
        # TODO: Add in an error message if the arm gets past its range
        return False
def posArduCom(flag, parallel, perpendicular):
    """Communicates with the arduino. Sends desired position 
       data to arduio once the move is complete it updates the
       position
       :param flag:
       :param parallel:
       :param perpendicular:
       :return:
    """
    dataToSend = "Move To:" + str(parallel) + "," + str(perpendicular)
    arduino.write(dataToSend)
    # waits for response from arduino
    while arduino.inWaiting() == 0:
        time.sleep(.1)

    # formates the data recieved
    flags[flag] = (arduino.readline().rstrip('\r\n'))
    precursor, statement = flags[flag].split(':')
    # looks at the end part of the string sent which will always be a bool
    if statement == 'True':
        parallel_pos[1] = parallel_pos[0]
        perpendicular_pos[1] = perpendicular_pos[0]
        parallel_pos[0] = parallel
        perpendicular_pos[0] = perpendicular
        logCurrentInfo(flag)
        return True
    else:
        logCurrentInfo(flag)
        return False
def pingArdu():
    """ Pings the arduino for current parallel postion, 
        perpendicular position, angle of wire
        Alters:angle and position values
        :return:
    """
    arduino.write("Ping")
    # waits for response from arduino
    while arduino.inWaiting() == 0:
        time.sleep(.1)
    dataRequested = (arduino.readline().rstrip('\r\n'))
    parallel, perpendicular, ang = dataRequested.split(',')
    parallel_pos[0] = int(parallel)
    perpendicular_pos[0] = int(perpendicular)
    angle = int(ang)
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
# noinspection PyRedeclaration
comsUp = intializeCom()
while comsUp:
    calibrated = calibrateArdu()
    while comsUp and calibrated:
        wireFound = scanForWire()
        if wireFound:
            setUpForHook()
