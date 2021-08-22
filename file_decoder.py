import os
import re
from pathlib import Path
import platform
import shutil
import argparse

parser = argparse.ArgumentParser()

flagswitch = parser.add_mutually_exclusive_group()

flagswitch.add_argument("-c", "--convert", help="Convert files to standard readable format", action="store_true")
parser.add_argument("-d", "--directory", help="Data directory (e.g. '/home/saltmaster/eData/4')", required=True)
parser.add_argument("-f", "--format", help="File format", choices=["wav", "x"], required=True)
parser.add_argument("-k", "--keep", help="Keep (swapped) hex dumps", action="store_true")
flagswitch.add_argument("-r", "--revert", help="Revert changes to files in game readable format", action="store_true")

args = parser.parse_args()

if args.convert:
    infile = "dat"
    outfile = args.format
elif args.revert:
    infile = args.format
    outfile = "dat"
else:
    infile = "dat"
    outfile = args.format

def destiny():
    if not args.keep:
        os.remove(location + file)

def getFiles():
    global filelist
    global location
    if location[-1] == "/" or location[-1] == "\\":
        filelist = os.listdir(location)
    else:
        if platform.system() == "Windows":
            location = location + "\\"
        else:
            location = location + "/"
        filelist = os.listdir(location) 

location = args.directory
getFiles()

for file in filelist:
    if re.match(".*\." + infile + "$", file):
        print("xxd -ps -c 10000000000 " + location + file + " > " + location + file + ".dump")
        os.system("xxd -ps -c 10000000000 " + location + file + " > " + location + file + ".dump")

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
        destiny()

getFiles()
for file in filelist:
    if re.match(".*\.swapped$", file):
        swapped = file
        print("xxd -p -r " + location + swapped + " > " + location + file + "." + outfile)
        os.system("xxd -p -r " + location + swapped + " > " + location + file + "." + outfile)
        shutil.move(location + file + "." + outfile, location + re.match("^[0-9]{1,6}\.", file).group(0) + outfile)
        destiny()

