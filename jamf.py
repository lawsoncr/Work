#!/usr/bin/python

import os
import tkinter as tk

#Root Window
root=tk.Tk()
root.title("Update")

tbox1 = tk.Text(root)
tbox1.place(x=3, y=2, height=30, width=300)
tbox1['borderwidth'] = 4
tbox1['relief'] = 'sunken'

##Code to run 

def main():
    #get list of updates
    up_list = os.popen("softwareupdate -l").read()
    
    ##if macOS update grab name and then 

    if 'Label: macOS' in up_list:
        x = (up_list.split("macOS",1)[1])
        y = x.split("\n",1)
        up_name= y[0]
    else: print ('no')

    #os.system(softwareupdate -i 'NAME')
    print(up_list)
    tbox1.insert("end-1c", "softwareupdate -i" + up_name)
    

main()

root.mainloop()
