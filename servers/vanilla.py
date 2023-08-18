import requests
#from main import consoleOutput

def install():
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
        return requests.get(serverURL).content