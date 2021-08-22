import os
import re
from pathlib import Path

def getFiles():
    global filelist
    global location
    if location[-1] == "/":
        filelist = os.listdir(location)
    else:
        location = location + "/"
        filelist = os.listdir(location) 

while (True):
    location = input("Enter the FULL path to the sound directory without quotes (e.g. '/home/saltmaster/eData/4'):")
    locpath = Path(location)
    if locpath.exists():
        getFiles()
        break

for file in filelist:
    if re.match(".*\.dat$", file):
        os.system("xxd -ps -c 10000000000 " + location + file + " > " + location + file + ".dump")
        print("xxd -ps -c 10000000000 " + location + file + " > " + location + file + ".dump")

getFiles()
for file in filelist:
    if re.match(".*\.dump$", file):
        with open(location + file) as reversify:
            global lines
            lines = reversify.readlines()

        s = lines[0]
        compiled = ''.join([ s[x:x+2][::-1] for x in range(0, len(s), 2) ])
        try:
            with open(location + file + ".swapped" , "w+") as swappedfile:
                print("Writing " + swappedfile.name + "...")
                swappedfile.write(compiled)
                print("Write complete!")
        except:
            print("Error while writing file, cannot continue.")
            exit()

getFiles()
for file in filelist:
    if re.match(".*\.swapped$", file):
        swapped = file
        os.system("xxd -p -r " + location + swapped + " > " + location + file + ".wav")
        print("xxd -p -r " + location + swapped + " > " + location + file + ".wav")


