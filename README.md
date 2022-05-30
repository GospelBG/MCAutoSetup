# Minecraft Server Setup
## Requirements
 - [Python 3.x](https://www.python.org/downloads/)
 - Libraries in [requirements.txt](https://github.com/GospelBG/AutoSetup/blob/3e8ec8ed9ea3fb2e0beb1388e5534dea795947fc/requirements.txt)
 - In some cases you will need [Java](https://java.com/).
 
 ### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;How to install libraries in `requirements.txt`
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; You can easily install the requirements using the following command:  
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`python3 -m pip install -r path-to-repo/requirements.txt`

## Compatible server Software
 - [SpigotMC](https://spigotmc.org)
 - [PaperMC](https://papermc.io)
 - [Vanilla](https://minecraft.net/)

## Flags
### - Disable colored output 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `--nocolor`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This tool uses a library called `termcolor`.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; If you are unable to use this library, this flag will skip this library and still output to the terminal.