import os
import subprocess
import csv
from packaging import version

status = os.system('systemctl is-active --quiet smb.service')
sambaPath='/home/user_name/python-project/reports/vulnerabilities-samba.txt'
file_path = "/etc/samba/smb.conf"
commandc = "smbd -V | awk 'NR==1{ gsub(/[^0-9.]/, \"\", $NF); print $NF }'"
currentVersion = os.popen(commandc).read().strip()



# Open the CSV file
with open('/home/user_name/python-project/csv/samba.csv', 'r') as file:
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


# 1 samba Version
def checkVersion():
    if(compare_versions(currentVersion, latestVersion)):
        pass
    else:
        f= open(sambaPath, "a+")
        f.write('*** Outdate samba Version. Severity: High\r\n\n')
        f.close()
        
        
# 2 Disable guest access
def checkguestAccess():
    command4=f"sed -n '/guest ok = no/p' '{file_path}' "
    guestAccess = os.popen(command4).read()
    if(guestAccess):
        pass
    else:
        f= open(sambaPath, "a+")
        f.write('*** Guest access is allowed. Severity: High\r\n\n')
        f.close()
        
        
# 3 Hosts allowed and denied by restricting access to specific IP addresses
def checkHostsAllowed():
    command3=f"sed -n '/hosts allow/p' '{file_path}' "
    hostsAllowed = os.popen(command3).read()
    if(hostsAllowed):
        pass
    else:
        f= open(sambaPath, "a+")
        f.write('*** Accepts connections from all devices. Severity: High\r\n\n')
        f.close()    


# 4 Max Connections
def checkMaxConnections():
    command1=f"sed -n '/max connections/p' '{file_path}' "
    maxConnectionsExists = os.popen(command1).read()
    if(maxConnectionsExists):
        pass
    else:
        f= open(sambaPath, "a+")
        f.write('** Multiple active connections is allowed. Severity: High\r\n\n')
        f.close()
 
    
# 5 SMB Encrypt
def checkSMBEncrypt():
    command2=f"sed -n '/smb encrypt/p' '{file_path}' "
    smbEncryptExists = os.popen(command2).read()
    if(smbEncryptExists):
        pass
    else:
        f= open(sambaPath, "a+")
        f.write('** Accepts unencrypted connections. Severity: High\r\n\n')
        f.close()


# 6 Encrypt password
def encryptPasswords():
    command8=f"sed -n '/encrypt passwords/p' '{file_path}' "
    encryptPasswords = os.popen(command8).read()
    if(encryptPasswords):
        pass
    else:
        f= open(sambaPath, "a+")
        f.write('*** Passwords are not encrypted. Severity: High\r\n\n')
        f.close()
        


# 7 Limiting protocol versions to SMB2 and SMB3
def checkProtocolVersions():
    command5=f"sed -n '/min protocol/p' '{file_path}' "
    minProtocol = os.popen(command5).read()
    if(minProtocol):
        pass
    else:
        f= open(sambaPath, "a+")
        f.write('* Accepts outdated protocols. No Protocol Validation. Severity: Low \r\n\n')
        f.close()
        
        
# 8 Logging
def checkLogging():
    command9=f"sed -n '/log level/p' '{file_path}' "
    logLevel = os.popen(command9).read()
    if(logLevel):
        pass
    else:
        f= open(sambaPath, "a+")
        f.write('* No Logging enabled. Severity: Low\r\n')
        f.close()

# stores the default vulnerabilities of samba service permanently              
def defaultVulnerabilitiesFile():
    defaultfile= "/home/user_name/python-project/default-vulnerabilities/default-samba.txt"
    if os.path.exists(defaultfile):
        print('File Exists')
    else:
        os.system("touch /home/user_name/python-project/default-vulnerabilities/default-samba.txt")
        os.system("sudo chown user_name:user_name /home/user_name/python-project/default-vulnerabilities/default-samba.txt")
        os.system("cp '/home/user_name/python-project/reports/vulnerabilities-samba.txt' '/home/user_name/python-project/default-vulnerabilities/default-samba.txt'")
        
if(status==768):
    print('Service Not running')
    f= open(sambaPath,"w+")
    f.write("samba Service is not Installed or Running. Please Verify\r\n")
    f.close()

elif(status==0):
    f= open(sambaPath, "w+")
    f.write('Vulnerabilities for using the current default samba Server!!\r\n')
    f.write('Severity:  *** = High, ** = Medium, * = Low \r\n\n')
    f.close()
    checkVersion()
    checkguestAccess()
    checkHostsAllowed()
    checkMaxConnections()
    checkSMBEncrypt()
    encryptPasswords()
    checkProtocolVersions()
    checkLogging()
    defaultVulnerabilitiesFile()
    





