import time
import machine

from servo import Servo

# ------------------------------------------------------------
# PIN SETUP
# ------------------------------------------------------------
# Servos
pin1 = machine.Pin(4)  # GPIO 4
pin2 = machine.Pin(27) # GPIO 27

wingLeft = Servo(pin1)
wingRight = Servo(pin2)

# Vibrating motor
pin21 = machine.Pin(21, machine.Pin.OUT) 
pin21.value(0)

# Light sensor
# Outputs values in the range 0 - 4096, where 4096 is darkest, 0 
# is brightest. However here it is reversed, with 0 indicating 
# lowest level of light. 
pin34 = machine.Pin(34) # A2
adc = machine.ADC(pin34)
adc.atten(machine.ADC.ATTN_11DB)

lightVal = 0

# MOTH FEELS!
excitementLevel = 0
hungerLevel = 0

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
def translateInverse(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    valueScaled = 1 - valueScaled

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


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
# The higher the level of light the more rapidly the moth's
# wings should flap (meaning the delay should be less). 0.35 
# seems to the the lowest amount we can do comfortably when 
# going from 0 to 180.
def flapBasedOnExcitement(lightLevel):
    delayMin = 0.35
    delayMax = 1.0

    delayAmt = translateInverse(lightLevel, 3300, 4096, delayMin, delayMax)
    delayAmt = float(str(round(delayAmt, 2)))

    if delayAmt < delayMin:
        delayAmt = delayMin
    
    elif delayAmt > delayMax:
        delayAmt = delayMax

    wingAngle = translate(lightLevel, 3300, 4096, 0, 180)

    if wingAngle < 0:
        wingAngle = 0
    
    elif wingAngle > 180:
        wingAngle = 180

    wingAngle = int(wingAngle)

    print("delayAmt: " + str(delayAmt))
    print("wingAngle: " + str(wingAngle))

    wingLeft.write_angle(180) 
    wingRight.write_angle(0)
    pin21.value(1)
    time.sleep(delayAmt)

    wingLeft.write_angle(180 - wingAngle)
    wingRight.write_angle(wingAngle)
    pin21.value(0)
    time.sleep(delayAmt)


# ------------------------------------------------------------
# A test function, opens wings (moves servos) in proportion to
# level of light being read by the sensor
def spreadWingsByLight(lightLevel):
    wingAngle = translate(lightLevel, 3300, 4096, 0, 180)

    if wingAngle < 0:
        wingAngle = 0
    
    elif wingAngle > 180:
        wingAngle = 180

    wingLeft.write_angle(180 - wingAngle)
    wingRight.write_angle(wingAngle)
    
    print("rightWingAngle: " + str(wingAngle) + ", leftWingAngle: " + str(180 - wingAngle))
    
    time.sleep(0.25)


# ------------------------------------------------------------
def runMoth():
    print("Initializing moth...")
    prepMoth()

    while True:

        lightVal = adc.read()
        # spreadWingsByLight(lightVal)
        flapBasedOnExcitement(lightVal)
    

# ------------------------------------------------------------
runMoth()
pin21.value(0)