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


print("Pension Monitor - Running")
a = PensionData()
a.getData()
links = a.links.copy()

print("Pension Monitor - Fetched Links")

a.loadData()

print("Pension Monitor - Data Loaded")

print("Pension Monitor - Sending Data")

with open("Current_Data.png") as f:
    lastest_file = pb.upload_file(f, "LatestNestData.png")

pb.push_file(**lastest_file)

print("Pension Monitor - Data Sent")

loader = loading()

pb = Pushbullet("")
pb.push_note("ONLINE", "Nest Pension Monitor Online.")

print("Pension Monitor - Monitoring")

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
                pass
    except:
        print("Failed")
        try:
            pb.push_note("Nest Script Crashed","")
        except:
            pass

pb.push_note("Nest Script Crashed","")