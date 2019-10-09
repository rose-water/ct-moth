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
# A light sensor outputs values in the range 0 - 4096, where
# 4096 is darkest and 0 is brightest. However in this circuit
# it is reversed, with 0 indicating lowest level of light and 
# higher numbers indicating higher levels of light. 
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
# For whatever reason my two servos, even though they're from 
# the same company, are not oriented the same way and their 0
# positions are opposite each other, hence one being 180 and 
# the other being 0.
def setRestingPosition():
    print("Setting resting position...")
    wingLeft.write_angle(180)
    wingRight.write_angle(0)


# ------------------------------------------------------------
def prepMoth():
    print("Prepping moth...")
    wingLeft.write_angle(0)
    wingRight.write_angle(0)
    time.sleep(5)

    setRestingPosition()
    time.sleep(5)
    print("Moth READY.")


# ------------------------------------------------------------
def runMoth():
    print("Initializing moth...")
    
    prepMoth()
    
    while True: 
        lightVal = adc.read()
        print("lightVal: " + str(lightVal))
        
        wingAngle = translate(lightVal, 3000, 4096, 0, 180)

        if wingAngle < 0:
            wingAngle = 0
        
        elif wingAngle > 180:
            wingAngle = 180
            
        wingLeft.write_angle(180 - wingAngle)
        wingRight.write_angle(wingAngle)
        
        print("rightWingAngle: " + str(wingAngle) + ", leftWingAngle: " + str(180 - wingAngle))
        
        time.sleep(0.25)

# ------------------------------------------------------------
runMoth()