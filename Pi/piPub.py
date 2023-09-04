
import wiotp.sdk.application
from time import sleep      
import wiotp.sdk.application
import warnings
warnings.filterwarnings('ignore')
import random
import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711

# calibrated reference
referenceUnit = -1123

def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    sys.exit()

# DOUT - GPIO 5
# SCLK - GPIO 6
hx = HX711(5, 6)

# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#hx.set_reference_unit(113)
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Connection successful. Ready to collect the sensor weight values!")
print("Tare done! Add weight now...")


def tea_powder():
    #Pi tea powder sensor code
    f2 = open('tea_powder.txt')
    val = f2.readline()
    return int(val)
    # return random.randint(100, 500)

def coffee_powder():
    #Pi coffee powder sensor code
    # return random.randint(25, 45)
    # Prints the weight.
    val = hx.get_weight(5)
    # print("Coffee powder from sensor", val)

    hx.power_down()
    hx.power_up()
    time.sleep(0.1)
    return int(val)

def milk():
    #Pi milk sensor code
    # return random.randint(100, 500)
    f2 = open('milk.txt')
    val = f2.readline()
    return int(val)

def sugar():
    #Pi sugar sensor code
    # return random.randint(100, 500)
    f2 = open('sugar.txt')
    val = f2.readline()
    return int(val)

options = wiotp.sdk.application.parseConfigFile("application.yaml")
client = wiotp.sdk.application.ApplicationClient(config=options)
client.connect()

prev_values = {"Milk": str(milk()), 
                "Sugar": str(sugar()), 
                "Coffee powder": str(coffee_powder()),
                "Tea powder": str(tea_powder())}

while True:
    inventory = {"Milk": str(milk()), 
                "Sugar": str(sugar()), 
                "Coffee powder": str(coffee_powder()),
                "Tea powder": str(tea_powder())}
    try:
        data = {
            "time" : time.time(),
            "state": "active"
        }
        client.publishEvent(typeId="RaspberryPi", deviceId="1", eventId="pi_status", msgFormat="json", data={'state':data})
        print(data)
        if any(prev_values[key] != inventory[key] for key in prev_values.keys()):
            success = client.publishEvent(typeId="RaspberryPi", deviceId="1", eventId="weight_status", msgFormat="json", data={'state':inventory})
            print(inventory)
            if success:
                print("Successfully published to the Cloud")
            prev_values = inventory
        sleep(10)
    except Exception as e:
        print("Exception: ", e)