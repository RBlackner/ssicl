#----------------------------------------------------------
#Libraries
import serial
import datetime
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
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
    text_file.write("Log file for light control \n\n")
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
    text_file.write(flags[0]+" "+flags[1]+" \n\n")
    text_file.close()
    return

def sendEmail():
    fromaddr = "darwinrpi13@gmail.com"
    toaddr = "reilyblackner1@gmail.com"

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log file from ssicl control system"

    body = ""

    msg.attach(MIMEText(body, 'plain'))

    filename = "log.txt"
    attachment = open("/home/pi/ssicl/Communication Testing/log.txt", "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "Darwin2017")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
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