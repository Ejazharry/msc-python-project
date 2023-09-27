import tkinter as tk
import subprocess
import os
from tkinter import messagebox


# Run the report http file to generate vulnerability report of the http service
def http_report():
    # http vulnerability report generation file
    filename = 'http.py'
    try:
        # Run the Python file using subprocess
        subprocess.run(['python', filename], check=True)
    except subprocess.CalledProcessError:
        # Handle any error that might occur during execution
        print(f"Error occurred while running {filename}")

# Run the harden http file to harden the http service
def harden_http():
    # http hardening file
    filename = 'harden-http.py'
    try:
        # Run the Python file using subprocess
        subprocess.run(['python', filename], check=True)
    except subprocess.CalledProcessError:
        # Handle any error that might occur during execution
        print(f"Error occurred while running {filename}")

# Run the report ssh file to generate vulnerability report of the ssh service
def ssh_report():
    # http vulnerability report generation file
    filename = 'ssh.py'
    try:
        # Run the Python file using subprocess
        subprocess.run(['python', filename], check=True)
    except subprocess.CalledProcessError:
        # Handle any error that might occur during execution
        print(f"Error occurred while running {filename}")

# Run the harden ssh file to harden the http service
def harden_ssh():
    # http hardening file
    filename = 'harden-ssh.py'
    try:
        # Run the Python file using subprocess
        subprocess.run(['python', filename], check=True)
    except subprocess.CalledProcessError:
        # Handle any error that might occur during execution
        print(f"Error occurred while running {filename}")
        
# Run the report mysql file to generate vulnerability report of the mysql service
def mysql_report():
    # http vulnerability report generation file
    filename = 'mysql.py'
    try:
        # Run the Python file using subprocess
        subprocess.run(['python', filename], check=True)
    except subprocess.CalledProcessError:
        # Handle any error that might occur during execution
        print(f"Error occurred while running {filename}")

# Run the harden mysql file to harden the mysql service
def harden_mysql():
    # http hardening file
    filename = 'harden-mysql.py'
    try:
        # Run the Python file using subprocess
        subprocess.run(['python', filename], check=True)
    except subprocess.CalledProcessError:
        # Handle any error that might occur during execution
        print(f"Error occurred while running {filename}")


# Run the report samba file to generate vulnerability report of the samba service
def samba_report():
    # http vulnerability report generation file
    filename = 'samba.py'
    try:
        # Run the Python file using subprocess
        subprocess.run(['python', filename], check=True)
    except subprocess.CalledProcessError:
        # Handle any error that might occur during execution
        print(f"Error occurred while running {filename}")
        

# Run the harden mysql file to harden the mysql service
def harden_samba():
    # http hardening file
    filename = 'harden-samba.py'
    try:
        # Run the Python file using subprocess
        subprocess.run(['python', filename], check=True)
    except subprocess.CalledProcessError:
        # Handle any error that might occur during execution
        print(f"Error occurred while running {filename}")
        
        
def http_report_dialog():
    http_report()
    update_csv_dialog()
    tk.messagebox.showinfo('Vulnerability Report', 'File Location: ~/python-project/reports/vulnerabilities-http.txt')

def harden_http_dialog():
    harden_http()
    tk.messagebox.showinfo('HTTPD Hardening', 'The http service is hardened successfully')
    
def ssh_report_dialog():
    ssh_report()
    update_csv_dialog()
    tk.messagebox.showinfo('Vulnerability Report', 'File Location: ~/python-project/reports/vulnerabilities-ssh.txt')

def harden_ssh_dialog():
    harden_ssh()
    tk.messagebox.showinfo('SSH Hardening', 'The ssh service is hardened successfully. Note that root logins and password based logins are now disabled')

def mysql_report_dialog():
    mysql_report()
    update_csv_dialog()
    tk.messagebox.showinfo('Vulnerability Report', 'File Location: ~/python-project/reports/vulnerabilities-mysql.txt')

def harden_mysql_dialog():
    harden_mysql()
    tk.messagebox.showinfo('MySQL Hardening', 'The mysql service is hardened successfully.')
    
def samba_report_dialog():
    samba_report()
    update_csv_dialog()
    tk.messagebox.showinfo('Vulnerability Report', 'File Location: ~/python-project/reports/vulnerabilities-samba.txt')

def harden_samba_dialog():
    harden_samba()
    tk.messagebox.showinfo('Samba Hardening', 'The samba service is hardened successfully.')

def samba_warning():
    msg_box = tk.messagebox.askquestion('Take a backup of smb.conf file', 'This process overwrites the entire samba configuration file and eliminates all sections and replaces with a custom secured [global] section. Are you okay with this ?', icon='warning')
    if msg_box == 'yes':
    	harden_samba_dialog()
    else:
        tk.messagebox.showinfo('Return', 'No changes made to the samba file')  
        
def update_csv_dialog():
    tk.messagebox.showinfo('Update CSV files', 'Please update the CSV files for all the services located at the directory - ~/python-project/csv/ before hardening')

def getConfirmation():
    msg_box2 = tk.messagebox.askquestion('Warning', 'Please make sure to enter a valid user_input, use the same user_input everytime.', icon='warning')
    if msg_box2 == 'yes':
    	enable_buttons()
    else:
        tk.messagebox.showinfo('Return', 'Update the user_input')
    
def enable_buttons():
    user_input = input_entry.get().strip()
    username = 'user_name'
    print(user_input)
    if user_input:
        os.system(f"sed -i 's/{username}/{user_input}/g' http.py")
        os.system(f"sed -i 's/{username}/{user_input}/g' mysql.py")
        os.system(f"sed -i 's/{username}/{user_input}/g' ssh.py")
        os.system(f"sed -i 's/{username}/{user_input}/g' samba.py")
        os.system(f"sed -i 's/{username}/{user_input}/g' harden-http.py")
        os.system(f"sed -i 's/{username}/{user_input}/g' harden-mysql.py")
        os.system(f"sed -i 's/{username}/{user_input}/g' harden-ssh.py")
        os.system(f"sed -i 's/{username}/{user_input}/g' harden-samba.py")
        httpissues.config(state=tk.NORMAL)
        hardenhttp.config(state=tk.NORMAL)
        sshissues.config(state=tk.NORMAL)
        hardenssh.config(state=tk.NORMAL)
        mysqlissues.config(state=tk.NORMAL)
        hardenmysql.config(state=tk.NORMAL)
        sambaissues.config(state=tk.NORMAL)
        hardensamba.config(state=tk.NORMAL)
    else:
        messagebox.showwarning("Warning", "Please enter the user_input")

# Create the Tkinter application
app = tk.Tk()
app.title("Automated Vulnerability Analysis and Hardening")


input_entry = tk.Entry(app)
input_entry.pack(pady=10)


ok_button = tk.Button(app, text="Start", command=getConfirmation)
ok_button.pack()

# Create a button to run the Python file
httpissues = tk.Button(app, text="HTTPD Vulnerability Report", bg='alice blue',command=http_report_dialog, state=tk.DISABLED)
httpissues.pack(pady=10)
hardenhttp = tk.Button(app, text="Harden HTTPD", bg='alice blue',command=harden_http_dialog, state=tk.DISABLED)
hardenhttp.pack(pady=10)

sshissues = tk.Button(app, text="SSH Vulnerability Report", bg='light cyan',command=ssh_report_dialog, state=tk.DISABLED)
sshissues.pack(pady=10)
hardenssh = tk.Button(app, text="Harden ssh", bg='light cyan',command=harden_ssh_dialog, state=tk.DISABLED)
hardenssh.pack(pady=10)

mysqlissues = tk.Button(app, text="MySQL Vulnerability Report", bg='misty rose',command=mysql_report_dialog, state=tk.DISABLED)
mysqlissues.pack(pady=10)
hardenmysql = tk.Button(app, text="Harden MySQL", bg='misty rose',command=harden_mysql_dialog, state=tk.DISABLED)
hardenmysql.pack(pady=10)

sambaissues = tk.Button(app, text="SAMBA Vulnerability Report", bg='thistle',command=samba_report_dialog, state=tk.DISABLED)
sambaissues.pack(pady=10)
hardensamba = tk.Button(app, text="Harden Samba", bg='thistle',command=samba_warning, state=tk.DISABLED)
hardensamba.pack(pady=10)

# Start the Tkinter event loop
app.geometry("650x500")
app.mainloop()



