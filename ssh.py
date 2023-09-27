import os
import subprocess
import csv
from packaging import version

status = os.system('systemctl is-active --quiet sshd.service')
sshPath='/home/user_name/python-project/reports/vulnerabilities-ssh.txt'
file_path = '/etc/ssh/sshd_config'
currentVersion = os.popen("ssh -V 2>&1 | grep -oP 'OpenSSH_\K[0-9.]+'").read() 


# Open the CSV file
with open('/home/user_name/python-project/csv/ssh.csv', 'r') as file:
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



### Vulnerability Report

# 1 checking ssh Version
def checkVersion():
    if(compare_versions(currentVersion, latestVersion)):
        pass
    else:
        f= open(sshPath, "a+")
        f.write('*** Outdate SSH Version. Severity: High\r\n')
        f.close()


# 2 Password based authentication
def checkPasswordlessAuthentication():
    passAuthExists=os.popen("sed -n '/^[^#]*PasswordAuthentication no/p' /etc/ssh/sshd_config").read()
    if(passAuthExists):
    	pass
    else:
    	f= open(sshPath, "a+")
    	f.write('*** Password Authentication must be denied. Severity: High\r\n')
    	f.close()


# 3 Users with empty passwords
def checkEmptyPasswords():
    emptyPassExists=os.popen("sed -n '/^[^#]*PermitEmptyPasswords no/p' /etc/ssh/sshd_config").read()
    if(emptyPassExists):
    	pass
    else:
    	f= open(sshPath, "a+")
    	f.write('*** Accepting Empty Passwords. Severity: High\r\n')
    	f.close()
     
     
# 4 Deny Root Login  
def checkRootLogin():
    rootLoginExists=os.popen("sed -n '/^[^#]*PermitRootLogin no/p' /etc/ssh/sshd_config").read()  
    if(rootLoginExists):
    	pass
    else:
    	f= open(sshPath, "a+")
    	f.write('*** Root Login via SSH is enabled. Severity: High\r\n')
    	f.close()


# 7 Limit for password attempts
def checkMaxAuthTries():
    maxAuthExists=os.popen("sed -n '/^[^#]*MaxAuthTries 3/p' /etc/ssh/sshd_config").read()
    if(maxAuthExists):
    	pass
    else:
    	f= open(sshPath, "a+")
    	f.write('** No limit for password attempts. Severity: Medium\r\n')
    	f.close()


# 6 Limit ssh access to limited users
def checkLimitedUsers():
    limitedUsers=os.popen("sed -n '/AllowUsers */p' /etc/ssh/sshd_config").read()
    if(limitedUsers):
    	pass
    else:
    	f= open(sshPath, "a+")
    	f.write('** No Restricted Access. Severity: Medium\r\n')
    	f.close()
    
    
# 7 Use Protocol 2 
def checkProtocol2():
    protocol2Exists=os.popen("sed -n '/Protocol 2/p' /etc/ssh/sshd_config").read()
    if(protocol2Exists):
    	pass
    else:
    	f= open(sshPath, "a+")
    	f.write('* Accepts outdated protocol versions. Severity: Low\r\n')
    	f.close()


# 8 SSH Connection Timeout
def checkConnectionTimeout():
    timeoutExists=os.popen("sed -n '/ClientAliveInterval 180/p' /etc/ssh/sshd_config").read()
    if(timeoutExists):
    	pass
    else:
    	f= open(sshPath, "a+")
    	f.write('* No Timeout set for Ideal Connections. Severity: Low\r\n')
    	f.close()

# stores the default vulnerabilities of ssh service permanently       
def defaultVulnerabilitiesFile():
    defaultfile= "/home/user_name/python-project/default-vulnerabilities/default-ssh.txt"
    if os.path.exists(defaultfile):
        print('File Exists')
    else:
        os.system("touch /home/user_name/python-project/default-vulnerabilities/default-ssh.txt")
        os.system("sudo chown user_name:user_name /home/user_name/python-project/default-vulnerabilities/default-ssh.txt")
        os.system("cp '/home/user_name/python-project/reports/vulnerabilities-ssh.txt' '/home/user_name/python-project/default-vulnerabilities/default-ssh.txt' ")

    
if(status==768):
    print('Service Not running')
    f= open(sshPath,"w+")
    f.write("SSH Service is not Installed or Running. Please Verify\r\n")
    f.close()

elif(status==0):
    f= open(sshPath, "w+")
    f.write('Vulnerabilities for using the current default SSH Server!!\r\n')
    f.write('Severity:  *** = High, ** = Medium, * = Low \r\n\n')
    f.close()
    checkVersion()
    checkPasswordlessAuthentication()
    checkEmptyPasswords()
    checkRootLogin()
    checkMaxAuthTries()
    checkLimitedUsers()
    checkProtocol2()
    checkConnectionTimeout()
    defaultVulnerabilitiesFile()


# Calling Vulnerability Analysis Methods





