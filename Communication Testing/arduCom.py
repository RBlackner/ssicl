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
parallel = 300
perpendicular =200

positionData = str(parallel) + "," + str(perpendicular)


arduino.write(positionData)

while (arduino.inWaiting() == 0):
    time.sleep(.1)

s[0] = (arduino.readline().rstrip('\r\n'))
print s[0]

if s[0] == "Position Recieved":
    print "String interpreted correctly through serial"