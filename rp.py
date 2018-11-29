"""
MIT License

Copyright (c) 2018 Visperi

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

client_id = '507484022675603456'
rpc = Presence(client_id)
rpc.connect()
w = winamp.Winamp()

previous_track = ""
cleared = False


def update_rpc():
    global previous_track
    global cleared
    trackinfo_raw = w.getCurrentTrackName()

    if trackinfo_raw != previous_track:
        winampver = w.getVersion()
        previous_track = trackinfo_raw
        trackinfo, tracknum = trackinfo_raw.split(" - "), w.getCurrentTrack() + 1
        artist = trackinfo[0].strip(f"{tracknum}. ")
        trackname = trackinfo[1]
        pos, now = w.getTrackStatus()[1] / 1000, time.time()  # [s]
        if len(trackname) < 2:
            trackname = f"Track: {trackname}"
        if pos >= 100000:  # Sometimes this is over 4 million if a new track starts
            pos = 0
        start = now - pos
        rpc.update(details=trackname, state=f"by {artist}", start=int(start), large_image="logo",
                   small_image="playbutton", large_text=f"Winamp v{winampver}", small_text="Playing")
        cleared = False


while True:
    status = w.getPlayingStatus()
    if status == "paused" or status == "stopped" and not cleared:
        rpc.clear()
        previous_track = ""
        cleared = True

    else:
        if status == "playing":
            update_rpc()
        time.sleep(1)
