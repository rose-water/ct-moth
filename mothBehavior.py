import time
import machine

from servo import Servo

# ------------------------------------------------------------
# SETUP
# ------------------------------------------------------------
# Servo setup
pin1 = machine.Pin(4)  # GPIO 4
pin2 = machine.Pin(27) # GPIO 27

wingLeft = Servo(pin1)
wingRight = Servo(pin2)

# Light sensor setup
pin34 = machine.Pin(34) # A2
adc = machine.ADC(pin34)
adc.atten(machine.ADC.ATTN_11DB)

lightVal = 0

# ------------------------------------------------------------
# https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + int(valueScaled * rightSpan)


# ------------------------------------------------------------
def setRestingPosition():
    print("[ setRestingPosition ]")
    wingLeft.write_angle(-45)
    wingRight.write_angle(45)


# ------------------------------------------------------------
def prepMoth():
    print("[ prepMoth ]")
    wingLeft.write_angle(0)
    wingRight.write_angle(0)
    time.sleep(10)
    setRestingPosition()
    time.sleep(10)
    print("Moth READY")

# ------------------------------------------------------------
# A light sensor outputs values in the range 0 - 4096, where
# 4096 is darkest and 0 is brightest. However in this circuit
# it is reversed, with 0 indicating lowest level of light and 
# higher numbers indicating higher levels of light. 
#
# We want the moth's wings to be more open and flutter more
# rapidly with more light, indicating happiness, and to be 
# closed with the lowest amount of light.
# ------------------------------------------------------------

prepMoth()

while True: 

    lightVal = adc.read()
    print("lightVal: " + str(lightVal))

    rightWingAngle = translate(lightVal, 1900, 4096, 0, 90)
    leftWingAngle = translate(lightVal, 1900, 4096, 0, 90)

    wingLeft.write_angle(-leftWingAngle)
    wingRight.write_angle(rightWingAngle)
    
    time.sleep(0.25)

