import os
import sys
import argparse
from pathlib import Path
import importlib
import subprocess


parser = argparse.ArgumentParser()

parser.add_argument('--nocolor', help="If you are having compatibility issues with the colored text to run the script without colored text.", action='store_true')

args = parser.parse_args()
if not args.nocolor:
    from termcolor import colored

def consoleOutput(content, color=""):
    if args.nocolor:
        color = ""
    
    if color == "":
        print(content)
    else:
        print(colored(content, color))

scriptDir = str(os.path.dirname(os.path.realpath(__file__)))

def main():
    options = []
    for file in os.listdir(os.path.join(scriptDir, "servers")):
        if file.endswith(".py"):
            options.append(Path(file).stem.capitalize().replace("mc", "MC"))

    consoleOutput("Welcome,")
    while True:
        Software = input("Select the desired server software:\n"+ " | ".join(options) + "\n").casefold()

        for i in options:
            if Software == i.casefold():
                server = importlib.import_module("servers."+i.casefold())
                install = getattr(server, 'install')
                jar = install()

        Setup(jar)
        exit()

def Run():
    if sys.platform == "win32" or sys.platform == "msys": #If it is a Windows-based OS.
        subprocess.run(args=[SrvDir+"/start.bat"])
    else:
        subprocess.run(args=["sh", SrvDir+"/start.sh"])

def createScript():
    script = ""
    args = ""
    extension = ""

    if sys.platform == "win32" or sys.platform == "msys": #If it is a Windows-based OS.
        script = open(scriptDir+"/deps/startWindows.bat", 'r').read()
        extension = "bat"
    else:
        script = open(scriptDir+"/deps/startUNIX.sh", 'r').read()
        extension = "sh"
    
    while True:
        initialRAM = input("Input the initial amount of RAM for the server \033[1m(MB)\033[0m\n")
        try:
            if int(initialRAM) > 0:
                break
            else:
                continue
        except ValueError:
            consoleOutput("Please, enter a valid number", 'yellow')
            continue
        
    while True:
        maximumRAM = input("Input the maximum amount of RAM available for the server \033[1m(MB)\033[0m\n")
        try:
            if int(maximumRAM) > 0:
                break
            else:
                continue
        except ValueError:
            consoleOutput("Please, enter a valid number", 'yellow')
            continue 
    
    args = "-Xms"+initialRAM+"m -Xmx"+maximumRAM+"m"

    script = script.replace(r'{args}', args)

    file = open(SrvDir+"/start."+extension, 'w')
    file.write(script)
    file.close()

def Setup(jar):
    while True:
        global SrvDir
        path = input("\033[1mPlease enter the path where you want your server to be in\033[0m"+" "+colored("(the directory will be created if it does not exist yet)", 'yellow')+":\n")
        
        if os.path.exists(path) and os.path.isdir(path):
            SrvDir = path
            os.chdir(SrvDir)
            break
        else:
            consoleOutput("Creating directory "+path+"...")
            SrvDir = path
            os.mkdir(SrvDir)
            os.chdir(SrvDir)
            continue
    
    file = open(SrvDir+"/server.jar", 'wb')
    file.write(jar)
    file.close()

    while True:
        answer = input("Create a launch script? [Y/n]\n")
        if answer == "" or answer.casefold() == "y":
            createScript()
            break
        elif answer.casefold() == "n":
            consoleOutput("Please place your start.sh/start.bat/start.cmd file in the server folder to proceed.")
            consoleOutput("Otherwise, this script won't be able to continue.", "red")
            input("\nPress enter to continue...")
            break

    consoleOutput("Starting setup...")

    Run()

    while True:
        EULAContent = ""
        EULA = input("\nYou need to agree to the Minecraft EULA in order to run a server.\nDo you agree? \033[1m(Y/N/Info)\033[0m\nNOTE: You can take profit of this moment to modify your 'server.properties' file.\n").casefold()
        if EULA == "y":
            file = open(SrvDir+"/eula.txt", "r")
            EULAContent = file.read()
            file.close()

            file = open(SrvDir+"/eula.txt", 'w')
            file.write(EULAContent.replace("false", "true"))
            file.close()

            input("Setup has been successfuly made.\nYou can start your server by running the file named 'start.sh'/'start.bat'\n\n\033[1mPress Enter to quit.\033[0m\n")
            exit()

        elif EULA == "n":
            consoleOutput("Aborting...")
            exit()
        
        elif EULA == "info":
            consoleOutput("\nYou can read the eula file with your prefered text editor.\nThe file is located in:\n"+SrvDir+"/eula.txt")
            continue

        else:
            continue

if __name__ == "__main__":
    main()