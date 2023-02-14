#Connor Lawson 
#Program to Configure Network switches

 
import os
import tkinter as tk
import tkinter.ttk
import paramiko
import time
import netmiko
from netmiko import ConnectHandler
from PIL import ImageTk, Image 

#Root Window
root=tk.Tk()
root.title("HCS Network App")

# setting the window size
root.geometry("800x800")
image1 = Image.open("hcs.png")

test = ImageTk.PhotoImage(image1)

label1 = tkinter.Label(image=test)
label1.image = test

label1.place(x=25, y=200)
  
# declaring string variable
# for storing switch info
os_var=tk.StringVar()
sw_var=tk.StringVar()
s_var=tk.StringVar()
loc_var=tk.StringVar()
h_var=tk.StringVar()

#Output box for switch config
tbox1 = tk.Text(root)
tbox1.place(x=265, y=2, height=500, width=500)
tbox1['borderwidth'] = 4
tbox1['relief'] = 'sunken'

window_width = 250
window_heigth = 500

# Create frames inside the root window to hold other GUI elements. All frames must be created in the main program, otherwise they are not accessible in functions. 
first_frame=tkinter.ttk.Frame(root, width=window_width, height=window_heigth)
first_frame['borderwidth'] = 4
first_frame['relief'] = 'sunken'
first_frame.grid(column=0, row=9, padx=5, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))

def create_widgets_in_first_frame():
    # Create the label for the frame
    ##Below code is for gui display 
    tlabel = tk.Label(first_frame, text = 'Switch Config', font=('calibre',10, 'bold'))

    #OS
    os_label = tk.Label(first_frame, text = 'OS', font=('calibre',10, 'bold'))
    os_entry = tk.Entry(first_frame,textvariable = os_var, font=('calibre',10,'normal'))

    #switch size
    sw_label = tk.Label(first_frame, text = 'Switch Size', font = ('calibre',10,'bold'))
    sw_entry=tk.Entry(first_frame, textvariable = sw_var, font = ('calibre',10,'normal'))

    #School
    s_label = tk.Label(first_frame, text = 'School', font = ('calibre',10,'bold'))
    s_entry=tk.Entry(first_frame, textvariable = s_var, font = ('calibre',10,'normal'))

    #Switch Location
    sl_label = tk.Label(first_frame, text = 'Location', font = ('calibre',10,'bold'))
    sl_entry=tk.Entry(first_frame, textvariable = loc_var, font = ('calibre',10,'normal'))

    #host address
    h_label = tk.Label(first_frame, text = 'Host address', font = ('calibre',10,'bold'))
    h_entry=tk.Entry(first_frame, textvariable = h_var, font = ('calibre',10,'normal'))
    
    # creating a button using the widget
    # Button that will call the submit function
    sub_btn=tk.Button(first_frame,text = 'Submit', command = submit)


    # Create the button for the frame
    first_window_quit_button = tkinter.Button(first_frame, text = "Quit", command = quit_program)
    first_window_quit_button.grid(column=0, row=9, pady=10, sticky=(tkinter.N))
    first_window_next_button = tkinter.Button(first_frame, text = "Next", command = call_second_frame_on_top)
    first_window_next_button.grid(column=1, row=9, pady=10, sticky=(tkinter.N))

    # placing the label and entry in
    # the required position using grid
    # method
    tlabel.grid(row=0,column=1)
    os_label.grid(row=1,column=0)
    os_entry.grid(row=1,column=1)
    sw_label.grid(row=2,column=0)
    sw_entry.grid(row=2,column=1)
    s_label.grid(row=3,column=0)
    s_entry.grid(row=3,column=1)
    sl_label.grid(row=4,column=0)
    sl_entry.grid(row=4,column=1)
    h_label.grid(row=5,column=0)
    h_entry.grid(row=5,column=1)
    sub_btn.grid(row=7,column=1)

  
# defining a function that will
# get the switch info
# print them on the screen
def submit():
 
    user_os=os_var.get()
    sw_size=sw_var.get()
    school = s_var.get()
    location = loc_var.get()
    host = h_var.get()
     
    print("OS : " + user_os)
    print("Switch size: " + sw_size)
    print("Enter school : " + school)
    print("Switch Location: " + location)
    print("Host: " + host)

    if int(host) <= 254:
        sw_config(school, location, host, sw_size, user_os)
    else:
        print ("Error IP out of bounds") 

    os_var.set("")
    sw_var.set("")
    s_var.set("")
    loc_var.set("")
    h_var.set("")

def sw_config(school, location, host, sw_size, user_os):
    
    subnets = {
        "removed senistive information"
    }
    
    sub = subnets[school]
    subnet = ("**"+ sub + "****")

    ip = ("***"+ sub +"***" + host)
    ip_list = [ip]

    if user_os == "Win":
        ping_win(ip_list, school, location, subnet, sw_size, host, sub, ip, user_os)
        
    elif user_os != "Win":
        ping_mac(ip_list, school, location, subnet, sw_size, host, sub, ip, user_os)



def ping_win(ip_list, school, location, subnet, sw_size, host, sub, ip, user_os):
    
    for i in ip_list:
        response = os.popen(f"ping {i}").read()

    if "Approximate round trip" in response:
            tbox1.delete('1.0', tk.END)
            tbox1.insert("end-1c", ip + " active\n")
            tbox1.insert("end-1c", "Enter a new host address")
            host = input("")

            if int(host) <= 254:
                sw_config(school, location, host, sw_size, user_os)
            else:
                print ("Error IP out of bounds")
    else:
            print(f"DOWN {ip} IP not active")
            out(school, location, subnet, host, sub, sw_size)

def ping_mac(ip_list, school, location, subnet, sw_size, host, sub, ip, user_os):

    for i in ip_list:
        response = os.popen(f"ping -t 3 {i}").read()

    if "round-trip" in response:
            tbox1.delete('1.0', tk.END)
            tbox1.insert("end-1c", ip + " active\n")
            tbox1.insert("end-1c", "Enter a new host address")
            host = input("")

            if int(host) <= 254:
                sw_config(school, location, host, sw_size, user_os)
            else:
                print ("Error IP out of bounds")
                
    else:
            print(f"DOWN {ip} IP not active")
            out(school, location, subnet, host, sub, sw_size)
            
#Output config for switch
def out(school, location, subnet, host, sub, sw_size):
    tbox1.delete('1.0', tk.END)
    tbox1.insert("end-1c", " \n")
    tbox1.insert("end-1c", "hostname " + school + "-" + "SW" + "-" +location + " \n")
    tbox1.insert("end-1c", " \n")
    tbox1.insert("end-1c", "timesync sntp\n")
    tbox1.insert("end-1c", "sntp unicast\n")
    tbox1.insert("end-1c", "sntp server priority 1 *******\n")
    tbox1.insert("end-1c", "time daylight-time-rule continental-us-and-canada\n")
    tbox1.insert("end-1c", "time timezone -300\n")
    tbox1.insert("end-1c", " \n")
    tbox1.insert("end-1c", "ip default-gateway " + subnet + " \n")
    tbox1.insert("end-1c", " \n")
    tbox1.insert("end-1c", "snmp-server community “public” unrestricted\n")
    tbox1.insert("end-1c", "snmp-server host ******* community “public” \n")
    tbox1.insert("end-1c", "snmp-server contact “************”\n")
    tbox1.insert("end-1c", " \n") 
    tbox1.insert("end-1c", "*******\n")
    tbox1.insert("end-1c", "\tname “*******”\n")
    if int(sw_size) == 8:
        tbox1.insert("end-1c","\tno untagged 8\n")
    tbox1.insert("end-1c","\tip address ***"+ sub +"***" + host + " **********\n")
    tbox1.insert("end-1c","\texit\n")
    ##vlan 100
    if len(sub) == 1:
        tbox1.insert("end-1c","******" + sub + "\n")
    else:
        tbox1.insert("end-1c","******" + sub + "\n")
    if int(sw_size) == 8:
        tbox1.insert("end-1c","\ttagged 8-10\n")
        tbox1.insert("end-1c","\tname “***************”\n")
        tbox1.insert("end-1c","\tno ip address\n")
        tbox1.insert("end-1c","\texit\n")
    ##vlan 200
    if len(sub) == 1:
        tbox1.insert("end-1c","******" + sub + "\n")
    else:
        tbox1.insert("end-1c","******" + sub + "\n")
    if int(sw_size) == 8:
        tbox1.insert("end-1c","\tuntagged 8\n")
        tbox1.insert("end-1c","\ttagged 9-10\n")
        tbox1.insert("end-1c","\tname “**********”\n")
        tbox1.insert("end-1c","\tno ip address\n")   
        tbox1.insert("end-1c","\texit\n")
    tbox1.insert("end-1c","loop-protect 1-" + sw_size + "\n")
    tbox1.insert("end-1c","no dhcp config-file-update\n")
    tbox1.insert("end-1c", " \n") 
    tbox1.insert("end-1c","password *********\n")
    tbox1.insert("end-1c","*********\n")
    tbox1.insert("end-1c","*********\n")
    tbox1.insert("end-1c", " \n")
    tbox1.insert("end-1c","password operator user-name “*****”\n")
    tbox1.insert("end-1c","********\n")
    tbox1.insert("end-1c","********\n")
    tbox1.insert("end-1c", " \n")
    tbox1.insert("end-1c", "********\n")
    tbox1.insert("end-1c","*********\n")





##Code Below is for SSH into a switch.

ip_var=tk.StringVar()

second_frame=tkinter.ttk.Frame(root, width=window_width, height=window_heigth)
second_frame['borderwidth'] = 2
second_frame['relief'] = 'sunken'
second_frame.grid(column=1, row=9, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))

def create_widgets_in_second_frame():
    # Create the label for the frame
    t2label = tk.Label(second_frame, text = 'Switch SSH', font=('calibre',10, 'bold'))

    #Enter IP
    ip_label = tk.Label(second_frame, text = 'IP', font=('calibre',10, 'bold'))
    ip_entry = tk.Entry(second_frame,textvariable = ip_var, font=('calibre',10,'normal'))

    #Connect Button
    sub_btn2=tk.Button(second_frame,text = 'Connect', command = sw_ssh)

    #Uptime Button
    v_btn2=tk.Button(second_frame,text = 'Uptime')
    v_btn2.grid(row=7,column=1)

    t2label.grid(row=0,column=1)
    ip_label.grid(row=1,column=0)
    ip_entry.grid(row=1,column=1)
    sub_btn2.grid(row=2,column=1)

    # Create the button for the frame
    second_window_back_button = tkinter.Button(second_frame, text = "Back", command = call_first_frame_on_top)
    second_window_back_button.grid(column=0, row=15, pady=10, sticky=(tkinter.N))
    second_window_next_button = tkinter.Button(second_frame, text = "Next", command = call_third_frame_on_top)
    second_window_next_button.grid(column=1, row=15, pady=10, sticky=(tkinter.N))


#Method to SSH into switch

def sw_ssh():

    ip2 = ip_var.get()

    tbox1.delete('1.0', tk.END)
    tbox1.insert("end-1c", ip2 + "\n")

    device = ConnectHandler(device_type='aruba_os', ip=ip2, username='*****', password='******')
    tbox1.insert("end-1c", "Connected\n")
    device.disconnect()

def uptime(device):

    output = device.send_command("show version")
    tbox1.insert("end-1c", output)
    device.disconnect()


def create_widgets_in_third_frame():
    # Create the label for the frame
    third_window_label = tkinter.ttk.Label(third_frame, text='Window 3')
    third_window_label.grid(column=0, row=0, pady=10, padx=10, sticky=(tkinter.N))

    # Create the button for the frame
    third_window_back_button = tkinter.Button(third_frame, text = "Back", command = call_second_frame_on_top)
    third_window_back_button.grid(column=0, row=1, pady=10, sticky=(tkinter.N))
    third_window_quit_button = tkinter.Button(third_frame, text = "Quit", command = quit_program)
    third_window_quit_button.grid(column=1, row=1, pady=10, sticky=(tkinter.N))

def call_first_frame_on_top():
    # This function can be called only from the second window.
    # Hide the second window and show the first window.
    second_frame.grid_forget()
    first_frame.grid(column=1, row=9, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))

def call_second_frame_on_top():
    # This function can be called from the first and third windows.
    # Hide the first and third windows and show the second window.
    first_frame.grid_forget()
    third_frame.grid_forget()
    second_frame.grid(column=1, row=9, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))

def call_third_frame_on_top():
    # This function can only be called from the second window.
    # Hide the second window and show the third window.
    second_frame.grid_forget()
    third_frame.grid(column=1, row=9, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))

def quit_program():
    root.destroy()

third_frame=tkinter.ttk.Frame(root, width=window_width, height=window_heigth)
third_frame['borderwidth'] = 2
third_frame['relief'] = 'sunken'
third_frame.grid(column=1, row=9, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))

# Create all widgets to all frames
create_widgets_in_third_frame()
create_widgets_in_second_frame()
create_widgets_in_first_frame()

# Hide all frames in reverse order, but leave first frame visible (unhidden).
third_frame.grid_forget()
second_frame.grid_forget()
  
# performing an infinite loop
# for the window to display
root.mainloop()
