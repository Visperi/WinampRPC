# WinampRPC

This script simply connects your Winamp with Discord rich presence and shows current track and artist.

Winamp.py is a slightly modified version of [this](https://github.com/DerpyChap/PyWinamp) winamp controller.

Fast forwarding tracks is not currently supported but I think that could be implemented pretty easily. However if you 
change the position of current track, pausing and unpausing or restarting the main.py should correct the elapsed time 
in Discord. If the trackname is less than 2 characters long it is changed to format `Track: {trackname}` (see example 3). 
This is because Discord rich presence supports only strings longer than one character.

## Requirements

- Winamp
- Python 3.6+
- `pypresence` 3.3.0+
- `pywin32` 224+

Any relatively new Winamp version should be fine. Im using the latest official version ([link](https://www.winamp.com/)).

## How to use

1. Ensure you meet the requirements
2. Download the files and place them in the same directory
3. (*optional*) Set up some custom assets
4. Run main.py while using Winamp and Discord

## Custom assets

To show album art instead of default Winamp logo, you need to:

1. Make your own Discord app for this script in their [Developer portal](https://discordapp.com/developers/applications/)
2. Make files `album_covers.json` and `album_name_exceptions.txt`
3. In `settings.json`
    * Replace the `client_id` with your app id
    * set `custom_assets` true 
    * (*optional*) Define a default asset key and text for large asset (if given, this is shown when an album asset 
    could not be found)
    * (*optional*) Define a small asset key and text (if given, this is shown when a track is playing)
4. Upload default assets with keys matching to ones given in `settings.json`
5. Upload some album assets and add corresponding `album name: asset key` pairs to `album_covers.json` (so no default 
asset keys are needed in this file)

If you have multiple albums with same names, add the duplicate album names to `album_name_exceptions.txt` each on their 
own line. These album names are then returned in format `Artist - Album name` instead of just the album name.  
Remember to take this into account when adding new keys to the api and `album_covers.json`.
 
Do note that due to restrictions in the api, following rules must be followed when adding album assets:

- There can be maximum of 300 assets for your app
- The keys must be maximum of 30 characters long
- The keys must not have any special characters (including spaces)
- The keys in `album_covers.json` and `settings.json` must be exact matches with the ones in the api

In case Discord can't find any match for asset key from their api, the asset in question is simply ignored. Therefore 
if you wish to leave the small asset out, just set the small asset key empty. Same thing applies to large 
assets. If your large asset in Discord is missing, there are no matching keys for your default large asset or album 
cover.

## Examples

As seen in these images, there should not be problem with showing any kind of characters as long as winamp can read 
them properly.

![cyrillic example](https://i.imgur.com/Llzdby7.png)
![japanese example](https://i.imgur.com/7m51K2G.png)
![short track name](https://i.imgur.com/o8nLrwI.png)
![custom asset](https://i.imgur.com/F08aPu1.png)
