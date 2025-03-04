#phiSearch.py
#command line: python phiSearch.py phi1.txt ehr JMS.txt

import sys



#Parsing class should read inputFile and see what information it needs to search
class Parsing(object):

    def __init__(self, input):
        self.input = input
        self.info = []

    #should return self.info list of PHI info needed to search
    def parse(self):

        #read input file
        try:
            with open(self.input, 'r') as file:
                #read PHI values that need to be found and save in self.info
                #read line by line
                for line in file:
                    wordCount = 0
                    for word in line.split():
                        wordCount += 1
                        if wordCount == 1:
                            self.info.append(word)

        except FileNotFoundError:
            print(f"Error: File '{self.input}' not found.")
        except Exception as e:
            print(f"Error: {e}")
        
        return self.info
       
        

#SearchRecord should keep track of the occurances of the found PHI in the record file passed in
class SearchRecord:

    def __init__(self, info, record):
        self.info = info
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
        self.algorithm = SearchRecord

        #loop through self.input and call corresponding functions in Search Record


        


def main():
    #test main
    #data = "hello"
    #print(data)

    #ensure command-line arguments
    if len(sys.argv) < 3:
        print("Missing input file and/or record file")
        sys.exit(1)
    inputFile = sys.argv[1]
    recordFile = sys.argv[2]

    parseInfo = Parsing(inputFile)
    infoList = parseInfo.parse()
    search = Record(infoList)

   
if __name__ == "__main__":
    main()




