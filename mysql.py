import os
import subprocess
import csv
from packaging import version

status = os.system('systemctl is-active --quiet mysqld.service')
mysqlPath='/home/user_name/python-project/reports/vulnerabilities-mysql.txt'
file_path = "/etc/my.cnf.d/mysql-server.cnf"
currentVersion = os.popen("mysql --version | awk -F'[ .-]' '{print $4'.'$5}'").read()


# Open the CSV file
with open('/home/user_name/python-project/csv/mysql.csv', 'r') as file:
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




# 1 mysql Version
def checkVersion():
    if(compare_versions(currentVersion, latestVersion)):
        pass
    else:
        f= open(mysqlPath, "a+")
        f.write('*** Outdate Mysql Version. Severity: High\r\n\n')
        f.close()

    
# 2 Check Bind Address
def checkbindAddress():
    command1=f"sed -n '/bind/p' '{file_path}' "
    bindAddressExists = os.popen(command1).read()
    if(bindAddressExists):
        pass
    else:
        f= open(mysqlPath, "a+")
        f.write('** Accepts all connections from the network. Severity: Medium\r\n\n')
        f.close()


# 3 Skip Show database 
def skipShowDatabase():
    command3=f"sed -n '/skip/p' '{file_path}' "
    skipDatabaseExists = os.popen(command3).read()
    if(skipDatabaseExists):
        pass
    else:
        f= open(mysqlPath, "a+")
        f.write('** Listing of other users databases is enabled. Severity: Medium\r\n\n')
        f.close()


# 4 Default port
def defaultPort():
    command4=f"sed -n '/port/p' '{file_path}' "
    portExists = os.popen(command4).read()
    if(portExists):
        pass
    else:
        f= open(mysqlPath, "a+")
        f.write('** Default port in usage. Severity: Medium\r\n\n')
        f.close()
        
        
# 5 Password Validation
def passwordValidation():
    command6=f"sed -n '/password/p' '{file_path}'"
    passwordExists = os.popen(command6).read()
    if(passwordExists):
        pass
    else:
        f= open(mysqlPath, "a+")
        f.write('** No password validation in use. Severity: Medium\r\n\n')
        f.close()


# 6 General Log
def generalLog():
    command5=f"sed -n '/general/p' '{file_path}' "
    logExists = os.popen(command5).read()
    if(logExists):
        pass
    else:
        f= open(mysqlPath, "a+")
        f.write('* No general logging enabled. Severity: Low\r\n\n')
        f.close()
        
# stores the default vulnerabilities of mysql service permanently       
def defaultVulnerabilitiesFile():
    defaultfile= "/home/user_name/python-project/default-vulnerabilities/default-mysql.txt"
    if os.path.exists(defaultfile):
        print('File Exists')
    else:
        os.system("touch /home/user_name/python-project/default-vulnerabilities/default-mysql.txt")
        os.system("sudo chown user_name:user_name /home/user_name/python-project/default-vulnerabilities/default-mysql.txt")
        os.system("cp '/home/user_name/python-project/reports/vulnerabilities-mysql.txt' '/home/user_name/python-project/default-vulnerabilities/default-mysql.txt'")
        
if(status==768):
    print('Service Not running')
    f= open(mysqlPath,"w+")
    f.write("Mysql Service is not Installed or Running. Please Verify\r\n")
    f.close()

elif(status==0):
    f= open(mysqlPath, "w+")
    f.write('Vulnerabilities for using the current default Mysql Server!!\r\n')
    f.write('Severity:  *** = High, ** = Medium, * = Low \r\n\n')
    f.close()
    checkVersion()
    checkbindAddress()
    skipShowDatabase()
    defaultPort()
    passwordValidation()
    generalLog()
    defaultVulnerabilitiesFile()





