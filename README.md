# WinampRPC

A script reading playing status from Winamp and connecting it to Discord rich presence with images.

Winamp.py is a standalone Winamp controller module fleshed out for modern python with OOP in mind. It was originally 
based on controller made by DerpyChap, which can be found from his 
[PyWinamp repository](https://github.com/DerpyChap/PyWinamp).

Fast-forwarding tracks is not currently supported. If the track position is changed, pausing and un-pausing the track 
or restarting `main.py` should correct the elapsed time in Discord. If the track name is one character long, 
it is changed to format `Track: {track_name}`. This is due to Discord rich presence supporting only strings at least 
two characters long.

## Requirements

The minimum Python version supported is 3.8.

- Winamp
- `pypresence`
- `pywin32`

Any relatively new Winamp version should be fine. Versions starting from 5.0 should be safe.

## How to use

1. Clone the repository
2. (*optional*) Set up some custom assets
3. Run main.py while using Winamp and Discord

In case there are some troubles with pywin32 especially after updating Python, running pip upgrade command should 
solve this: `python -m pip install --upgrade pywin32`.  

## Custom assets

Getting custom images to the rich presence is rather simple:

1. Create a new Discord app for WinampRPC in Discords' [Developer portal](https://discordapp.com/developers/applications/) 
2. Make files `album_covers.json` and `album_name_exceptions.txt`
3. In `settings.json`
    * Replace the `client_id` with the new Discord app ID
    * set `custom_assets` True
    * (*optional*) Define a default asset key and text for large asset. If given, this image is shown when an album 
    asset cannot be found from Discord API
    * (*optional*) Define a small asset key and text. If given, this is shown when a track is playing
4. Upload default assets with keys matching to ones given in `settings.json` (if any)
5. Upload some album assets and add corresponding `album name: asset_key` pairs to `album_covers.json`. The default 
asset keys are not needed in this file.

If there are many albums with same name, the album name must be added to `album_name_exceptions.txt` each on their own 
line for the assets to work. For these albums the assets are searched in format `artist - album name` instead of only 
the album name. Naturally this must also be taken into account when saving the assets into Discord API.
 
Due to restrictions in the Discord asset API, following rules must be met with custom assets:

- There can be maximum of 300 assets for an application
- The asset keys cannot be longer than 30 characters long
- The keys cannot have any special characters, including spaces
- The asset keys in `album_covers.json` and `settings.json` must be exact matches with the ones in asset API

If there are no matches for an asset key in Discord API, they are simply ignored. Therefore, if ignoring large or 
small asset is needed, it is possible by leaving their asset keys empty. This also means if WinampRPC is working but 
assets are not appearing, there are no matches between Discord API and the asset keys in local files.

## Examples

As these images show, there should not really be problem with any kind of alphabet as long as they are supported in 
UTF-8.

![cyrillic example](https://i.imgur.com/Llzdby7.png)
![japanese example](https://i.imgur.com/7m51K2G.png)
![short track name](https://i.imgur.com/o8nLrwI.png)
![custom asset](https://i.imgur.com/F08aPu1.png)
