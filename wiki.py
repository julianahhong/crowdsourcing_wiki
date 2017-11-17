import urllib2
import re
import csv
import datetime

#timestamp format: 2017-11-16T22:22:01Z"
#dict is {"Pat_Harrington": [1/6/16, 1/9/16], ...}
dateRanges = {}

def parseDateRanges(file_path):
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
                dateRanges[row[1]] = [startTimestamp, endTimestamp]
            firstRow = False
        #print(dateRanges)

parseDateRanges("project1.csv")
import requests
import json
def GetRevisions(pageTitle, startDate, endDate):
    url = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&rvlimit=50&rvprop=content&titles=" + pageTitle + '&rvstart=' + startDate + '&rvend=' + endDate
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

    # return revisions
    # parameters = {"format": "xml", "titles": "David_Bowie", "rvprop": "content"}
    # response = requests.get("https://en.wikipedia.org/w/api.php", params=parameters)
    # print(response.content)
    response = requests.get(url)
    res_content = response.content
    json_res = json.loads(res_content)
    #a = res_content["query"]
    page_num = json_res["query"]["pages"].keys()[0]
    # print(json_res["query"]["pages"][page_num]["revisions"][0]["*"])
    revisions = json_res["query"]["pages"][page_num]["revisions"]

    for rev in revisions:
        content = rev["*"]
        s = content.encode('ascii','ignore')
        print(s.find("death_date") != -1)

revisions = GetRevisions("David_Bowie", "2016-01-11T23:00:00Z", dateRanges["David_Bowie"][1])

# for i in revisions[0]:
#     print(i)
