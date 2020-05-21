# Ambient Lighting

This project makes using of lifxlan library which immplemts the LIFX LAN protocol to control LIFX B22 light bulbs, it also uses PIL to grab screenshots of the main moniter. The domient colour of this screenshot is then conveted from RGB to HSBK and sent to the bulb.

## Demo Video

![](/AmbientLighting.mp4)

## Warning

This project uses PIL and the ImageGrab module, this module only works on windows.