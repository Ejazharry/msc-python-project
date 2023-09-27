import os
import subprocess
import csv
from packaging import version

status = os.system('systemctl is-active --quiet sshd.service')
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
    
    # Storing the first value 
    second_row = next(reader)

    # Storing the value of latest version
    passAuth = second_row[1]
    
    # Storing the first value 
    third_row = next(reader)

    # Storing the value of latest version
    rootLogin = third_row[1]
    
    # Storing the first value 
    fourth_row = next(reader)

    # Storing the value of latest version
    protocol = fourth_row[1]
    
    # Storing the first value 
    fifth_row = next(reader)

    # Storing the value of latest version
    timeOut = fifth_row[1]
    
    # Storing the first value 
    sixth_row = next(reader)

    # Storing the value of latest version
    replacementUsers = sixth_row[1]
    
    # Storing the first value 
    seventh_row = next(reader)

    # Storing the value of latest version
    maxAuth = seventh_row[1]




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

### Hardening SSH Server

# 1 ssh Version
def updateSSHVersion():
    if(compare_versions(currentVersion, latestVersion)):
        pass
    else:
        os.system('sudo yum upgrade -y sshd')


    
# 2 Deny Password based authentication
def passwordlessAuthentication():
    passAuthExists=os.popen("sed -n '/^[^#]*PasswordAuthentication no/p' /etc/ssh/sshd_config").read()
    if(passAuthExists):
    	pass
    else:
        os.system("sudo sed -i '/PasswordAuthentication yes/s/^#//' /etc/ssh/sshd_config")
        command1= f" sudo sed -i '/PasswordAuthentication yes/s/yes/{passAuth}/' '/etc/ssh/sshd_config'"
        os.system(command1)


# 3 Deny Users with empty passwords
def denyEmptyPasswords():
    emptyPassExists=os.popen("sed -n '/^[^#]*PermitEmptyPasswords no/p' /etc/ssh/sshd_config").read()
    if(emptyPassExists):
    	pass
    else:
        os.system("sudo sed -i '/PermitEmptyPasswords no/s/^#//' /etc/ssh/sshd_config")


# 4 Deny Root Login 
def denyRootLogin():
    rootLoginExists=os.popen("sed -n '/^[^#]*PermitRootLogin no/p' /etc/ssh/sshd_config").read()  
    if(rootLoginExists):
    	pass
    else:
        os.system("sudo sed -i '/PermitRootLogin prohibit-password/s/^#//' /etc/ssh/sshd_config")
        command2= f"sudo sed -i '/PermitRootLogin prohibit-password/s/prohibit-password/{rootLogin}/' '/etc/ssh/sshd_config'"
        os.system(command2)
    
    
# 5 Use Protocol 2 
def protocol2():
    protocolExists=os.popen('sed -n "/Protocol 2/p" /etc/ssh/sshd_config').read()
    if(protocolExists):
    	print('Exists')
    else:
    	os.system("sudo sed -i '16i\Protocol 2' /etc/ssh/sshd_config")

    
    
# 6 SSH Connection Timeout
def connectionTimeout():
    os.system("sudo sed -i '/ClientAliveInterval 0/s/^#//' /etc/ssh/sshd_config")
    command3= f"sudo sed -i '/ClientAliveInterval 0/s/0/{timeOut}/' '/etc/ssh/sshd_config'"
    os.system(command3)
    
    
# 7 Limit for password attempts
def checkMaxAuthTries():
    maxAuthExists=os.popen("sed -n '/^[^#]*MaxAuthTries 3/p' /etc/ssh/sshd_config").read()
    if(maxAuthExists):
    	print('')
    else:
    	os.system("sudo sed -i '/MaxAuthTries 6/s/^#//' /etc/ssh/sshd_config")
    	command5= f"sudo sed -i '/MaxAuthTries 6/s/6/{maxAuth}/' '/etc/ssh/sshd_config'"
    	os.system(command5)
    
    
# 8 Allow Limited Users
def limitedUsers():
    usersExists=os.popen("sed -n '/AllowUsers */p' /etc/ssh/sshd_config").read()
    if(usersExists):
        os.system("sudo sed -i '/AllowUsers/d' '/etc/ssh/sshd_config'")
        users= f"sudo sed -i '51i\{replacementUsers}' '/etc/ssh/sshd_config'"
        os.system(users)
    else:
    	command4=f"sudo sed -i '51i\{replacementUsers}' '/etc/ssh/sshd_config'"
    	os.system(command4)
    	os.system('sudo systemctl restart sshd.service')


# Calling Hardening Methods
if(status==768):
    print('Service Not running')


elif(status==0):
    updateSSHVersion()
    passwordlessAuthentication()
    denyEmptyPasswords()
    denyRootLogin()
    protocol2()
    connectionTimeout()
    checkMaxAuthTries()
    limitedUsers()

