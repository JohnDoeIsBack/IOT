import RPi.GPIO as GPIO
import time
import sys
import datetime
from hx711 import HX711
import urllib2

myAPI = "<INSERT YOUR API KEY HERE>"

myDelay = 15

def cleanAndExit():
    print "Cleaning up..."
    GPIO.cleanup()
    print "Exiting, Job Done!"
    sys.exit()

hx = HX711(5, 6)
hx.set_reference_unit(14)
hx.reset()
hx.tare()
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
print baseURL
while True:
    try:
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment the three lines to see what it prints.
        #np_arr8_string = hx.get_np_arr8_string()
        #binary_string = hx.get_binary_string()
        #print binary_string + " " + np_arr8_string
        
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        val = max(0, int(hx.get_weight(5)))
        print val
        
        conn = urllib2.urlopen(baseURL + '&field1=%s' % (val))
	print conn.read()
	print(datetime.datetime.now())
	# Closing the connection
	conn.close()
       # if (val>=85):
            #print "high value"
        #else:
       #     print "low value"  
        hx.power_down()
        hx.power_up()
        time.sleep(0.5)
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("LSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#hx.set_reference_unit(113)