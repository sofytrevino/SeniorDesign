#phiSearch.py
#command line: python phiSearch.py phi1.txt JMS.txt

import sys
import re
import string
import streamlit as st

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
        self.retrievedWords = {}
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
                    self.retrievedWords["*name*"] = Name
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
                        address_index = 0
                        updated_lines = []
                        for line in lines:
                            for Address in addressFound:
                                if Address in line:
                                    token = f"*address{address_index}*"
                                    self.retrievedWords[token] = Address
                                    line = line.replace(Address, token)
                                    address_index += 1
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
                    self.retrievedWords["*DoB*"] = DoB
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
                    self.retrievedWords["*SSN*"] = SSN
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
                        self.retrievedWords["*phone*"] = Phone
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
                        self.retrievedWords["*email*"] = Email
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
                    self.retrievedWords["*Provider*"] = Provider
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
                    self.retrievedWords["*HospitalName*"] = Hospital
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
                        self.retrievedWords["*Medicaid Account*"] = Medicaid
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
                    self.retrievedWords["*Account*"] = Account
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
                lines = file.readlines()
                updated_lines = []
                date_pattern = r'\b\d{1,2}/\d{1,2}/\d{4}\b'
                dates_found = set()

                # First: collect all unique dates
                for line in lines:
                    matches = re.findall(date_pattern, line)
                    for match in matches:
                        dates_found.add(match)

                # Then: replace and track them
                for line in lines:
                    for i, date in enumerate(dates_found):
                        token = f"*Date{i}*"
                        if token not in self.retrievedWords:
                            self.retrievedWords[token] = date
                        count = line.count(date)
                        if count > 0:
                            datesCount += count
                            line = line.replace(date, token)
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
                        self.retrievedWords["*Social Worker*"] = SocialWorker
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
        mrnCount = 0
        try:
            with open(self.record, 'r+') as file:
                lines = file.readlines()
                updated_lines = []
                mrn_pattern = r'\bTX[A-Z0-9]{4,}-[A-Z0-9]{4,}\b'  # matches formats like TXB4459-BS34334
                mrns_found = set()

                # Find all MRNs in file
                for line in lines:
                    matches = re.findall(mrn_pattern, line)
                    for match in matches:
                        mrns_found.add(match)

                # Replace MRNs with tokens and build mapping
                for line in lines:
                    for i, mrn in enumerate(mrns_found):
                        token = f"*MedicalRecordNumber*"
                        if token not in self.retrievedWords:
                            self.retrievedWords[token] = mrn
                        count = line.count(mrn)
                        if count > 0:
                            mrnCount += count
                            line = line.replace(mrn, token)
                    updated_lines.append(line)

                file.seek(0)
                file.truncate(0)
                file.writelines(updated_lines)

        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")

        return mrnCount
    
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

                license_found = set()
                license_pattern = r'license number:\s*[A-Z]{2,}\d{2,}-\d{3,}'  # e.g., license number: MD77-786123

                for line in lines:
                    matches = re.findall(license_pattern, line, flags=re.IGNORECASE)
                    for match in matches:
                        # Extract just the license ID part after the colon
                        license_id = match.split(":")[1].strip()
                        license_found.add(license_id)

                for line in lines:
                    for i, lic in enumerate(license_found):
                        token = f"*LicenseNumber*"
                        if token not in self.retrievedWords:
                            self.retrievedWords[token] = lic
                        count = line.count(lic)
                        if count > 0:
                            licenseCount += count
                            line = line.replace(lic, token)
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

                # Match serial numbers like B1001-7786432 or SN-00112233
                serial_pattern = r'\b[A-Z]{1,5}\d{2,}-\d{4,}\b'
                serials_found = set()

                for line in lines:
                    matches = re.findall(serial_pattern, line)
                    for match in matches:
                        serials_found.add(match)

                for line in lines:
                    for i, serial in enumerate(serials_found):
                        token = f"*SerialNumber*"
                        if token not in self.retrievedWords:
                            self.retrievedWords[token] = serial
                        count = line.count(serial)
                        if count > 0:
                            serialCount += count
                            line = line.replace(serial, token)
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
                        token = "*deviceID*"
                        self.retrievedWords["*deviceID*"] = deviceId
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
                        token = "*IPAddress*"
                        self.retrievedWords["*IPAddress*"] = ipAddress
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
    def biometric(self):
        biometricCount = 0
        try:
            with open(self.record, 'r+') as file:
                # Find the social worker's name
                lines = file.readlines()
                keyword = False
                found = False
                biometric = ""
                for line in lines:
                    if not found and ("Biometric:" in line or "biometric:" in line):
                        parts = line.split(":", 1)
                        if len(parts) > 1:
                            biometric = parts[1].strip()
                            found = True
                            break
                
                # Replace occurrences of the social worker's name
                if biometric:
                    token = "*biometrics*"
                    self.retrievedWords["*biometrics*"] = biometric
                    updated_lines = []
                    for line in lines:
                        occurrences = line.count(biometric)
                        if occurrences > 0:
                            biometricCount += occurrences
                            line = line.replace(biometric, token)
                        updated_lines.append(line)
                    file.seek(0)
                    file.truncate(0)
                    file.writelines(updated_lines)

        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")
            
        return biometricCount


    #def full face images

    #def unique id
    def unique_code(self):
        codeCount = 0
        try:
            with open(self.record, 'r+') as file:
                lines = file.readlines()
                updated_lines = []

                codes_found = set()
                code_pattern = r'Code:\s*\d{5,}'  # Matches "Code:772980014"

                for line in lines:
                    matches = re.findall(code_pattern, line)
                    for match in matches:
                        # Extract just the numeric part (after "Code:")
                        code_number = match.split(":")[1].strip()
                        codes_found.add(code_number)

                for line in lines:
                    for i, code in enumerate(codes_found):
                        token = f"*Code*"
                        if token not in self.retrievedWords:
                            self.retrievedWords[token] = code
                        count = line.count(code)
                        if count > 0:
                            codeCount += count
                            line = line.replace(code, token)
                    updated_lines.append(line)

                file.seek(0)
                file.truncate(0)
                file.writelines(updated_lines)

        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")

        return codeCount
    
    #health plan ID
    def healthPlan(self):
        healthPlan_count = 0
        healthPlan_pattern = re.compile(r'\b\d{3}-\d{4}-\d{4}\b')  # matches 888-6765-1110 format
        try:
            with open(self.record, 'r+') as file:
                lines = file.readlines()
                updated_lines = []
                found_health_plan = None

                for line in lines:
                    match = healthPlan_pattern.search(line)
                    if match:
                        found_health_plan = match.group()
                        break  # Only redact the first one (based on your logic)

                if found_health_plan:
                    token = "*HealthPlanID*"
                    self.retrievedWords[token] = found_health_plan  # Store for re-identification

                    for line in lines:
                        count = line.count(found_health_plan)
                        if count > 0:
                            healthPlan_count += count
                            line = line.replace(found_health_plan, token)
                        updated_lines.append(line)

                    file.seek(0)
                    file.truncate(0)
                    file.writelines(updated_lines)

        except FileNotFoundError:
            print(f"Error: File '{self.record}' not found.")

        return healthPlan_count




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
            if "Certificate" in info or "license" in info or "Certificate number" in info or "license number" in info or "Certificate/license numbers" in info:
                certificate = self.algorithm.certificate()
                license = self.algorithm.license()
                counts.append(certificate)
                counts.append(license)
            if "Biometric" in info:
                #print("record biometric record")
                biometricInfo = self.algorithm.biometric()
                counts.append(biometricInfo)
            if "Health" in info:
                #print("record health ID")
                healthID = self.algorithm.healthPlan()
                counts.append(healthID)
            


        return counts

    

def main():


    st.title("De-identification program")

    name = st.text_input("Enter input file")
    name2 = st.text_input("Enter medical file")
    if(st.button('Enter')):
        inputFile = name.title()
        recordFile = name2.title()
       
        outputFile = "NewJMS.txt"

        with open(recordFile, 'r') as source, open(outputFile, "w") as destination:
            destination.write(source.read())

        parseInfo = Parsing(inputFile)
        infoList = parseInfo.parse()

        search = Record(infoList, outputFile)
        found = search.find()

        retrievedWordsFile = "retrievedwords.txt"
        with open(retrievedWordsFile, 'w') as f:
            for token, word in search.algorithm.retrievedWords.items():
                f.write(f"{token} {word}\n")

        print("PHI Final Count: ", found)

    st.subheader("Re-identification program")
    name3 = st.text_input("Enter text file")
    name4 = st.text_input("Enter output file")
    if(st.button('Submit')):
        retrievedWordsFile = name3.title()
        deidentifiedFile = name4.title()
        #st.success(retrievedWordsFile)
        #st.success(deidentifiedFile)

        reidentifiedFile = "Reidentified.txt"
        reident_map = {}
        with open(retrievedWordsFile, 'r') as f:
            for line in f:
                parts = line.strip().split(' ', 1)
                if len(parts) == 2:
                    token, realword = parts
                    reident_map[token] = realword

        with open(deidentifiedFile, 'r') as file:
            content = file.read()

        for token, realword in reident_map.items():
            content = content.replace(token, realword)

        with open(reidentifiedFile, 'w') as file:
            file.write(content)

        print(f"Reidentification complete output written to {reidentifiedFile}")


   
if __name__ == "__main__":
    main()

    

# python phiSearch.py deidentify PHI3.txt "ehr EC 3 .txt"
# python phiSearch.py reidentify retrievedwords.txt NewJMS.txt
