from pensiondata import PensionData
import os
import time

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

loader = loading()


while True:
    time.sleep(1)#60*10)
    loader.loading()
    try:
        a.getData()
        if links != a.links:
            print("New PDFs Found")
            os.system("cp new.pk old.pk")
            os.system("rm new.pk")
            a.loadData()
            links = a.links.copy()
    except expression as identifier:
        pass