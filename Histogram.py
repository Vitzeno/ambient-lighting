import operator

'''
Histogram class, this will be used to find the dominante colour of a given image 
in terms of Hue.
'''
class Histogram:

    '''
    Initialises a dictionary which represents the histogram
    '''
    def __init__(self):
        self.histogram = dict()
        self.shistogram = dict()

        for i in range(0, 361):
            self.histogram[i] = 0
        for i in range(0, 101):
            self.shistogram[i] = 0

    '''
    Provided an image, this method populates the hue valeus in the 
    histogram
    '''
    def buildHistogram(self, image):
        width, height = image.size
        pixel = image.load()
        for i in range(0, width):
            for j in range (0, height):
                hsbvals = self.convertRGBtoHSB(pixel[i, j][0], pixel[i, j][1], pixel[i, j][2])
                #print(hsbvals)
                self.histogram[round(hsbvals[0])] += 1
                self.shistogram[round(hsbvals[1])] += 1
    
    '''
    Returns the hue value with the maximum peak in the hue histogram
    '''
    def getDominantHue(self):
        return max(self.histogram.items(), key=operator.itemgetter(1))[0]
    
    '''
    Returns the saturation value with the maximum peak in the saturation histogram
    '''
    def getDominantSaturation(self):
        return max(self.shistogram.items(), key=operator.itemgetter(1))[0]

    '''
    Convers a colour given in seprate r g b vaues into hsb format
    and returns an array containing hue, saturation and brightness
    '''
    def convertRGBtoHSB(self, r, g, b):
        if(r > g):
            cmax = r
        else:
            cmax = g
        if(b > cmax):
            cmax = b
        
        if(r < g):
            cmin = r
        else:
            cmin = g
        if(b < cmin):
            cmin = b
        
        brightness = cmax / 255.0
        if(cmax != 0):
            saturation = (cmax - cmin) / cmax
        else:
            saturation = 0
        
        if(saturation == 0):
            hue = 0
        else:
            redc = (cmax - r) / (cmax - cmin)
            greenc = (cmax - g) / (cmax - cmin)
            bluec = (cmax - b) / (cmax - cmin)

            if(r == cmax):
                hue = bluec - greenc
            elif(g == cmax):
                hue = 2.0 + redc - bluec
            else:
                hue = 4.0 + greenc - redc
            
            hue = hue / 6.0
            if(hue < 0):
                hue = hue + 1.0
    
        hsbvals = [hue * 360, saturation * 100, brightness * 100]
        return hsbvals

    '''
    Prints histogram
    '''
    def printHistogram(self):
        for x, y in self.histogram.items():
            print("Key: {0}, Value {1}" .format(x, y))