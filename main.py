import sys
import pyfiglet
from time import sleep

from Histogram import Histogram
from Settings import Settings

from PIL import ImageGrab
from lifxlan import BLUE, GREEN, RED, CYAN, PINK, COLD_WHITE, LifxLAN

'''
MONITER_RES_WIDTH = 3840
MONITER_RES_HEIGHT = 2160

SCREENSHOT_WIDTH = 1500
SCREENSHOT_HEIGHT = 20
'''

settings = Settings().getSettingsObject()

def main():
    numLights = None

    if(len(sys.argv) != 2):
        print("\nDiscovery will go much faster if you provide the number of lights on your LAN:")
        print("i.e:")
        print("  sudo python3 {} <number of lights on LAN>\n" .format(sys.argv[0]))
    else:
        numLights = int(sys.argv[1])

    presentMenu(numLights)

'''
Simple method to present user with a menu of options

@param 
    numLights: number of lights on the LAN, simple pass along required by mimicScreen()
'''
def presentMenu(numLights):
    mainMenu = True
    title = pyfiglet.figlet_format("Vitzeno's LightRoom")

    while(mainMenu):
        print(title)
        print("\nSelect from the options below (and press enter) \n")
        print("1: Mimic Screen")
        print("2: Set lights manually")
        print("3: Settings")
        print("4: Quit")

        choice = input()
        if(int(choice) == 1):
            mainMenu = False
            mimicScreen(numLights)
        elif(int(choice) == 2):
            mainMenu = False
            pass
        elif(int(choice) == 3):
            mainMenu = False
            pass
        elif(int(choice) == 4):
            mainMenu = False
            pass

'''
Allows connected lights to mimic the colour of the users screen contents

@param 
    numLights: number of lights on the LAN
'''
def mimicScreen(numLights):
    '''
    LifxLAN client, number of lights be None (unknown), however providing the number of lights
    on the LAN will make discovery faster
    '''
    lifx = LifxLAN(numLights)

    # get device object and bulb
    devices = lifx.get_lights()
    bulb = devices[0]
    print("Selected {}".format(bulb.get_label()))
    initColour = getBulbColour(bulb)

    while True:
        try:
            colour = getScreenColour()
            setBulbColourInterpolated(bulb, colour, 15)
        except (KeyboardInterrupt):
            setBulbColour(bulb, initColour)
            break


'''
Uses PIL to get a screenshot on the main mointer,
tested to work with multi-moniter setups.
'''
def getScreenColour():
    # X1,Y1,X2,Y2
    image = ImageGrab.grab(bbox=(settings.MONITER_RES_WIDTH / 2 - settings.SCREENSHOT_WIDTH, settings.MONITER_RES_HEIGHT / 2 - settings.SCREENSHOT_HEIGHT, settings.MONITER_RES_WIDTH / 2 + settings.SCREENSHOT_WIDTH, settings.MONITER_RES_HEIGHT / 2 + settings.SCREENSHOT_HEIGHT))
    #image.save("test.png")

    hist = Histogram()
    hist.buildHistogram(image)

    hue = hist.getDominantHue()
    saturation = hist.getDominantSaturation()
    brightness = hist.getDominantBrightness()

    colour = [convertToLIFXFormat(hue), convertToLIFXFormat(saturation), convertToLIFXFormat(brightness), 6000]
    return colour

'''
Converts HSB values from range 0-100 to 0-65535 as expected by LIFX LAN protocol

@param 
    value: int or float to convert

@return 
    converted int or float
'''
def convertToLIFXFormat(value):
    return min(value/360 * 65535, 65535)

'''
A simple nunmber sacling method

@param
    value: value to scale int or float
    oldMax: max value of current scale range
    oldMin: min value of current scale range

    newMin: min value of new scale range
    newMax: max value of new scale range

@return 
    scaled int or float
'''
def scaled(value, oldMax, oldMin, newMin = 0, newMax = 65535):
    return (newMax - newMin) / (oldMax - oldMin) * (value - oldMax) + newMax

'''
Sets the bulb colour using LIFX LAN protocol, but interpolates smoothly between
the current colour and new colour. The step size determines how fast this
interploation shoul occur.

@param
    bulb: LIFX bulb object
    colour: HSBK colour array
    setps: int determinig interpolation speed
'''
def setBulbColourInterpolated(bulb, colour, steps):
    initColour = bulb.get_color()
    for i in range(0, steps):
        hsbk = [interpolate(initColour[0], colour[0], i + 1, steps), interpolate(initColour[1], colour[1], i + 1, steps), interpolate(initColour[2], colour[2], i + 1, steps), colour[3]]
        print("step: {0} value {1}" .format(i, hsbk))
        sleep(0.05)
        setBulbColour(bulb, hsbk)

'''
Interpolated between two values

@params
    startValue: start values
    endValue: end value to interpolate to
    stepNumber: number of steps interpolation should take
    lastStepNumber: totol number of steps

@return
    next value in interpolation step
'''
def interpolate(startValue, endValue, stepNumber, lastStepNumber):
    return (endValue - startValue) * stepNumber / lastStepNumber + startValue

'''
Simply sets the bulb colour using the LIFX LAN protocol

@param
    bulb: LIFX bulb object
    colour: HSBK colour array
'''
def setBulbColour(bulb, colour):
    bulb.set_color(colour, rapid=True)

'''
Simply gets the current bulb colour in HSB using LIFX LAN protocol

@param
    bulb: LIFX bulb object
'''
def getBulbColour(bulb):
    return bulb.get_color()

if __name__=="__main__":
    main()