from util import *
from emulator import Emulator
from test import *
from selenium import webdriver
import PIL.Image

class Emmy(Emulator):
    def __init__(self):
        super().__init__("Emmy", "https://emmy-gbc.vercel.app/", startup_time=0.5)

    def setup(self):
        # download("http://problemkaputt.de/no$gmb.zip", "downloads/no$gmb.zip", fake_headers=True)
        # extract("downloads/no$gmb.zip", "emu/no$gmb")
        # https://chromedriver.storage.googleapis.com/109.0.5414.74/chromedriver_win32.zip
        download("https://chromedriver.storage.googleapis.com/109.0.5414.74/chromedriver_win32.zip", "downloads/chromedriver_win32.zip")
        extract("downloads/chromedriver_win32.zip", "emu/chromedriver_win32")
        self.driver = webdriver.Chrome("emu/chromedriver_win32/chromedriver.exe")
        self.driver.get("https://emmy-gbc.vercel.app/")
        self.driver.find_element(value="emu-speed").click()
        self.driver.find_element(value="drawer-section-settings").click()

    def isWindowOpen(self):
        return self.driver is not None

    def isProcessAlive(self, p):
        return True

    def processOutput(self, p):
        return None

    def endProcess(self, p):
        pass

    def returncode(self, p):
        return 0

    def startProcess(self, rom, *, model, required_features):
        systemmode = {DMG: "dmg-mode", CGB: "cgb-mode"}.get(model)
        if systemmode is None:
            return None
        self.driver.find_element(value=systemmode).click()
        rom_path = os.path.abspath(rom)
        try:
            self.driver.find_element(value="rom-input").send_keys(rom_path)
            try:
                # if an alert appeared, it means the rom is incompatible
                self.driver.switch_to.alert.accept()
                return None
            except:
                # no alert, so error thrown, so the rom is compatible
                return self.driver
        except Exception as e:
            return None

    # must return a pillow image object
    def getScreenshot(self):
        canvas = self.driver.find_element(value="emulator-frame")
        canvas_base64 = self.driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)

        # decode
        canvas_png = base64.b64decode(canvas_base64)
        # by default, 4 canvas pixels = 1 screen pixel
        large_image = PIL.Image.open(io.BytesIO(canvas_png))
        # resize to 1:1
        small_image = large_image.resize((160, 144), PIL.Image.NEAREST)
        return small_image

