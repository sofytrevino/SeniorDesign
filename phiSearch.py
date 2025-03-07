#phiSearch.py
#command line: python phiSearch.py phi1.txt ehr JMS.txt

import sys
import re



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

    def names(self):
        nameCount = 0
        try:
            with open(self.record, 'r+') as file:
                #first find the name we will be looking for
                keyword = False
                for line in file:
                    for word in line.split():
                        if(word == "Patient:" | word == 'Name:'):
                            keyword = True
                        elif keyword == True:
                            keyword = False
                            Name = word
                            print(Name)
                
                #loop through remainder of file and replace and count occurances that equal to Name
                token = "*name*"
                index = 0
                line = file.readlines()
                for word in line:
                    if word == Name:
                        nameCount+= 1
                        replacement = line.replace(word, token)
                        line[index] = replacement
                    index += 1
                file.truncate(0)
                file.writelines(line)
                file.close()


        except FileNotFoundError:
            print(f"Error: File '{self.input}' not found.")
        
        return nameCount


    #def dateOfBirth(self):
    def dateOfBirth(self):
        dateOfBirthCount = 0
        try:
            with open(self.record, 'r+') as file:
                #first find the date of birth we will be looking for
                keyword = False
                for line in file:
                    for word in line.split():
                        if(word == "Date of Birth:" | word == 'date of birth:'  | word == 'DoB:' | word == 'dob:'):
                            keyword = True
                        elif keyword == True:
                            keyword = False
                            DoB = word
                            print(DoB)
                
                #loop through remainder of file and replace and count occurances that equal to Date Of Birth
                token = "*dob*"
                index = 0
                line = file.readlines()
                for word in line:
                    if word == DoB:
                        dateOfBirthCount+= 1
                        replacement = line.replace(word, token)
                        line[index] = replacement
                    index += 1
                file.truncate(0)
                file.writelines(line)
                file.close()


        except FileNotFoundError:
            print(f"Error: File '{self.input}' not found.")
        
        return dateOfBirthCount

    
    #def socialNum(self):
    def socialNum(self):
        socialNumCount = 0
        try:
            with open(self.record, 'r+') as file:
                #first find the social security number we will be looking for
                keyword = False
                for line in file:
                    for word in line.split():
                        if(word == "Social Security Number:" | word == 'Social Secuirty:' | word == 'social security number:'  | word == 'social security:' | word == 'SSN:' | word == 'ssn:'):
                            keyword = True
                        elif keyword == True:
                            keyword = False
                            SSN = word
                            print(SSN)
                
                #loop through remainder of file and replace and count occurances that equal to Social Security Number
                token = "*ssn*"
                index = 0
                line = file.readlines()
                for word in line:
                    if word == SSN:
                        socialNumCount+= 1
                        replacement = line.replace(word, token)
                        line[index] = replacement
                    index += 1
                file.truncate(0)
                file.writelines(line)
                file.close()


        except FileNotFoundError:
            print(f"Error: File '{self.input}' not found.")
        
        return socialNumCount

    #def phoneNum(self):
    def phoneNum(self):
        phoneNumCount = 0
        try:
            with open(self.record, 'r+') as file:
                #first find the phone number we will be looking for
                keyword = False
                for line in file:
                    for word in line.split():
                        if(word == "Phone Number:" | word == 'phone number:' | word == 'Phone:' | word == 'phone:'):
                            keyword = True
                        elif keyword == True:
                            keyword = False
                            Phone = word
                            print(SSN)
                
                #loop through remainder of file and replace and count occurances that equal to Phone Number
                token = "*phone*"
                index = 0
                line = file.readlines()
                for word in line:
                    if word == Phone:
                        phoneNumCount+= 1
                        replacement = line.replace(word, token)
                        line[index] = replacement
                    index += 1
                file.truncate(0)
                file.writelines(line)
                file.close()


        except FileNotFoundError:
            print(f"Error: File '{self.input}' not found.")
        
        return phoneNumCount

    #def email(self):
    def email(self):
        emailCount = 0
        try:
            with open(self.record, 'r+') as file:
                #first find the email we will be looking for
                keyword = False
                for line in file:
                    for word in line.split():
                        if(word == "Email address:" | word == 'email:' | word == "Email Address:"  | word == "email address:" ):
                            keyword = True
                        elif keyword == True:
                            keyword = False
                            Email = word
                            print(Email)
                
                #loop through remainder of file and replace and count occurances that equal to Email
                token = "*email*"
                index = 0
                line = file.readlines()
                for word in line:
                    if word == Email:
                        emailCount+= 1
                        replacement = line.replace(word, token)
                        line[index] = replacement
                    index += 1
                file.truncate(0)
                file.writelines(line)
                file.close()

        
        except FileNotFoundError:
            print(f"Error: File '{self.input}' not found.")
        
        return emailCount



#Record takes in the input list of PHI and addresses the necessary search functions
class Record:
    def _init__(self, input):
        self.input = input
        self.algorithm = SearchRecord

        #loop through self.input and call corresponding functions in Search Record
        #rajfryy authored:
    def process(self):
        return self.searcher.replace_phi()

    def process(self):
        return self.searcher.replace_phi()
        


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




