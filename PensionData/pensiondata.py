import urllib.request
import re
from datetime import datetime
import time
import numpy as np
import tabula
import pandas as pd
import matplotlib.pyplot as plt
import pickle

class PensionData:
    def __init__(self):
        self.baseURL = "https://www.nestpensions.org.uk/schemeweb/dam/nestlibrary/"
        self.months = ["January", "February", "March", "April", "May", "June", "July"]
        self.monthLUT = {}

    def getDATA(self):
        html = urllib.request.urlopen("https://www.nestpensions.org.uk/schemeweb/nest/aboutnest/investment-approach/other-fund-choices/fund-factsheets.html")
        text = html.read().decode("utf-8")

        LinkMonthYearRE = re.compile(r"href=\"(.*\.pdf)\".*prices\ ([a-zA-Z]*?)\ ([0-9]*?)\ *\(")

        results = LinkMonthYearRE.findall(text)
        self.links = []
        self.months = []
        self.years = []

        for each in results:
            if(each[0][0] == "/"):
                self.links.append("https://www.nestpensions.org.uk" + each[0])
            else:
                self.links.append(each[0])
            dt = datetime.strptime("{0} {1}".format(each[1], each[2]), "%B %Y")
            self.months.append(dt.month)
            self.years.append(each[2].lower())

        for i, link in enumerate(self.links):
            os.system("mkdir data")
            urllib.request.urlretrieve(link, "data/{0}-{1}.pdf".format(self.months[i],self.years[i]))
            print("Downloaded ", i, " @ ", self.months[i], ":", self.years[i], " From:", link)

    def loadData(self):
        import datetime
        try:
            new = pd.read_pickle("new.pk")
            print("Data Loaded")
        except:
            for i,_ in enumerate(self.links):
                try:
                    print("Reading ", self.years[i],":",self.months[i])
                    PATH = "data/{0}-{1}.pdf".format(self.months[i], self.years[i])
                    df = tabula.read_pdf(PATH, pages="all")
                    for index, row in df.iterrows():
                        if"Fund" in row.to_string():
                            break
                    df.columns = df.iloc[index+1]
                    df = df[-8:]
                    newnames = ["Name"]
                    newnames.extend(df.columns[1:])
                    df.columns = newnames
                    week2, week3 = df.columns[2].split(" ",1)
                    df[week2], df[week3] = zip(*df[df.columns[2]].map(lambda x: x.split(' ')))
                    df = df.drop([df.columns[2]], axis = 1)
                    df['Name'] = df['Name'].apply(lambda x: x.strip("Your ").strip(" Fund"))
                    if i == 0:
                        new = df
                    else:
                        new = pd.merge(new, df, how='outer')#.fillna(1)
                except:
                    print("Failed on :", self.months[i],":", self.years[i])

            print(new.head())
            new.set_index("Name",inplace=True)

            new.to_pickle("new.pk")
            print("Data Pickled")

        new = new.replace({"-": np.nan})
        #new = new.fillna(0)
        print(new.head())
        patterns = ["%d.%m.%Y","%d/%m/%Y"]
        newcolumns = []
        for col in new.columns:
            for pattern in patterns:
                try:
                    newcolumns.append(datetime.datetime.strptime(col, pattern))
                except:
                    pass
        new.columns = newcolumns
        new = new.reindex(sorted(new.columns[1:]), axis=1)
        pickle.dump(new, open("Sorted.pk", "wb"))
        for index, row in new.iterrows():
            x = (list(map(float, row.tolist())))
            plt.plot(new.columns, x, label=index)
        plt.xticks(rotation = 45)
        plt.legend()
        plt.show()



if __name__ == "__main__":
    x = PensionData()
    x.getDATA()
    x.loadData()
