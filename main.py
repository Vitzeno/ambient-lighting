import sys
from time import sleep

from lifxlan import BLUE, GREEN, RED, CYAN, PINK, COLD_WHITE, LifxLAN

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

    # get bulb state
    initPower = bulb.get_power()
    initColour = bulb.get_color()

    print("Init colour: {0}" .format(initColour))
    print("Blue colour: {0}" .format(BLUE))

    bulb.set_color(BLUE, rapid=True)
    input("Press Enter to continue...")
    bulb.set_color(RED, rapid=True)
    input("Press Enter to continue...")
    bulb.set_color(GREEN, rapid=True)
    input("Press Enter to continue...")
    bulb.set_color(CYAN, rapid=True)
    input("Press Enter to continue...")
    bulb.set_color(PINK, rapid=True)
    input("Press Enter to continue...")
    bulb.set_color(initColour, rapid=True)
    input("Press Enter to continue...")



if __name__=="__main__":
    main()