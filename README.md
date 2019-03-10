# WinampRPC

This script simply connects your Winamp with Discord rich presence and shows current track and artist.

Winamp.py is a slightly modified version of [this](https://github.com/DerpyChap/PyWinamp) winamp controller.

Fast forwarding tracks is not currently supported but I think that could be implemented pretty easily. However if you 
change the position of current track, pausing and unpausing or restarting the main.py should correct the elapsed time 
in Discord. If the trackname is less than 2 characters long it is changed to format `Track: {trackname}` (see example 3). 
This is because Discord rich presence supports only strings longer than one character.

# Requirements

- Winamp
- Python 3.6+
- `pypresence` 3.3.0+
- `pywin32` 224+

Any relatively new Winamp version should be fine. Im using the latest official version ([link](https://www.winamp.com/)).

# How to use

1. Ensure you meet the requirements
2. Download the files and place them in the same directory
3. Run main.py while using winamp

# Custom assets

To show album art instead of default Winamp logo, you need to:
 
1. Make your own Discord app for this script
2. Replace the client_id to your app id and set custom_assets true in `settings.json`
3. Define the default large asset key and text (if any) in `settings.json`
3. Define the small asset key and text (if any) in `settings.json`
4. Upload some assets and add `album name: asset key` pairs to `album_covers.json` (excet the default large asset and small asset)
 
Do note that due to restrictions in the api, following rules must be followed when making asset keys:

- The keys must be maximum of 30 characters long
- The keys must not have any special characters (including spaces)
- The keys in `album_covers.json` and `settings.json` must be exact matches with the ones in the api

# Examples

As seen in these images, there should not be problem with showing any kind of characters as long as winamp can read 
them properly.

![cyrillic example](https://i.imgur.com/Llzdby7.png)
![japanese example](https://i.imgur.com/7m51K2G.png)
![short track name](https://i.imgur.com/o8nLrwI.png)
