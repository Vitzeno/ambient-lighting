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


    def __init__(self):
        print("Init singleton settings object")
        self.MONITER_RES_WIDTH = 3840
        self.MONITER_RES_HEIGHT = 2160

        self.SCREENSHOT_WIDTH = 1500
        self.SCREENSHOT_HEIGHT = 20
    
    def setUpDefaultData(self):
        self.MONITER_RES_WIDTH = 3840
        self.MONITER_RES_HEIGHT = 2160

        self.SCREENSHOT_WIDTH = 1500
        self.SCREENSHOT_HEIGHT = 20

    '''
    Init the settings list JSON file and write to disk, default parameters are used
    '''
    def initSettingsList(self):
        print("Init settings and write to file")
        try:
            self.setUpDefaultData()
            Serialise.serialiseObjectToFile(self, self.FILE_NAME, self.FILE_DIR)
        except (IOError, OSError, FileNotFoundError) as e:
            print("Failed to init {0}" .format(self.FILE_NAME))

    '''
    Read settings from disk, if it does not exist call init to create one with default parameters

    Use this method to access the settings object

    return: deserialised object or newly created settings object
    '''
    def getSettingsObject(self):
        try:
            glObject = Serialise.deserialiseObjectFromFile(self.FILE_NAME, self.FILE_DIR)
        except (IOError, OSError, FileNotFoundError) as e:
            print("File {0} not found, init default data" .format(self.FILE_NAME))
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
            print("Failed to write new object {0} to file" .format(self.FILE_NAME))
