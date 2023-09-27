import os
import subprocess
import csv
from packaging import version

status = os.system('systemctl is-active --quiet mysqld.service')
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
    
    # Storing the second value 
    second_row = next(reader)

    # Storing the value of bindaddress 
    bindAddress = second_row[1]
    
    # Storing the third value 
    third_row = next(reader)

    # Storing the value of localFile 
    localFile = third_row[1]
    
    # Storing the fourth value 
    fourth_row = next(reader)

    # Storing the value of skip database 
    skipDatabase = fourth_row[1]
    
    # Storing the fifth value 
    fifth_row = next(reader)

    # Storing the value of port
    addPort = fifth_row[1]
    
    # Storing the sixth value 
    sixth_row = next(reader)

    # Storing the value of general log
    generalLog = sixth_row[1]
    
    # Storing the seventh value 
    seventh_row = next(reader)

    # Storing the value of general log
    validatePassword1 = seventh_row[1]
    validatePassword2 = seventh_row[2]
    validatePassword3 = seventh_row[3]
    validatePassword4 = seventh_row[4]

    
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
def setVersion():
    if(compare_versions(currentVersion, latestVersion)):
        pass
    else:
        os.system('sudo yum upgrade -y mysql-server')

    
# 2 Check Bind Address
def setbindAddress():
    command1=f"sed -n '/bind/p' '{file_path}'"
    bindAddressExists = os.popen(command1).read()
    if(bindAddressExists):
        pass
    else:
    	os.system("sudo sed -i '$a\\"+ bindAddress + "' /etc/my.cnf.d/mysql-server.cnf")


# 3 Skip Show database 
def setShowDatabase():
    command3=f"sed -n '/skip/p' '{file_path}' "
    skipDatabaseExists = os.popen(command3).read()
    if(skipDatabaseExists):
        pass
    else:
        os.system("sudo sed -i '$a\\"+ skipDatabase + "' /etc/my.cnf.d/mysql-server.cnf")


# 4 Default port
def setDefaultPort():
    command4=f"sed -n '/port/p' '{file_path}' "
    portExists = os.popen(command4).read()
    if(portExists):
        pass
    else:
        os.system("sudo sed -i '$a\\port = "+ addPort + "' /etc/my.cnf.d/mysql-server.cnf")
        os.system("sudo semanage port -a -t mysqld_port_t -p tcp "+addPort+"")


# 5 Password Validation
def setPasswordValidation():
    command6=f"sed -n '/password/p' '{file_path}'"
    passwordExists = os.popen(command6).read()
    if(passwordExists):
        pass
    else:
        os.system("sudo sed -i '$a\\"+ validatePassword1 + "' /etc/my.cnf.d/mysql-server.cnf")
        os.system("sudo sed -i '$a\\"+ validatePassword2 + "' /etc/my.cnf.d/mysql-server.cnf")
        os.system("sudo sed -i '$a\\"+ validatePassword3 + "' /etc/my.cnf.d/mysql-server.cnf")
        os.system("sudo sed -i '$a\\"+ validatePassword4 + "' /etc/my.cnf.d/mysql-server.cnf")
        
        
# 6 General Log
def setGeneralLog():
    command5=f"sed -n '/general/p' '{file_path}' "
    logExists = os.popen(command5).read()
    if(logExists):
        pass
    else:
        os.system("sudo sed -i '$a\\"+ generalLog + "' /etc/my.cnf.d/mysql-server.cnf")
       
        

if(status==768):
    print('Service Not running')

elif(status==0):
    setVersion()
    setbindAddress()
    setShowDatabase()
    setDefaultPort()
    setGeneralLog()
    setPasswordValidation()
    os.system('sudo systemctl restart mysqld.service')
    os.system('sudo systemctl daemon-reload')




