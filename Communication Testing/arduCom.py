#----------------------------------------------------------
#Libraries
import serial
import time
#----------------------------------------------------------
#Setup
arduino = serial.Serial('/dev/ttyACM0',9600,timeout = None)
s = [0]
#----------------------------------------------------------
#Links arduino to the raspberry pi
time.sleep(2) #may need to increase this time because of setup time
#----------------------------------------------------------
#Test Code
arduino.write("Light On:False")

while (arduino.inWaiting() == 0):
    time.sleep(.1)

s[0] = (arduino.readline().rstrip('\r\n'))
print s[0]

if s[0] == "Light On:True":
    print "The light is now on"
elif s[0] == "Light On:False":
    print "The light is now off"
time.sleep(5)