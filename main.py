import shutil
import subprocess
import os
import sys
import tempfile

import requests

Software = ""
MCVersion = ""
SoftwareVersion = ""
SrvDir = ""

scriptDir = str(os.path.dirname(os.path.realpath(__file__)))

def main():
    global Software
    print("Welcome,")
    while True:
        Software = input("Select the desired server software:\nSpigot | PaperMC | Vanilla\n").casefold()
        if Software == "spigot":
            Spigot()

        elif Software == "papermc":
            PaperMC()

        elif Software == "vanilla":
            Vanilla()
            
        else:
            print("\nTry again.")
            continue
        
        while True:
            createStartScript = input("Do you want to create a start script for your server now? (Y/N)\n").casefold()
            if createStartScript == "y":
                createScript()
                break
            elif createStartScript == "n":
                exit()
            else:
                continue
        
        Setup()
        exit()


def PaperMC():
    global MCVersion
    global SoftwareVersion
    while True:
        try:
            MCVersion = input("Please, input your desired Minecraft version:\n")
            versions = requests.get("https://papermc.io/api/v2/projects/paper/versions/"+MCVersion).json()
            SoftwareVersion = versions["builds"][len(versions["builds"])-1]
            print("Will be downloading build "+str(SoftwareVersion)+" of PaperMC.\n")
            if SoftwareVersion != 0:
                break
            else:
                print("There was an error finding the lastest PaperMC version.\nTry again later.\n")
                continue
        except subprocess.CalledProcessError as exc:
            print("There was an error finding the lastest PaperMC version.\nTry again later.\n")
            print(exc.cmd)
            print(exc.stderr)
            exit()

    while True:
        global SrvDir
        path = input("Please enter the path where you want your server to be in (all files in it will be deleted):\n")
        
        if os.path.exists(path) and os.path.isdir(path):
            SrvDir = path
            shutil.rmtree(SrvDir)
            os.mkdir(SrvDir)

            os.chdir(SrvDir)
            break
        else:
            print("Couldn't find the selected directory. Try again.")
            continue
    
    server = open(SrvDir+"/server.jar", 'wb')
    server.write(requests.get("https://papermc.io/api/v2/projects/paper/versions/"+str(MCVersion)+"/builds/"+str(SoftwareVersion)+"/downloads/paper-"+str(MCVersion)+"-"+str(SoftwareVersion)+".jar").content)
    server.close()

def Run():
    if sys.platform == "win32" or sys.platform == "msys": #If it is a Windows-based OS.
        subprocess.run(args=[SrvDir+"/start.bat"])
    else:
        subprocess.run(args=["sh", SrvDir+"/start.sh"])


def Spigot():
    buildTools = open(tempfile.gettempdir()+"/buildtools.jar", 'wb')
    buildTools.write(requests.get("https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar").content)
    buildTools.close()

    MCVersion = input("Please, input your desired Minecraft version:\n")

    os.chdir(tempfile.gettempdir())
    try:
        subprocess.run(args=["java", "-jar", "buildtools.jar", "--rev", MCVersion])
    except subprocess.CalledProcessError as e:
        print("Ended with return code "+e.returncode)
        print(e.output)
    

def Vanilla():
    print("Vanilla")

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
        initialRAM = input("Input the initial amount of RAM for the server (MB)\n")
        try:
            if int(initialRAM) > 0:
                break
            else:
                continue
        except ValueError:
            print("Please, enter a valid number")
            continue
        
    while True:
        maximumRAM = input("Input the maximum amount of RAM available for the server (MB)\n")
        try:
            if int(maximumRAM) > 0:
                break
            else:
                continue
        except ValueError:
            print("Please, enter a valid number")
            continue 
    
    args = "-Xms"+initialRAM+"m -Xmx"+maximumRAM+"m"

    script = script.replace(r'{args}', args)

    file = open(SrvDir+"/start."+extension, 'w')
    file.write(script)
    file.close()

def Setup():
    print("Starting setup...")

    Run()

    while True:
        EULAContent = ""
        EULA = input("You need to agree to the Minecraft EULA in order to run a server.\nDo you agree? (Y/N/Info)\nNOTE: You can take profit of this moment to modify your 'server.properties' file.\n").casefold()
        if EULA == "y":
            file = open(SrvDir+"/eula.txt", "r")
            EULAContent = file.read()
            file.close()

            file = open(SrvDir+"/eula.txt", 'w')
            file.write(EULAContent.replace("false", "true"))
            file.close()

            input("Setup has been successfuly made.\nYou can start your server by running the file named 'start.sh'/'start.bat'\n\nPress Enter to quit.\n")
            exit()

            break
        elif EULA == "n":
            print("Aborting...")
            exit()
        
        elif EULA == "info":
            print("\nYou can read the eula file with your prefered text editor.\nThe file is located in:\n"+SrvDir+"/eula.txt\n")
            continue

        else:
            continue

if __name__ == "__main__":
    main()