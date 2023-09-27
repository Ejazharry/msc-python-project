import os
import subprocess
import csv
from packaging import version


status = os.system('systemctl is-active --quiet httpd.service')
httpPath='/home/user_name/python-project/reports/vulnerabilities-http.txt'
file_path = '/etc/httpd/conf/httpd.conf'
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


# Change Default Port
def checkChangePort():
    defaultPort = os.popen("sed -n '/Listen 80/p' /etc/httpd/conf/httpd.conf").read()
    if(defaultPort):
    	f= open(httpPath, "a+")
    	f.write('*** Apache Server is hosted on Default Port. Severity - High \r\n\n')
    	f.close()
    	

# Http Version
def checkVersion():
    if(compare_versions(currentVersion, latestVersion)):
        pass
    else:
        f= open(httpPath, "a+")
        f.write('*** Outdate Apache Version. Severity - High\r\n\n')
        f.close()


# Directory Listing
def checkDirectoryListing():
    directoryListingExists = os.popen("sed -n '/Options -Indexes/p' /etc/httpd/conf/httpd.conf").read()
    if(directoryListingExists):
        pass
    else:
        f= open(httpPath, "a+")
        f.write('*** Directory Listing is active. Severity - High\r\n\n')
        f.close()


# Limit HTTP Request Methods
def checkLimitHttpRequestMethods():
    limitExists = os.popen('sed -n "/LimitExcept GET POST HEAD/p" /etc/httpd/conf/httpd.conf').read()
    if(limitExists):
        pass
    else:
        f= open(httpPath, "a+")
        f.write('** Server accepts all HTTP request methods. Severity - Medium\r\n\n')
        f.close()
        
        
# ServerTokens
def checkServerTokens():
    serverTokenExists = os.popen("sed -n '/ServerTokens Prod/p' /etc/httpd/conf/httpd.conf").read()
    if(serverTokenExists):
        pass
    else:
        f= open(httpPath, "a+")
        f.write('** The server name, operating system & version and architecture information are disclosed in the response header. Severity - Medium\r\n\n')
        f.close()
    


# ServerSignature
def checkServerSignature():
    serverSignatureExists = os.popen("sed -n '/ServerSignature Off/p' /etc/httpd/conf/httpd.conf").read()
    if(serverSignatureExists):
        pass
    else:
        f= open(httpPath, "a+")
        f.write('** ServerSignature is enabled, the server displays the version info on the default and error pages. Severity - Medium\r\n\n')
        f.close()



# Etag Header
def checkFileETag():
    etagExists = os.popen("sed -n '/FileETag None/p' /etc/httpd/conf/httpd.conf").read()
    if(etagExists):
        pass
    else:
        f= open(httpPath, "a+")
        f.write('** Information disclosure through FileETag header. Severity - Medium\r\n\n')
        f.close()


# Trace Enable Off
def checkTraceEnable():
    traceExists = os.popen("sed -n '/TraceEnable off/p' /etc/httpd/conf/httpd.conf").read()
    if(traceExists):
        pass
    else:
        f= open(httpPath, "a+")
        f.write('** Cross site tracing attack through telnet. TraceEnable is active. Severity - Medium\r\n\n')
        f.close()

    
# TimeOut 30 Seconds
def checkTimeoutSeconds():
    timeoutValue = os.popen("sed -n '/Timeout 30/p' /etc/httpd/conf/httpd.conf").read()
    if(timeoutValue):
        pass
    else:
        f= open(httpPath, "a+")
        f.write('* No timeout configuration, possibility of SlowLoris and DDoS attack. Severity - Low\r\n\n')
        f.close()

# This file contains the Vulnerabilities of the default http config file
def defaultVulnerabilitiesFile():
    defaultfile= "/home/user_name/python-project/default-vulnerabilities/default-http.txt"
    if os.path.exists(defaultfile):
        pass
    else:
        os.system("touch /home/user_name/python-project/default-vulnerabilities/default-http.txt")
        os.system("sudo chown user_name:user_name /home/user_name/python-project/default-vulnerabilities/default-http.txt")
        os.system("cp '/home/user_name/python-project/reports/vulnerabilities-http.txt' '/home/user_name/python-project/default-vulnerabilities/default-http.txt'")
        
if(status==768):
    print('Service Not running')
    f= open(httpPath,"w+")
    f.write("Apache Service is not Installed or Running. Please Verify\r\n\n")
    f.close()

elif(status==0):
    f= open(httpPath, "w+")
    f.write('Vulnerabilities for using the current default Apache Server!!\r\n')
    f.write('Severity:  *** = High, ** = Medium, * = Low \r\n\n')
    f.close()
    checkChangePort()
    checkVersion()
    checkDirectoryListing()
    checkLimitHttpRequestMethods()
    checkServerTokens()
    checkServerSignature()
    checkFileETag()
    checkTraceEnable()
    checkTimeoutSeconds()
    defaultVulnerabilitiesFile()





