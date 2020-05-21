import sys
from time import sleep

from Histogram import Histogram

from PIL import ImageGrab
from lifxlan import BLUE, GREEN, RED, CYAN, PINK, COLD_WHITE, LifxLAN

MONITER_RES_WIDTH = 3840
MONITER_RES_HEIGHT = 2160

# On a 16:9 4k moniter this should produce a centered 1600x900 screenshot
SCREENSHOT_WIDTH = 800
SCREENSHOT_HEIGHT = 450

def main():
    numLights = None

    if(len(sys.argv) != 2):
        print("\nDiscovery will go much faster if you provide the number of lights on your LAN:")
        print("i.e:")
        print("  sudo python3 {} <number of lights on LAN>\n" .format(sys.argv[0]))
    else:
        numLights = int(sys.argv[1])

    '''
    LifxLAN client, number of lights be None (unknown), however providing the number of lights
    on the LAN will make discovery faster
    '''
    lifx = LifxLAN(numLights)

    # get device object and bulb
    devices = lifx.get_lights()
    bulb = devices[0]
    print("Selected {}".format(bulb.get_label()))

    while True:
        try:
            colour = getScreenColour()
            setBulbColour(bulb, colour)
        except (KeyboardInterrupt):
            setBulbColour(bulb, [0.0, 0.0, 65535, 3500])
            break

'''
Uses PIL to get a screenshot on the main mointer,
tested to work with multiple moniters.

Not very generic, hardcoded values on work on my moniter
with resolution of 3840x2160
'''
def getScreenColour():
    image = ImageGrab.grab(bbox=(MONITER_RES_WIDTH / 2 - SCREENSHOT_WIDTH, MONITER_RES_HEIGHT / 2 - SCREENSHOT_HEIGHT, MONITER_RES_WIDTH / 2 + SCREENSHOT_WIDTH, MONITER_RES_HEIGHT / 2 + SCREENSHOT_HEIGHT))  # X1,Y1,X2,Y2
    pixels = image.load()
    #image.save("test.png")

    hist = Histogram()
    hist.buildHistogram(image)
    #hist.printHistogram()

    hue = hist.getDominantHue()
    saturation = hist.getDominantSaturation()

    colour = [convertToLIFXFormat(hue), convertToLIFXFormat(saturation), 65535, 3500]
    print("Colour: ", colour)
    return colour

def convertToLIFXFormat(value):
    return min(value/360 * 65535, 65535)

def scaled(value, oldMax, oldMin):
    oldMin = oldMin
    oldMax = oldMax
    newMin = 0
    newMax = 65535

    return (newMax - newMin) / (oldMax - oldMin) * (value - oldMax) + newMax

def setBulbColour(bulb, colour):
    bulb.set_color(colour, rapid=True)

def getBulbColour(bulb):
    return bulb.get_color()

if __name__=="__main__":
    main()