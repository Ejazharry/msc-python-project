import os
import subprocess
import csv
from packaging import version

status = os.system('systemctl is-active --quiet smb.service')
file_path = "/etc/samba/smb.conf"
commandc = "smbd -V | awk 'NR==1{ gsub(/[^0-9.]/, \"\", $NF); print $NF }'"
currentVersion = os.popen(commandc).read().strip()
smb_conf_file = '/etc/samba/smb.conf'
custom_global_file = '/home/user_name/python-project/samba_custom_conf/secure-samba.conf'
old_ip_range = '192.168.1.0/24'

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
    
    # Storing the second value 
    second_row = next(reader)

    # Storing the value of latest version
    networkAddress = second_row[1]

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
    
# Validates wether the current version is not outdated and upgrades
def setVersion():
    if(compare_versions(currentVersion, latestVersion)):
        pass
    else:
        os.system('sudo yum update -y samba')

# Replaces the smb.conf file with the contents in the secure conf file
def replace_contents_with_custom_file(target_file_path, custom_file_path):
    try:
        # Read the contents from the custom file
        with open(custom_file_path, 'r') as custom_file:
            custom_contents = custom_file.read()

        # Open the target file in write mode and replace its contents
        with open(target_file_path, 'w') as target_file:
            target_file.write(custom_contents)

        print("Contents replaced successfully!")
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Updates the default samba host allowed IP addresses with the csv information
def replace_ip_address_range(smb_conf_file, old_range, new_range):
    with open(smb_conf_file, 'r') as file:
        file_content = file.read()

    # Perform the replacement
    new_content = file_content.replace(old_range, new_range)

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(new_content)


if(status==768):
    print('Service Not running')

elif(status==0):
    setVersion()
    replace_contents_with_custom_file(smb_conf_file, custom_global_file)
    replace_ip_address_range(smb_conf_file, old_ip_range, networkAddress)
    os.system('sudo systemctl restart smb.service')




