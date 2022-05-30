import shutil
import subprocess
import os
import sys
import tempfile
import argparse
from glob import glob1
import requests


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

Software = ""
MCVersion = ""
SoftwareVersion = ""
SrvDir = ""

scriptDir = str(os.path.dirname(os.path.realpath(__file__)))

def main():
    global Software
    consoleOutput("Welcome,")
    while True:
        Software = input("Select the desired server software:\n\033[1mSpigot | PaperMC | Vanilla\033[0m\n").casefold()
        if Software == "spigot":
            Spigot()

        elif Software == "papermc":
            PaperMC()

        elif Software == "vanilla":
            Vanilla()
            
        else:
            consoleOutput("\nTry again.")
            continue
        
        while True:
            createStartScript = input("Do you want to create a start script for your server now? \033[1m(Y/N)\033[0m\n").casefold()
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
            MCVersion = input("\033[1mPlease, input your desired Minecraft version\033[0m:\n")
            versions = requests.get("https://papermc.io/api/v2/projects/paper/versions/"+MCVersion).json()
            SoftwareVersion = versions["builds"][len(versions["builds"])-1]
            consoleOutput("Will be downloading build "+str(SoftwareVersion)+" of PaperMC.\n")
            if SoftwareVersion != 0:
                break
            else:
                consoleOutput("There was an error finding the lastest PaperMC version.\nTry again later.\n", 'red')
                continue
        except subprocess.CalledProcessError as exc:
            consoleOutput("There was an error finding the lastest PaperMC version.\nTry again later.\n", 'red')
            consoleOutput(exc.cmd)
            consoleOutput(exc.stderr)
            exit()

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
    
    server = open(SrvDir+"/server.jar", 'wb')
    server.write(requests.get("https://papermc.io/api/v2/projects/paper/versions/"+str(MCVersion)+"/builds/"+str(SoftwareVersion)+"/downloads/paper-"+str(MCVersion)+"-"+str(SoftwareVersion)+".jar").content)
    server.close()

def Run():
    if sys.platform == "win32" or sys.platform == "msys": #If it is a Windows-based OS.
        subprocess.run(args=[SrvDir+"/start.bat"])
    else:
        subprocess.run(args=["sh", SrvDir+"/start.sh"])


def Spigot():
    tmpdir = tempfile.mkdtemp()
    buildTools = open(tmpdir+"/buildtools.jar", 'wb')
    buildTools.write(requests.get("https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar").content)
    buildTools.close()

    MCVersion = input("\033[1mPlease, input your desired Minecraft version:\033[0m\n")

    os.chdir(tmpdir)
    consoleOutput("Downloading and compiling Spigot.\nThis might take a while.\n")
    try:
        subprocess.run(args=["java", "-jar", "buildtools.jar", "--rev", MCVersion])
        
    except subprocess.CalledProcessError as e:
        consoleOutput("Ended with return code "+e.returncode)
        consoleOutput(e.output)

    if not len(glob1(tmpdir, "*.jar")) == 2: # Check if server.jar was generated. There should be 2 jars: BuildTools and the server itself.
        consoleOutput("\n\nERROR: Files weren't generated correctly.\nPlesase check console outputs above to troubleshot the error.", 'red')
        input("\nPress Enter to exit...")
        exit()

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


def Vanilla():
    global MCVersion
    MCVersion = input("\033[1mPlease, input your desired Minecraft version\033[0m:\n")
    versions = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").json()
    versionJSON = ""
    versionURL = ""
    serverURL = ""
    for i in range(len(versions['versions'])):
        if (versions['versions'][i]['id'] == MCVersion):
            versionURL = versions['versions'][i]['url']
            break

    if versionURL == "":
        consoleOutput("\n\nERROR: Server version '"+MCVersion+"' couldn't be found", 'red')
        input("\033[1mPress Enter to exit...\033[0m")
        exit()
    
    else:
        versionJSON = requests.get(versionURL).json()
        serverURL = versionJSON['downloads']['server']['url']
    
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
        
        server = requests.get(serverURL).content

        file = open('server.jar', 'wb')
        file.write(server)
        file.close()


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

def Setup():
    consoleOutput("Starting setup...")

    Run()

    while True:
        EULAContent = ""
        EULA = input("\n\nYou need to agree to the Minecraft EULA in order to run a server.\nDo you agree? \033[1m(Y/N/Info)\033[0m\nNOTE: You can take profit of this moment to modify your 'server.properties' file.\n").casefold()
        if EULA == "y":
            file = open(SrvDir+"/eula.txt", "r")
            EULAContent = file.read()
            file.close()

            file = open(SrvDir+"/eula.txt", 'w')
            file.write(EULAContent.replace("false", "true"))
            file.close()

            input("Setup has been successfuly made.\nYou can start your server by running the file named 'start.sh'/'start.bat'\n\n\033[1mPress Enter to quit.\033[0m\n")
            exit()

            break
        elif EULA == "n":
            consoleOutput("Aborting...")
            exit()
        
        elif EULA == "info":
            consoleOutput("\nYou can read the eula file with your prefered text editor.\nThe file is located in:\n"+SrvDir+"/eula.txt\n")
            continue

        else:
            continue

if __name__ == "__main__":
    main()