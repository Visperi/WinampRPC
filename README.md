# WinampRPC
This script simply connects your Winamp with Discord rich presence and shows current track and artist.

Winamp.py is a slightly modified version of [this](https://github.com/DerpyChap/PyWinamp) winamp controller. Unfortunately I dont know how to make Winamp plugins so the rp.py console needs to be always running. So far I have not encountered any problems while using this script.

Fast forwarding tracks is not currently supported but I think that could be implemented pretty easily. However if you change the position of current track, pausing and unpausing or restarting the rp.py should correct the elapsed time in Discord. If the trackname is less than 2 characters long it is changed to format `Track: {trackname}` (see example 3). This is because Discord rich presence supports only strings longer than one character.

# Requirements
- Winamp
- Python 3.6+
- `pypresence` 3.3.0+
- `pywin32` 224+

Code could work with older python versions if you convert f-strings into older format. Any relatively new Winamp version should be fine. Im using the newest official version ([link](https://www.winamp.com/)).

# How to use
1. Ensure you meet the requirements
2. Download the files and place them in the same directory
3. Run rp.py while using winamp

# Examples
As seen in these images, there should not be problem with showing any kind of characters.

![cyrillic example](https://i.imgur.com/Llzdby7.png)
![japanese example](https://i.imgur.com/7m51K2G.png)
![short trackname](https://i.imgur.com/o8nLrwI.png)
