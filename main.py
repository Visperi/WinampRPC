"""
MIT License

Copyright (c) 2018-2019 Visperi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from pypresence import Presence
import time
import winamp
import os
import json

# Get the directory where this script was executed to ensure python can find .json files
main_path = os.path.dirname(__file__)


def get_settings():
    with open(f"{main_path}\\settings.json") as settings_file:
        settings = json.load(settings_file)

    return settings["client_id"], settings["default_asset_key"], settings["default_asset_name"], \
        settings["small_asset_key"], settings["small_asset_text"], settings["custom_assets"]


client_id, default_large_key, default_large_text, small_asset_key, small_asset_text, custom_assets = get_settings()

w = winamp.Winamp()
winamp_version = w.getVersion()
rpc = Presence(client_id)
rpc.connect()

previous_track = ""
cleared = False

# If boolean custom_assets is set True, try to load file for album assets
if custom_assets:
    try:
        # File for album cover assets is loaded only when starting the script so restart is needed when new albums
        # are added
        with open(f"{main_path}\\album_covers.json", encoding="utf8") as data_file:
            album_asset_keys = json.load(data_file)
    except FileNotFoundError:
        print("Could not find album_covers.json. Default images will be used.")
        custom_assets = False


def get_album_art(track_position):
    """
    Dump current playlist into C:\\Users\\username\\Appdata\\Roaming\\Winamp\\Winamp.m3u8. Then read the path of current
    track from the file and find the album name from it. If album has corresponding album name with key in file
    album_covers.json, return the asset key and album name. Otherwise return default asset key and text. Also, this
    function assumes the music directory structure is like artist\\album\\tracks. If the folder structure is something
    else, the album_name variable may not be the album name and you need to check these manually.
    This function is used only if custom_assets is set to True and album_covers.json is found.

    :param track_position: Current track's position in the playlist, starting from 0
    :return: Album asset key and album name. Asset key in api must be exactly same as this key.
    """

    w.dumpList()
    appdata_path = os.getenv("APPDATA")
    # Returns list of paths to every track in playlist which are in format
    # 'path_to_music_directory\\artist\\album\\track'
    tracklist_paths = w.getTrackList(f"{appdata_path}\\Winamp\\Winamp.m3u8")
    # Get the current track's directory path
    track_path = os.path.dirname(tracklist_paths[track_position])
    # Get the tail of the path i.e. the album name
    album_name = os.path.basename(track_path)

    try:
        large_asset_key = album_asset_keys[album_name]
        large_asset_text = album_name
    except KeyError:
        # Could not find asset key for album cover. Use default asset and asset text instead
        large_asset_key = default_large_key
        if default_large_text == "winamp version":
            large_asset_text = f"Winamp v{winamp_version}"
        elif default_large_text == "album name":
            large_asset_text = album_name
        else:
            large_asset_text = default_large_text

    return large_asset_key, large_asset_text


def update_rpc():
    global previous_track
    global cleared
    trackinfo_raw = w.getCurrentTrackName()  # This is in format {tracknum}. {artist} - {track title} - Winamp

    if trackinfo_raw != previous_track:
        previous_track = trackinfo_raw
        trackinfo = trackinfo_raw.split(" - ")[:-1]
        track_pos = w.getCurrentTrack()  # Track position in the playlist
        artist = trackinfo[0].strip(f"{track_pos + 1}. ")
        track_name = " - ".join(trackinfo[1:])
        pos, now = w.getTrackStatus()[1] / 1000, time.time()  # Both are in seconds

        if len(track_name) < 2:
            track_name = f"Track: {track_name}"
        if pos >= 100000:  # Sometimes this is over 4 million if a new track starts
            pos = 0
        start = now - pos

        # If boolean custom_assets is set true, get the asset key and text from album_covers.json
        if custom_assets:
            large_asset_key, large_asset_text = get_album_art(track_pos)
        else:
            large_asset_key = "logo"
            large_asset_text = f"Winamp v{winamp_version}"

        rpc.update(details=track_name, state=f"by {artist}", start=int(start), large_image=large_asset_key,
                   small_image=small_asset_key, large_text=large_asset_text, small_text=small_asset_text)
        cleared = False


while True:
    status = w.getPlayingStatus()
    if status == "paused" or status == "stopped" and not cleared:
        rpc.clear()
        previous_track = ""
        cleared = True

    elif status == "playing":
        update_rpc()
    time.sleep(1)
