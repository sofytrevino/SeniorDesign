#phiSearch.py
#command line: python phiSearch.py phi1.txt ehr JMS.txt

import sys

def main():
    #test main
    #data = "hello"
    #print(data)

    inputFile = sys.argv[1]
    recordFile = sys.argv[2]

    search = SearchRecord(inputFile, recordFile)
    parseInfo = Parsing(inputFile, search)
   
if __name__ == "__main__":
    main()


#Parsing class should read inputFile and see what information it needs to search
class Parsing:

    def _init__(self, input, searchAlgorithm):
        self.input = input
        self.info = []
        self.search = searchAlgorithm


    #def parse(self):
        #should use the SearchRecord to call the search function

#SearchRecord should keep track of the occurances of the found PHI in the record passed in
class SearchRecord:

    def _init__(self, input, record):
        self.input = input
        self.record = record


    #functions should return the number of occurances found of each type

    #def names(self):


    #def dateOfBirth(self):

    
    #def socialNum(self):


    #def phoneNum(self):


    #def email(self):



#Record takes in the input list of PHI and addresses the necessary search functions
class Record:
    def _init__(self, input):
        self.input = input



