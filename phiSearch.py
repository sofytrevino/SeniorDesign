#phiSearch.py
#command line: python phiSearch.py phi1.txt JMS.txt

import sys
import re
import string

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
                ALPHA = string.ascii_letters
                for line in file:
                    wordCount = 0
                    for word in line.split():
                        if word.startswith(tuple(ALPHA)):
                            wordCount += 1
                            if wordCount == 1:
                                if word == "Allergies":
                                    #word = "".join(line[1:]).strip()
                                    #print("allergies found in parse: ", word)
                                    self.info.append(line)
                                else:
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
                namesFound = []
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
                                    namesFound.append(Name)
                                    L_name = Name.split()[-1]
                                #print(Name)
                                #print(L_name)
                                keyword = True
                                break
                                
                #loop through remainder of file and replace and count occurances that equal to Name
                if Name != "":
                    token = "*name*"
                    updated_lines = []
                    for Name in namesFound:
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
                addressFound = []
                keyword = False
                found = False
                Address = ""
                for line in lines:
                    words = line.split()
                    for word in words:
                        if(word == "Address:" or word == 'address:'):
                            keyword = True
                            #Address = word
                        elif keyword == True:
                            keyword = False
                            #add the following words after address to the address String object
                            if "Address:" in line or "address:" in line:
                                Address = line.split(":", 1)[1].strip()
                            addressFound.append(Address)
                            #print(Address)
                                
                
                
                #loop through remainder of file and replace and count occurances that equal to Email
                if Address != "":
                        token = "*address*"
                        updated_lines = []
                        for line in lines:
                            for Address in addressFound:
                                if Address in line:
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
                emailFound = []
                keyword = False
                found = False
                Email = ""
                for line in lines:
                    words = line.split()
                    for word in words:
                        if(word in emailBank):
                            keyword = True
                        elif keyword == True:
                            keyword = False
                            Email = word.strip()
                            emailFound.append(Email)
                            #print(Email)
                            #found = True
                
                #loop through remainder of file and replace and count occurances that equal to Email
                if Email != "":
                        token = "*email*"
                        updated_lines = []
                        for line in lines:
                            for Email in emailFound:
                                if Email in line:
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
                accountBank = {"Provider", "Provider:"}
                keyword = False
                Provider = ""
                lines = file.readlines()
                for line in lines:
                    words = line.split()
                    for word in words:
                        if not keyword:
                            if(word in accountBank):
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
    
                token = "*Lab Results*\n"
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
    def medicaid(self):
        medicaid_count = 0
        medicaid_format = re.compile('[0123456789]{4} [0123456789]{4} [0123456789]{4} [0123456789]{4}')
        try:
            with open(self.record, 'r+') as file:
                #first identify the medicaid number we are looking for
                #replace all occurrences of the medicaid number with the term "medicaid"
                found = False
                lines = file.readlines()
                for line in lines:
                    if not found:
                        re.sub(medicaid_format, "*Medicaid Account*", line, medicaid_count)
                        Medicaid=re.search(medicaid_format, line)
                        if Medicaid:
                            found = True
                            Medicaid = Medicaid.group()  # Output: 1234 5678 9012 3456
                            print(Medicaid)
                if not Medicaid:
                    Medicaid = ""

                #loop through remainder of file and replace and count occurances that equal to Medicaid
                if Medicaid != "":
                        token = "*Medicaid Account*"
                        updated_lines = []
                        for line in lines:
                            occurrences = line.count(Medicaid)
                            if occurrences > 0:
                                medicaid_count+= 1
                                line = line.replace(Medicaid, token)
                            updated_lines.append(line)
                        file.seek(0)
                        file.truncate(0)
                        file.writelines(updated_lines)
        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")

        return medicaid_count

    #def account
    def account(self):
        accountCount = 0
        try:
            with open(self.record, 'r+') as file:
                #first find the account occurrence we will be looking for
                accountBank = {"Account", "Account:", "account", "account:"}
                keyword = False
                Account = "" #consider making a list and using in to check if need to add to the array during if statement below
                lines = file.readlines()
                for line in lines:
                    words = line.split()
                    for word in words:
                        if not keyword:
                            if(word in accountBank):
                                parts = line.split()
                                if len(parts) > 1:
                                    Account = " ".join(parts[1:]).strip() #try make 1
                                    L_Account = Account.split()[-1]
                                #print(Account)
                                #print(L_Account)
                                keyword = True
                                break
                                
                #loop through remainder of file and replace and count occurances that equal to Account
                if Account != "":
                    token = "*Account*"
                    updated_lines = []
                    for line in lines:
                        occurences =  line.count(Account)
                        occurences2 = line.count(L_Account)
                        if occurences > 0:
                            accountCount += occurences
                            line = line.replace(Account, token)
                        if occurences2 > 0:
                            accountCount += occurences
                            line = line.replace(L_Account, token)
                        updated_lines.append(line)
                    file.seek(0)
                    file.truncate(0)
                    file.writelines(updated_lines)
                
        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")
        return accountCount

    #def allergies(self, list)  list = allergies you are looking for
    def allergies(self, list):
        allergiesCount = 0
        allergiesBank = {"Allergies"}
        try:
            with open(self.record, 'r+') as file:
                #first find the email we will be looking for
                lines = file.readlines()
                keyword = False
                found = False
                Allergies = "-"
                
                token = "*Allergies*\n"
                updated_lines = []
                for line in lines:
                    if found:
                        if line.startswith("-"):
                            word = line.split()
                            word = " ".join(word[1:]).strip()
                            #check if allergy part of the list
                            for med in list:
                                if med in word:
                                    #print("found allergy")
                                    allergiesCount += 1
                                    line = token
                        else:
                            for med in list:
                                if med in line:
                                    #print("found allergy")
                                    allergiesCount += 1
                                    line = token
                    if "Allergies:" in line:
                        found = True
                    updated_lines.append(line)
                file.seek(0)
                file.truncate(0)
                file.writelines(updated_lines)
        
        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")


        return allergiesCount

    #def dates
    def dates(self):
        datesCount = 0
        try:
            with open(self.record, 'r+') as file:
                #first find the date we will be looking for
                lines = file.readlines()
                updated_lines = []
                for line in lines:
                    # Updated regex to match dates in MM/DD/YYYY format
                    dates = re.findall(r'\b\d{1,2}/\d{1,2}/\d{4}\b', line)
                    for date in dates:
                        datesCount += 1
                        line = line.replace(date, "*date*")
                    updated_lines.append(line)
                file.seek(0)
                file.truncate(0)
                file.writelines(updated_lines)
        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")
        return datesCount


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

    #def fax number
    def fax(self):
        faxCount = 0
        try:
            with open(self.record, 'r+') as file:
                lines = file.readlines()
                updated_lines = []
                for line in lines:
                    # match common fax num format
                    #faxes = re.findall(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', line)
                    fax = re.search(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', line)
                    #for fax in faxes:
                    if "fax" in line.lower():#ensures it's a fax
                        if fax: 
                            fax = fax.group()
                            faxCount += 1
                            line = line.replace(fax, "*Fax Number*")
                    updated_lines.append(line)
                file.seek(0)
                file.truncate(0)
                file.writelines(updated_lines)
        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")

        return faxCount

    #def medical record #
    def medical_record_number(self):
        count = 0
        token = "*medical num*"
        try:
            with open(self.record, 'r') as file:
                lines = file.readlines()
            with open(self.record, 'w') as file:
                for line in lines:
                    if "Medical record number:" in line:
                        line = re.sub(r'(Medical record number:\s*)[\w\-]+', r'\1*medical num*', line)
                        count += 1
                    file.write(line)
        except Exception as e:
            print(f"Error processing medical record number: {e}")
        return count
    
    #def certificate
    def certificate(self):
        certificateCount = 0
        try:
            with open(self.record, 'r+') as file:
                lines = file.readlines()
                updated_lines = []
                cnum = "Certificate number:"
                for line in lines:
                    certificate = re.search('[A-Z]{2}[0-9]{3}[a-z]-[0-9]{4}', line)
                    if cnum in line:
                        if certificate:
                            certificate = certificate.group()
                            certificateCount += 1
                            line = line.replace(certificate, "*Certificate number*")
                    updated_lines.append(line)
                file.seek(0)
                file.truncate(0)
                file.writelines(updated_lines)
        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")

        return certificateCount

    #def license
    def license(self):
        licenseCount = 0
        try:
            with open(self.record, 'r+') as file:
                lines = file.readlines()
                updated_lines = []
                lnum = "license number:"
                for line in lines:
                    license = re.search('[A-Z]{2}[0-9]{2}-[0-9]{6}', line)
                    if lnum in line:
                        if license:
                            license = license.group()
                            licenseCount += 1
                            line = line.replace(license, "*License number*")
                    updated_lines.append(line)
                file.seek(0)
                file.truncate(0)
                file.writelines(updated_lines)
        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")

        return licenseCount

    #def serial num
    def serial(self):
        serialCount = 0
        try:
            with open(self.record, 'r+') as file:
                lines = file.readlines()
                updated_lines = []
                #pattern = re.compile(r'(Serial(?: Number)?:\s*)([A-Za-z0-9\-]+)', re.IGNORECASE)
                pattern = re.compile(r'\b(?:serial\s*number(?:s)?|serials?|s/n)\s*:?\s*([A-Za-z0-9_\-\/]+)', re.IGNORECASE)
                for line in lines:
                    matches = pattern.findall(line)
                    for serial in matches:
                        serialCount += 1
                        #print(serial)
                        line = line.replace(serial, "*Serial Number*")
                        updated_lines.append(line)
                    updated_lines.append(line)
                file.seek(0)
                file.truncate(0)
                file.writelines(updated_lines)
        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")

        return serialCount

    #def device identifiers
    def device(self):
        deviceIdCount = 0
        try:
            with open(self.record, 'r+') as file:
                #first find the phone number we will be looking for
                lines = file.readlines()
                keyword = False
                found = False
                deviceId = ""
                deviceKeyword = {"Device:", "Device"}
                for line in lines:
                    words = line.split()
                    for word in words:
                        if not found:
                            if word in deviceKeyword:
                                keyword = True
                            elif keyword == True:
                                keyword = False
                                deviceId = word.split(":", 1)[1]
                                #print(deviceId)
                                found = True
                                break
                #loop through remainder of file and replace and count occurances that equal to Phone Number
                if deviceId != "":
                        token = "*device id*"
                        updated_lines = []
                        for line in lines:
                            occurrences = line.count(deviceId)
                            if occurrences > 0:
                                deviceIdCount+= 1
                                line = line.replace(deviceId, token)
                            updated_lines.append(line)
                        file.seek(0)
                        file.truncate(0)
                        file.writelines(updated_lines)


        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")
        
        return deviceIdCount

    #def URL
    def url(self):
        urlCount = 0
        try:
            with open(self.record, 'r+') as file:
                lines = file.readlines()
                updated_lines = []
                for line in lines:
                    # Updated regex to match URLs starting with https:// or www. and capture everything after
                    urls = re.findall(r'\b(?:https?://|www\.)[^\s]*', line)
                    for url in urls:
                        urlCount += 1
                        line = line.replace(url, "*URL*")
                    updated_lines.append(line)
                file.seek(0)
                file.truncate(0)
                file.writelines(updated_lines)
        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")
        return urlCount

    #def IP address
    def ip(self):
        ipCount = 0
        try:
            with open(self.record, 'r+') as file:
                #first find the phone number we will be looking for
                lines = file.readlines()
                keyword = False
                found = False
                ipAddress = ""
                ipKeyword = {"Internet", "IP", "IP:"}
                for line in lines:
                    words = line.split()
                    for word in words:
                        if not found:
                            if word in ipKeyword:
                                keyword = True
                            elif keyword == True:
                                keyword = False
                                ipAddress = word.split(":", 1)[1]
                                #print(deviceId)
                                found = True
                                break
                #loop through remainder of file and replace and count occurances that equal to Phone Number
                if ipAddress != "":
                        token = "*IP Address*"
                        updated_lines = []
                        for line in lines:
                            occurrences = line.count(ipAddress)
                            if occurrences > 0:
                                ip+= 1
                                line = line.replace(ipAddress, token)
                            updated_lines.append(line)
                        file.seek(0)
                        file.truncate(0)
                        file.writelines(updated_lines)


        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")
        
        return ipCount

    #def biometric identifiers

    #def full face images

    #def unique id
    def unique_code(self):
        #print("unique_code() method was called!")  # Confirm function runs
        count = 0
        try:
            with open(self.record, 'r') as file:
                lines = file.readlines()
            with open(self.record, 'w') as file:
                for line in lines:
                    if "Code:" in line:
                        #print("Code line detected:", line.strip())
                        line = re.sub(r'(Code:\s*)\d+', r'\1*ID*', line)
                        count += 1
                    file.write(line)
        except Exception as e:
            print(f"Error processing unique code: {e}")
        return count




#Record takes in the input list of PHI and addresses the necessary search functions
class Record(object):
    def __init__(self, input, outputFile):
        self.input = input
        self.algorithm = SearchRecord(outputFile)

    def find(self):
        inputs = self.input
        counts = []
        #loop through self.input and call corresponding functions in Search Record
        #print("inputs: ", inputs)14
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
            if "Email" in info or "Electronic" in info:
                #print("record email")
                email = self.algorithm.email()
                counts.append(email)
            if "Provider" in info:
                print("record provider")
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
            if "URL" in info or "Web" in info:
                #print("record URLs")
                url = self.algorithm.url()
                counts.append(url)
            if "Date" in info:
                #print("record dates")
                dates = self.algorithm.dates()
                counts.append(dates)
            if "Fax" in info:
                #print("record fax")
                fax = self.algorithm.fax()
                counts.append(fax)
            if "serial" in info:
                #print("record serial num")
                serial = self.algorithm.serial()
                counts.append(serial)
            if "Allergies" in info:
               #print("record allergies results")
                list = "".join(info[9:]).strip()
                list2 = list.strip("()").split("; ")
                allergies = self.algorithm.allergies(list2)
                counts.append(allergies)
            if "Device" in info:
                #print("record device identifiers")
                device = self.algorithm.device()
                counts.append(device)
            if "Internet" in info or "IP" in info:
                #print("record IP Address")
                ip = self.algorithm.ip()
                counts.append(ip)
            if "Medicaid" in info:
                #print("record medicaid")
                medicaid = self.algorithm.medicaid()
                counts.append(medicaid)
            elif "Account" in info:
                #print("record Acocunt")
                account = self.algorithm.account()
                counts.append(account)
            if "Unique" in info or "identifying" in info:
                #print("record unique identifying num")
                uniqueID = self.algorithm.unique_code()
                counts.append(uniqueID)
            if "Medical" in info:
                #print("record medical record num")
                medical = self.algorithm.medical_record_number()
                counts.append(medical)
            elif "Certificate" in info or "license" in info or "Certificate number" in info or "license number" in info or "Certificate/license numbers" in info:
                certificate = self.algorithm.certificate()
                license = self.algorithm.license()
                counts.append(certificate)
                counts.append(license)
            


            """
            elif "Social worker" in info:
                #print("record social worker")
                socialW = self.algorithm.socialWorker()
                counts.appened(socialW)
            elif "Fax" in info:
                #print("record fax number")
                fax = self.algorithm.fax()
                counts.append(fax)
            elif "Medical" in info
                #print("record medical record num")
                medical = self.algorithm.medical()
                counts.append(medical)
            elif "Accounts" in info:
                #print("record Account nums")
                accounts = self.algorithm.accounts()
                counts.append(accounts)
            elif "Certificate" in info or "License" in info:
                #print("record certificate/license num")
                certificate = self.algorithm.certificate()
                counts.append(certificate)
            elif "Serial" in info:
                #print("record serial num")
                serial = self.algorithm.serial()
                counts.append(serial)
            elif "URL" in info or "Web" in info:
                #print("record URLs")
                url = self.algorithm.url()
                counts.append(url)
            elif "Biometric" in info:
                #print("record biometric")
                biometric = self.algorithm.biometric()
                counts.append(biometric)
            elif "Full face" in info:
                #print("record full face images")
                face = self.algorithm.face()
                counts.append(face)
            elif "Unique" in info:
                #print("record unique identifying num")
                uniqueID = self.algorithm.uniqueID()
                counts.append(uniqueID)
            """


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
