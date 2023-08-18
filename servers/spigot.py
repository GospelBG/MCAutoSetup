from main import consoleOutput
import tempfile
import requests
import os
import subprocess
from glob import glob1

def install():
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
    else:
        jarfile = open("spigot-"+MCVersion+".jar", 'rb')
        return jarfile.read()