# MCAutoSetup
## Requirements
 - [Python 3.x](https://www.python.org/downloads/)
 - Libraries in [requirements.txt](https://github.com/GospelBG/AutoSetup/blob/3e8ec8ed9ea3fb2e0beb1388e5534dea795947fc/requirements.txt)
 - [Java](https://java.com/)  

You can easily install the required libraries using the following command on your console:  
`python3 -m pip install -r path-to-repo/requirements.txt`

## Compatible server software
 - [Spigot](https://spigotmc.org)
 - [PaperMC](https://papermc.io)
 - [Vanilla](https://www.minecraft.net/download/server)
 - You can add your own scripts to the [servers](/servers/) folder. See [Creating custom scripts](#creating-custom-scripts).

## Flags
### Disable colored output 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `--nocolor`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This tool uses a library called `termcolor`.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; If you are unable to use this library, this flag will skip this library's calls and normally print output to the terminal.

## Creating custom scripts
You can create your own scripts to add support to any server software not that doesen't figure in the [list](#compatible-server-software). The script must handle the download of the server files and **return the server jarfile as bytes.**

Please use the `consoleOutput` function from `main.py` to print output to the console. You may add any color as an argument after the output message. Refer to [termcolor's Readme file](https://github.com/termcolor/termcolor#text-properties) to see a full list of text properties.