##onsync.Export.csv
##frontline export desktop to go 
## run at 6 am 

import os
import PyInstaller
 
# Function to rename multiple files
def main():
   
    folder = "/Users/clawson/Desktop/frontline export"

    
    for filename in enumerate(os.listdir(folder)):
        
        subname = "OneSync"

        if filename != None:
            dst = f"OneSync.csv"
            src =f"{folder}/{filename}"  # foldername/filename, if .py file is outside folder
            dst =f"{folder}/{dst}"
            
            # rename() function will
            # rename all the files
            os.rename(src, dst)
        else:
            print("Not Found!")

main()
