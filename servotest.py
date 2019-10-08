import time
import machine
from servo import Servo

pin_1 = machine.Pin(27)  # GPIO 27
pin_2 = machine.Pin(4)   # GPIO 4
pin_34 = machine.Pin(34) # A2

servo_1 = Servo(pin_1)
servo_2 = Servo(pin_2)

adc = machine.ADC(pin_34)
adc.atten(machine.ADC.ATTN_11DB) 

lightVal = 0

servo_1.write_angle(0)
servo_2.write_angle(0)

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
while True: 

    lightVal = adc.read()
    print(lightVal)

    lightVal = translate(lightVal, 3200, 4096, 0, 90)

    servo_1.write_angle(lightVal)
    servo_2.write_angle(-lightVal)
    time.sleep(0.25)