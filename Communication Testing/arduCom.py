#----------------------------------------------------------
#Libraries
import serial
import datetime
import smtplib
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
time.sleep(2) #may need to increase this time because of setup time
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
    # inializes the log file for pi
    text_file = open("log.txt", "w")
    text_file.write("Raspberry Pi Log file for Robotic Arm Control \n\n")
    text_file.close()
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
    
def logCurrentInfo():
    """Logs data after a communication sequence
    """
    # logs data to an a pre intialized Log.txt file
    text_file = open("log.txt", "a")
    text_file.write(str(datetime.datetime.now()) + ": \n")
    text_file.write(flags[0]+ flags[1] + " \n\n")
    text_file.close()
    return

def sendEmail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("darwinrpi13@gmail.com", "Darwin2017")

    msg = "YOUR MESSAGE!"
    server.sendmail("darwinrpi13@gmail.com", "reilyblackner@gmail.com", msg)
    server.quit()

# ---------------------------------
# Main Function
# ---------------------------------
# Intialization for communication
comsUp = intializeCom()
print(flags[0])

while comsUp:
    command = raw_input("Enter Command:(Light On, Ping, Exit)\n")
    if command == "Exit":
        break
    arduino.write(command)

    while (arduino.inWaiting() == 0):
        time.sleep(.1)

    s[0] = (arduino.readline().rstrip('\r\n'))
    print s[0]

    if s[0] == "Light On:True":
        flags[1] = s[0]
        print "The light is now on"
    elif s[0] == "Light On:False":
        flags[1] = s[0]
        print "The light is now off"
    elif s[0] == "Pinged":
        logCurrentInfo()
        print "Info loged"
sendEmail()