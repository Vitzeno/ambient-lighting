import Serialise as Serialise

def Singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@Singleton
class Settings:
    FILE_DIR = "config/"
    FILE_NAME = "config.txt"

    '''
    Downscaling filters

    Image.NEAREST   (0)
    Image.LANCZOS   (1)
    Image.BILINEAR  (2)
    Image.BICUBIC   (3) 
    Image.BOX       (4)
    Image.HAMMING   (5)
    '''

    def __init__(self):
        print("[DEBUG] Init singleton settings object")
        self.MONITER_RES_WIDTH = 3840
        self.MONITER_RES_HEIGHT = 2160
        self.SCREENSHOT_WIDTH = 1500
        self.SCREENSHOT_HEIGHT = 20
        self.title = "Vitzeno's LightRoom"
        self.downsacling_quality = 0
        self.transition_steps = 5
    
    def setUpDefaultData(self):
        self.MONITER_RES_WIDTH = 3840
        self.MONITER_RES_HEIGHT = 2160
        self.SCREENSHOT_WIDTH = 1500
        self.SCREENSHOT_HEIGHT = 20
        self.title = "Vitzeno's LightRoom"
        self.downsacling_quality = 0
        self.transition_steps = 5

    '''
    Init the settings list JSON file and write to disk, default parameters are used
    '''
    def initSettingsList(self):
        print("[DEBUG] Init settings and write to file")
        try:
            self.setUpDefaultData()
            Serialise.serialiseObjectToFile(self, self.FILE_NAME, self.FILE_DIR)
        except (IOError, OSError, FileNotFoundError) as e:
            print("[DEBUG] Failed to init {0}" .format(self.FILE_NAME))

    '''
    Read settings from disk, if it does not exist call init to create one with default parameters

    Use this method to access the settings object

    return: deserialised object or newly created settings object
    '''
    def getSettingsObject(self):
        try:
            glObject = Serialise.deserialiseObjectFromFile(self.FILE_NAME, self.FILE_DIR)
        except (IOError, OSError, FileNotFoundError) as e:
            print("[DEBUG] File {0} not found, init default data" .format(self.FILE_NAME))
            self.initSettingsList()
        
        glObject = Serialise.deserialiseObjectFromFile(self.FILE_NAME, self.FILE_DIR)
        return glObject

    '''
    Write settings object to file
    '''
    def setSettingsObject(self):
        try:
            Serialise.serialiseObjectToFile(self, self.FILE_NAME, self.FILE_DIR)
        except (IOError, OSError, FileNotFoundError) as e:
            print("[DEBUG] Failed to write new object {0} to file" .format(self.FILE_NAME))
