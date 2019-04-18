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

loader = loading()


while True:
    loader.loading()
    time.sleep(60*10)
    try:
        a.getData()
        if links != a.links:
            print("New PDFs Found")
            links = a.links.copy()
            
    except:
        pass