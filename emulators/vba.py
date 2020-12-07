from util import *
from emulator import Emulator
import shutil


class VBA(Emulator):
    def __init__(self):
        super().__init__("VisualBoyAdvance", startup_time=0.6)
    
    def setup(self):
        download("https://sourceforge.net/projects/vba/files/latest/download", "downloads/vba.zip")
        extract("downloads/vba.zip", "emu/vba")
        setDPIScaling("emu/vba/VisualBoyAdvance.exe")
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "vba.ini"), "emu/vba/vba.ini")

    def startProcess(self, rom, *, gbc=False):
        return subprocess.Popen(["emu/vba/VisualBoyAdvance.exe", os.path.abspath(rom)], cwd="emu/vba")


class VBAM(Emulator):
    def __init__(self):
        super().__init__("VisualBoyAdvance-M", startup_time=1.0)
        self.title_check = lambda title: "VisualBoyAdvance-M" in title
    
    def setup(self):
        download("https://github.com/visualboyadvance-m/visualboyadvance-m/releases/download/v2.1.4/visualboyadvance-m-Win-64bit.zip", "downloads/vba-m.zip")
        extract("downloads/vba-m.zip", "emu/vba-m")
        setDPIScaling("emu/vba-m/visualboyadvance-m.exe")
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "vbam.ini"), "emu/vba-m/vbam.ini")

    def startProcess(self, rom, *, gbc=False):
        return subprocess.Popen(["emu/vba-m/visualboyadvance-m.exe", os.path.abspath(rom)], cwd="emu/vba-m")

    def getScreenshot(self):
        screenshot = getScreenshot(self.title_check)
        if screenshot is None:
            return None
        x = (screenshot.size[0] - 160) // 2
        y = (screenshot.size[1] - 144) // 2 - 1
        return screenshot.crop((x, y, x + 160, y + 144))
