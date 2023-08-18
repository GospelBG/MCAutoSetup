import requests
import subprocess
from main import consoleOutput

def install():
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
        
    serverURL ="https://papermc.io/api/v2/projects/paper/versions/"+str(MCVersion)+"/builds/"+str(SoftwareVersion)+"/downloads/paper-"+str(MCVersion)+"-"+str(SoftwareVersion)+".jar"
    return requests.get(serverURL).content