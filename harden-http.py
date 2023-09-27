import os
import subprocess
import csv
from packaging import version


status = os.system('systemctl is-active --quiet httpd.service')
file_path = '/etc/httpd/conf/httpd.conf'
specific_line = 'ServerRoot "/etc/httpd"'
specific_line_for_directoryListing = '<Directory "/var/www/html">'
currentVersion = os.popen("httpd -v | grep -oP 'Apache\/\K\d+\.\d+\.\d+'").read()


# Open the CSV file
with open('/home/user_name/python-project/csv/http.csv', 'r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)

    # Ignoring the first line
    next(reader)

    # Storing the first value 
    first_row = next(reader)

    # Storing the value of latest version
    latestVersion = first_row[1]
    
    # Storing the second value
    second_row = next(reader)

    # Storing the value of serverToken 
    serverTokenValue = second_row[1]

    # Storing the third row
    third_row = next(reader)

    # Storing the value for serverSignatures
    serverSignatureValue = third_row[1]

    # Storing the fourth row
    fourth_row = next(reader)

    # Storing the value for directory listing
    directoryListingValue = fourth_row[1]
    
    # Storing the fifth row
    fifth_row = next(reader)

    # Storing the value for eTag
    eTagValue = fifth_row[1]
    
    # Storing the sixth row
    sixth_row = next(reader)

    # Storing the value for trace value
    traceValue = sixth_row[1]
    
    # Storing the seventh row
    seventh_row = next(reader)

    # Storing the value for trace value
    customPort = seventh_row[1]
    
    # Storing the eight row
    eigth_row = next(reader)

    # Storing the value for limit values
    limitValue1 = eigth_row[1]
    limitValue2 = eigth_row[2]
    limitValue3 = eigth_row[3]


    
# Function to insert a line after a give specific line 
def insert_line_after_specific_line(file_path, specific_line, new_line):
    # Read the contents of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the index of the specific line
    try:
        line_index = lines.index(specific_line + '\n')
    except ValueError:
        print("Specific line not found in the file.")
        return

    # Insert the new line after the specific line
    lines.insert(line_index + 1, new_line + '\n')

    # Write the modified contents back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
        
# Function to compare any two given versions
def compare_versions(version1, version2):
    v1 = list(map(int, version1.split('.')))
    v2 = list(map(int, version2.split('.')))

    for i in range(max(len(v1), len(v2))):
        n1 = v1[i] if i < len(v1) else 0
        n2 = v2[i] if i < len(v2) else 0

        if n1 < n2:
            return False
        elif n1 > n2:
            return True

    return True  # Versions are equal  
    
    
# 1 Http Version
def httpVersion():
    if(compare_versions(currentVersion, latestVersion)):
        pass
    else:
        os.system('yum upgrade -y httpd')

# 2 ServerTokens
def serverTokens():
    serverTokenExists = os.popen("sed -n '/ServerTokens Prod/p' /etc/httpd/conf/httpd.conf").read()
    if(serverTokenExists):
        pass
    else:
        insert_line_after_specific_line(file_path, specific_line, serverTokenValue)


# 3 ServerSignature
def serverSignature():
    serverSignatureExists = os.popen("sed -n '/ServerSignature Off/p' /etc/httpd/conf/httpd.conf").read()
    if(serverSignatureExists):
        pass
    else:
        insert_line_after_specific_line(file_path, specific_line, serverSignatureValue)

# 4 Directory Listing
def directoryListing():
    indexesExists = os.popen("sed -n '/Options Indexes/p' /etc/httpd/conf/httpd.conf").read()
    directoryListingExists = os.popen("sed -n '/Options -Indexes/p' /etc/httpd/conf/httpd.conf").read()
    if(directoryListingExists):
        pass
    elif(indexesExists):
        os.system("sed -i '/Options Indexes/s/Indexes/-&/' /etc/httpd/conf/httpd.conf")
        os.system("sed -i '/Options -Indexes FollowSymLinks/s/FollowSymLinks/+&/' /etc/httpd/conf/httpd.conf")    
    
    
# 5 Etag Header
def fileETag():
    etagExists = os.popen("sed -n '/FileETag None/p' /etc/httpd/conf/httpd.conf").read()
    if(etagExists):
        pass
    else:
        insert_line_after_specific_line(file_path, specific_line, eTagValue)
    
    
# 6 Limit HTTP Request Methods
def limitHttpRequestMethods():
    limitExists = os.popen('sed -n "/LimitExcept GET POST HEAD/p" /etc/httpd/conf/httpd.conf').read()
    if(limitExists):
        pass
    else:
        insert_line_after_specific_line(file_path, specific_line_for_directoryListing, limitValue1)
        insert_line_after_specific_line(file_path, limitValue1, limitValue2)
        insert_line_after_specific_line(file_path, limitValue2, limitValue3)
    
    
# 7 Trace Enable Off
def traceEnable():
    traceExists = os.popen("sed -n '/TraceEnable off/p' /etc/httpd/conf/httpd.conf").read()
    if(traceExists):
        pass
    else:
        insert_line_after_specific_line(file_path, specific_line, traceValue)
    
# 8 Change Default Port
def changePort():
    defaultPort = os.popen("sed -n '/Listen 80/p' /etc/httpd/conf/httpd.conf").read()
    if(defaultPort):
        commanddemo=f"sed -i '/Listen 80/s/80/{customPort}/' '/etc/httpd/conf/httpd.conf'"
        os.system(commanddemo)
    	
# 9 TimeOut 30 Seconds
def timeoutSeconds():
    timeoutValue = os.popen('sed -n "/Timeout 30/p" /etc/httpd/conf/httpd.conf').read()
    if(timeoutValue):
        pass
    else:
        insert_line_after_specific_line(file_path, specific_line, 'Timeout 30')


if(status==768):
    print('Service Not running')

elif(status==0):
    httpVersion()
    serverTokens()
    serverSignature()   
    directoryListing()
    fileETag()
    traceEnable()
    limitHttpRequestMethods()
    changePort()
    timeoutSeconds()
    os.system('systemctl restart httpd.service')
    os.system('systemctl daemon-reload')


 
    
