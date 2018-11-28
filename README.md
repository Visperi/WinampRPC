# WinampRPC
This script simply makes a rich presence into Discord and shows the track and artist you are playing. Winamp.py is a slightly modified version of [this](https://github.com/DerpyChap/PyWinamp) winamp controller. Unfortunately I dont know how to make Winamp plugins so the rp.py console needs to be always running. So far I have not encountered any problems while using this script.

Fast forwarding tracks is not currently supported but I think that could be implemented pretty easily. However if you change the position of current track, pausing and unpausing on rebooting the rp.py should correct the elapsed time in Discord. If the trackname is less than 2 characters long it is changed to format `Track: {trackname}` (see example 3). This is because Discord rich presence supports only strings longer thans one character.

# Requirements
- Winamp
- Python 3.6+
- `pypresence` 3.3.0+ (May work with earlier versions too)

# How to use
1. Ensure you meet the requirements
2. Download the files and place them in the same directory
3. Run rp.py while using winamp

# Examples

![cyrillic example](https://i.imgur.com/Llzdby7.png)
![japanese example](https://i.imgur.com/7m51K2G.png)
![short trackname](https://i.imgur.com/o8nLrwI.png)
