import urllib2
import re
import csv
import datetime
import requests
import json

class Search:
    def __init__(self):
        self.dateRanges = {}
        self.parseDateRanges("project1_subset.csv")
        #print(self.dateRanges)
        self.curr_timestamp = ""
        # self.curr_timestamp = self.searchForFirstUpdate("Pat_Harrington_Jr.", self.dateRanges["Pat_Harrington_Jr."][0])
        # print(self.curr_timestamp)
        self.timestamps = {}
        self.run()
#timestamp format: 2017-11-16T22:22:01Z"
#dict is {"Pat_Harrington": [1/6/16, 1/9/16], ...}

    def parseDateRanges(self, file_path):
        with open(file_path, 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            firstRow = True
            for row in csvreader:
                #print(row[0][2])
                if not firstRow:
                    startDate = datetime.datetime.strptime(row[3], '%m/%d/%y')
                    endDate = datetime.datetime.strptime(row[2], '%m/%d/%y')
                    startDate = str(startDate).replace(' ', 'T')
                    endDate = str(endDate).replace(' ', 'T')
                    startTimestamp = startDate + "Z"
                    endTimestamp = endDate + "Z"
                    self.dateRanges[row[1]] = [startTimestamp, endTimestamp]
                firstRow = False

    def containsFirstUpdate(self, pageTitle, startDate):
        # url = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&rvlimit=50&rvprop=content|timestamp&titles=" + pageTitle + '&rvstart=' + startDate +'&rvend=' + endDate
        url = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&rvlimit=50&rvprop=content|timestamp&titles=" + pageTitle + '&rvstart=' + startDate
       
        print(url)
        # revisions = []                                        #list of all accumulated revisions
        # next = ''                                             #information for the next request
        # while True:
        #     response = urllib2.urlopen(url + next).read()     #web request
        #     revisions += re.findall('<rev [^>]*>', response)  #adds all revisions from the current request to the list

        #     cont = re.search('<continue rvcontinue="([^"]+)"', response)
        #     if not cont:                                      #break the loop if 'continue' element missing
        #         break

        #     next = "&rvcontinue=" + cont.group(1)             #gets the revision Id from which to start the next request
        # print(revisions)
        # return revisions
        # parameters = {"format": "xml", "titles": "David_Bowie", "rvprop": "content"}
        # response = requests.get("https://en.wikipedia.org/w/api.php", params=parameters)
        # print(response.content)
        # response = requests.get(url)
        # res_content = response.content
        # json_res = json.loads(res_content)
        # #a = res_content["query"]
        # page_num = json_res["query"]["pages"].keys()[0]
        # # print(json_res["query"]["pages"][page_num]["revisions"][0]["*"])
        # revisions = json_res["query"]["pages"][page_num]["revisions"]

        # for rev in revisions:
        #     content = rev["*"]
        #     s = content.encode('ascii','ignore')
        #     print(s.find("death_date") != -1)

        response = requests.get(url)
        res_content = response.content
        json_res = json.loads(res_content)
        #a = res_content["query"]
        page_num = json_res["query"]["pages"].keys()[0]
        # print(json_res["query"]["pages"][page_num]["revisions"][0]["*"])
        # print(json_res)
        revisions = json_res["query"]["pages"][page_num]["revisions"]
        # print(revisions)
        for rev in revisions:
            self.curr_timestamp = rev["timestamp"]

            content = rev["*"]
            s = content.encode('ascii','ignore')
            # print(content)
            # print(s.find("death_date") != -1)
            if s.find("death_date") == -1:
                return True
        return False

    # containsFirstUpdate("Joe_Garagiola_Sr.", dateRanges["Joe_Garagiola"][0])

    # print(containsFirstUpdate("Joe_Garagiola_Sr.", dateRanges["Joe_Garagiola"][0]))
    # #if update in first range, get that date; otherwise, make start date later
    def searchForFirstUpdate(self,title_name, startDate):
        containsUpdate = self.containsFirstUpdate(title_name, startDate)
        print(containsUpdate)
        if containsUpdate:
            return self.curr_timestamp
        else:
            while(not containsUpdate):
                containsUpdate = self.containsFirstUpdate(title_name, startDate)
                startDate = self.curr_timestamp
        return self.curr_timestamp

    def run(self):
        times = {}

        for key in self.dateRanges:
            times[key] = self.searchForFirstUpdate(key, self.dateRanges[key][0])
        self.timestamps = times
        print(self.timestamps)
        self.writeToCSV()

    def writeToCSV(self):
        myFile = open('final_timestamps.csv', 'w')  
        with myFile:  
           writer = csv.writer(myFile)
           for key, value in self.timestamps.items():
                writer.writerow([key, value])

Search()