from pensiondata import PensionData
import time
from pushbullet import Pushbullet

class loading():
    def __init__(self):
        self.LUT = ['|','/','-','\\']
        self.wrap = len(self.LUT)
        self.i = 0
    def loading(self):
        if self.i == self.wrap:
            self.i = 0
        print(self.LUT[self.i], end = "\r")
        self.i += 1


a = PensionData()
a.getData()
links = a.links.copy()

a.loadData()
with open("Current_Data.png") as f:
    lastest_file = pb.upload_file(f, "LatestNestData.png")

pb.push_file(**lastest_file)

loader = loading()

pb = Pushbullet("")
pb.push_note("ONLINE", "Nest Pension Monitor Online.")

while True:
    loader.loading()
    time.sleep(60)
    try:
        a.getData()
        if links != a.links:
            print("New PDFs Found")
            links = a.links.copy()
            pb.push_note("New Nest Data")
            try:
                a.loadData()
                with open("Current_Data.png") as f:
                    lastest_file = pb.upload_file(f, "LatestNestData.png")
                
                pb.push_file(**lastest_file)
    except:
        print("Failed")
        try:
            pb.push_note("Nest Script Crashed","")
        except:
            pass

pb.push_note("Nest Script Crashed","")