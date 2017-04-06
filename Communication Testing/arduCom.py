#----------------------------------------------------------
#Libraries
import serial
import time
#----------------------------------------------------------
#Setup
# ---------------------------------
# Variables
# ---------------------------------
# Flags for tracking current tasks
flags = ["Initialized:False","Light On:False","Ping"]
# boolean flags for main code
comsUp = False
lightOn = False

# opens serial communication to arduino
arduino = serial.Serial('/dev/ttyACM0',9600,timeout = None)
s = [0]
#----------------------------------------------------------
#Links arduino to the raspberry pi
time.sleep(4) #may need to increase this time because of setup time
#----------------------------------------------------------

flags = ["Initialized:False","Light On:False","Ping"]
comsUp = False
lightOn = False

# ---------------------------------
# Functions for setting up
# ---------------------------------
def intializeCom():
    """Checks serial coms
    """
    return boolArduCom(0)

# ---------------------------------
# Helper functions
# ---------------------------------
def boolArduCom(flag):
    """Sends and recieves messages with arduino sends flag statments
       to beging certain functions
       :param: flag
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
        return True
    elif statement == 'False':
        return False
    else:
        return False

# ---------------------------------
# Main Function
# ---------------------------------
# Intialization for communication
comsUp = intializeCom()
print(flags[0])
'''
while comsUp:
    arduino.write(flags[1])

    while (arduino.inWaiting() == 0):
        time.sleep(.1)

    s[0] = (arduino.readline().rstrip('\r\n'))
    print s[0]

    if s[0] == "Light On:True":
        print "The light is now on"
    elif s[0] == "Light On:False":
        print "The light is now off"
    time.sleep(10)
'''