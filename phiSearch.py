#phiSearch.py
#command line: python phiSearch.py phi1.txt JMS.txt

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

    def __init__(self, record):
        self.record = record
        #self.outputFile = "JMS2.txt"
        
    #functions should return the number of occurances found of each type

    def name(self):
        nameCount = 0
        try:
            with open(self.record, 'r+') as file:
                #first find the name we will be looking for
                nameBank = {"Patient:", "Name:", "name:"}
                keyword = False
                Name = ""
                lines = file.readlines()
                for line in lines:
                    words = line.split()
                    for word in words:
                        if not keyword:
                            if(word in nameBank):
                                parts = line.split()
                                if len(parts) > 1:
                                    Name = " ".join(parts[2:]).strip()
                                    L_name = Name.split()[-1]
                                #print(Name)
                                #print(L_name)
                                keyword = True
                                break
                                
                #loop through remainder of file and replace and count occurances that equal to Name
                if Name != "":
                    token = "*name*"
                    updated_lines = []
                    for line in lines:
                        occurences =  line.count(Name)
                        occurences2 = line.count(L_name)
                        if occurences > 0:
                            nameCount += occurences
                            line = line.replace(Name, token)
                        if occurences2 > 0:
                            nameCount += occurences
                            line = line.replace(L_name, token)
                        updated_lines.append(line)
                    file.seek(0)
                    #file.truncate(0)
                    file.writelines(updated_lines)
            
                
        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")
        
        return nameCount

    #def address(self):
    def address(self):
        addressCount = 0
        try:
            with open(self.record, 'r+') as file:
                #first find the address we will be looking for
                lines = file.readlines()
                keyword = False
                found = False
                Address = ""
                for line in lines:
                    words = line.split()
                    for word in words:
                        if not found:
                            if(word == "Address:" or word == 'address:'):
                                keyword = True
                                #Address = word
                            elif keyword == True:
                                keyword = False
                                #add the following words after address to the address String object
                                if "Address:" in line or "address:" in line:
                                    Address = line.split(":", 1)[1].strip()
                                #print(Address)
                                found = True
                                break
                
                #loop through remainder of file and replace and count occurances that equal to Email
                if Address != "":
                        token = "*address*"
                        updated_lines = []
                        for line in lines:
                            occurrences = line.count(Address)
                            if occurrences > 0:
                                addressCount+= 1
                                line = line.replace(Address, token)
                            updated_lines.append(line)
                        file.seek(0)
                        file.truncate(0)
                        file.writelines(updated_lines)
                
        
        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")
        
        return addressCount

    #def dateOfBirth(self):
    def dateOfBirth(self):
        #print("finding date of birth")
        dateOfBirthCount = 0
        try:
            with open(self.record, 'r+') as file:
                #first find the date of birth we will be looking for
                lines = file.readlines()
                keyword = False
                found = False
                DoB = ""
                for line in lines:
                    words = line.split()
                    for word in words:
                        if not found:
                            #print("word: ", word)
                            if(word == "Date of Birth:" or word == 'date of birth:' or word == 'DoB:' or word == 'dob:' or word == "Birth:"):
                                keyword = True
                            elif keyword == True:
                                DoB = word.strip()
                                keyword = False
                                #print(DoB)
                                found = True
                                break
                #loop through remainder of file and replace and count occurances that equal to Date Of Birth
                if DoB != "":
                    token = "*DoB*"
                    updated_lines = []
                    for line in lines:
                        occurences = line.count(DoB)
                        if occurences > 0:
                            dateOfBirthCount+= 1
                            line = line.replace(DoB, token)
                        updated_lines.append(line)
                    file.seek(0)
                    file.truncate(0)
                    file.writelines(updated_lines)
                

        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")
        
        return dateOfBirthCount

    
    #def socialNum(self):
    def socialNum(self):
        #print("finding social num")
        socialNumCount = 0
        try:
            with open(self.record, 'r+') as file:
                #first find the social security number we will be looking for
                lines = file.readlines()
                keyword = False
                found = False
                SSN = ""
                for line in lines:
                    words =  line.split()
                    for word in words:
                        if not found:
                            if(word == "Social Security Number:" or word == 'Social Secuirty:' or word == 'social security number:' or word == 'social security:' or word == 'SSN:' or word == 'ssn:' or word == "Number:"):
                                keyword = True
                            elif keyword == True:
                                keyword = False
                                SSN = word.strip()
                                #print(SSN)
                                found = True
                                break
                
                #loop through remainder of file and replace and count occurances that equal to Social Security Number  
                if SSN != "":
                    SSN = str(SSN)
                    token = "*SSN*"
                    updated_lines = []
                    for line in lines:
                        occurrences = line.count(SSN)
                        if occurrences > 0:
                            socialNumCount+= 1
                            line = line.replace(SSN, token)
                        updated_lines.append(line)
                    file.seek(0)
                    file.truncate(0)
                    file.writelines(updated_lines)


        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")
        
        return socialNumCount

    #def phoneNum(self):
    def phoneNum(self):
        #print("finding phone Num")
        phoneNumCount = 0
        try:
            with open(self.record, 'r+') as file:
                #first find the phone number we will be looking for
                lines = file.readlines()
                keyword = False
                found = False
                Phone = ""
                for line in lines:
                    words = line.split()
                    for word in words:
                        if not found:
                            if(word == "Phone Number:" or word == 'phone number:' or word == 'Phone:' or word == 'phone:'):
                                keyword = True
                            elif keyword == True:
                                keyword = False
                                Phone = word
                                #print(Phone)
                                found = True
                                break
                #loop through remainder of file and replace and count occurances that equal to Phone Number
                if Phone != "":
                        token = "*phone*"
                        updated_lines = []
                        for line in lines:
                            occurrences = line.count(Phone)
                            if occurrences > 0:
                                phoneNumCount+= 1
                                line = line.replace(Phone, token)
                            updated_lines.append(line)
                        file.seek(0)
                        file.truncate(0)
                        file.writelines(updated_lines)


        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")
        
        return phoneNumCount

    #def email(self):
    def email(self):
        emailCount = 0
        try:
            with open(self.record, 'r+') as file:
                #first find the email we will be looking for
                lines = file.readlines()
                emailBank = {"email:", "Email:"}
                keyword = False
                found = False
                Email = ""
                for line in lines:
                    words = line.split()
                    for word in words:
                        if not found:
                            if(word in emailBank):
                                keyword = True
                            elif keyword == True:
                                keyword = False
                                Email = word.strip()
                                #print(Email)
                                found = True
                                break
                
                #loop through remainder of file and replace and count occurances that equal to Email
                if Email != "":
                        token = "*email*"
                        updated_lines = []
                        for line in lines:
                            occurrences = line.count(Email)
                            if occurrences > 0:
                                emailCount+= 1
                                line = line.replace(Email, token)
                            updated_lines.append(line)
                        file.seek(0)
                        file.truncate(0)
                        file.writelines(updated_lines)
        
        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")


        return emailCount
    

    #def provider
    def provider(self):
        providerCount = 0
        try:
            with open(self.record, 'r+') as file:
                #first find the name we will be looking for
                providerBank = {"Provider", "Provider:"}
                keyword = False
                Provider = ""
                lines = file.readlines()
                for line in lines:
                    words = line.split()
                    for word in words:
                        if not keyword:
                            if(word in providerBank):
                                parts = line.split()
                                if len(parts) > 1:
                                    Provider = " ".join(parts[2:]).strip()
                                    L_Provider = Provider.split()[-1]
                                #print(Provider)
                                #print(L_Provider)
                                keyword = True
                                break
                                
                #loop through remainder of file and replace and count occurances that equal to Name
                if Provider != "":
                    token = "*Provider*"
                    updated_lines = []
                    for line in lines:
                        occurences =  line.count(Provider)
                        occurences2 = line.count(L_Provider)
                        if occurences > 0:
                            providerCount += occurences
                            line = line.replace(Provider, token)
                        if occurences2 > 0:
                            providerCount += occurences
                            line = line.replace(L_Provider, token)
                        updated_lines.append(line)
                    file.seek(0)
                    #file.truncate(0)
                    file.writelines(updated_lines)
            
                
        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")
        
        return providerCount


    #def hospital
    def hospital(self):
        hospitalCount = 0
        try:
            with open(self.record, 'r+') as file:
                #first find the name we will be looking for
                hospitalBank = {"Hospital", "Hospital:"}
                keyword = False
                Hospital = ""
                lines = file.readlines()
                for line in lines:
                    words = line.split()
                    for word in words:
                        if not keyword:
                            if(word in hospitalBank):
                                parts = line.split()
                                if len(parts) > 1:
                                    Hospital = " ".join(parts[2:]).strip()
                                    L_Hospital = Hospital.split()[-1]
                                #print(Hospital)
                                #print(L_Hospital)
                                keyword = True
                                break
                                
                #loop through remainder of file and replace and count occurances that equal to Name
                if Hospital != "":
                    token = "*HospitalName*"
                    updated_lines = []
                    for line in lines:
                        occurences =  line.count(Hospital)
                        occurences2 = line.count(L_Hospital)
                        if occurences > 0:
                            hospitalCount += occurences
                            line = line.replace(Hospital, token)
                        if occurences2 > 0:
                            hospitalCount += occurences
                            line = line.replace(L_Hospital, token)
                        updated_lines.append(line)
                    file.seek(0)
                    #file.truncate(0)
                    file.writelines(updated_lines)
            
                
        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")
        
        return hospitalCount


    #def allergies



    #def lab resutls
    def lab(self):
        labCount = 0
        labBank = {"Lab"}
        try:
            with open(self.record, 'r+') as file:
                #first find the email we will be looking for
                lines = file.readlines()
                keyword = False
                found = False
                Lab = "-"
    
                token = "*Lab Results*"
                updated_lines = []
                for line in lines:
                    if found and line.startswith("-"):
                        labCount+= 1
                        line = token
                    if found and not line.startswith("-"):
                        found = False
                    if "Lab Results" in line:
                        found = True
                    updated_lines.append(line)
                file.seek(0)
                file.truncate(0)
                file.writelines(updated_lines)
        
        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")


        return labCount

    #def medicaid account


    #def social worker
    def socialWorker(self):
        socialWorkerCount = 0
        try:
                with open(self.record, 'r+') as file:
                    # Find the social worker's name
                    lines = file.readlines()
                    keyword = False
                    found = False
                    SocialWorker = ""
                    for line in lines:
                        if not found and ("Social worker:" in line or "Social Worker:" in line):
                            parts = line.split(":", 1)
                            if len(parts) > 1:
                                SocialWorker = parts[1].strip()
                                found = True
                                break
                    
                    # Replace occurrences of the social worker's name
                    if SocialWorker:
                        token = "*Social Worker*"
                        updated_lines = []
                        for line in lines:
                            occurrences = line.count(SocialWorker)
                            if occurrences > 0:
                                socialWorkerCount += occurrences
                                line = line.replace(SocialWorker, token)
                            updated_lines.append(line)
                        file.seek(0)
                        file.truncate(0)
                        file.writelines(updated_lines)
    
            except FileNotFoundError:
                print(f"Error: File '{self.record}' not found.")
            
            return socialWorkerCount



#Record takes in the input list of PHI and addresses the necessary search functions
class Record(object):
    def __init__(self, input, outputFile):
        self.input = input
        self.algorithm = SearchRecord(outputFile)

    def find(self):
        inputs = self.input
        counts = []
        #loop through self.input and call corresponding functions in Search Record
        #print("inputs: ", inputs)
        for info in inputs:
            if "Name" in info or "Patient" in info:
                #print("record name")
                names = self.algorithm.name()
                counts.append(names)
            if "Address" in info:
                #print("record address")
                address = self.algorithm.address()
                counts.append(address)
            if "Date" in info:
                #print("record date")
                date = self.algorithm.dateOfBirth()
                counts.append(date)
            if "Social" in info or "SSN" in info:
                #print("record social")
                social = self.algorithm.socialNum()
                counts.append(social)
            if "Phone" in info:
                #print("record phone")
                phone = self.algorithm.phoneNum()
                counts.append(phone)
            if "Email" in info:
                #print("record email")
                email = self.algorithm.email()
                counts.append(email)
            if "Provider" in info:
                #print("record provider")
                provider = self.algorithm.provider()
                counts.append(provider)
            if "Hospital" in info:
                #print("record hospital")
                hospital = self.algorithm.hospital()
                counts.append(hospital)
            if "Lab" in info:
                #print("record lab resutls")
                lab = self.algorithm.lab()
                counts.append(lab)
            if "Social" in info:
                #print("record social worker")
                socialWorker = self.algorithm.socialWorker()
                counts.append(socialWorker)
        return counts

        


def main():

    #ensure command-line arguments
    if len(sys.argv) < 3:
        print("Missing input file and/or record file")
        sys.exit(1)
    inputFile = sys.argv[1]
    recordFile = sys.argv[2]
    outputFile = "NewJMS.txt"

    #copy input file to output file
    with open(recordFile, 'r') as source, open(outputFile, "w") as destination:
        destination.write(source.read())
    

    parseInfo = Parsing(inputFile)
    infoList = parseInfo.parse()
    #print("info list: ", infoList)
    search = Record(infoList, outputFile)
    found = search.find()
    print("PHI Final Count: ", found)

   
if __name__ == "__main__":
    main()
