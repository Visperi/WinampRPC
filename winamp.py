"""
Python 3.6+ Winamp Controller

MIT License

Copyright (c) 2018-2019 Visperi
Copyright (c) 2001-2006 Shalabh Chaturvedi

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

import win32api
import win32gui

# wonder why win32 imports dont define these
WM_COMMAND = 0x0111
WM_USER = 0x400


class Winamp:

    def __init__(self):
        self.winamp_commands = {'prev': 40044,
                                'next': 40048,
                                'play': 40045,
                                'pause': 40046,
                                'stop': 40047,
                                'fadeout': 40157,
                                'forward': 40148,
                                'rewind': 40144,
                                'raisevol': 40058,
                                'lowervol': 40059}

        self.hWinamp = win32gui.FindWindow('Winamp v1.x', None)
        hexVersionNumber = hex(self.usercommand(0))  # Returns Winamp version as 0x50yz for version 5.yz
        self.sVersion = f"{hexVersionNumber[2]}.{hexVersionNumber[4:]}"

    def command(self, sCommand):
        if sCommand in self.winamp_commands:
            return win32api.SendMessage(self.hWinamp, WM_COMMAND, self.winamp_commands[sCommand], 0)
        else:
            print("NoSuchWinampCommand")
            exit()

    def __getattr__(self, attr):
        self.command(attr)
        return

    def usercommand(self, id_, data=0):
        return win32api.SendMessage(self.hWinamp, WM_USER, data, id_)

    def FilePath(self):
        return win32api.SendMessage(self.hWinamp, WM_WA_IPC, 0, 3031)

    def getVersion(self):
        """
        :return: the version number of winamp
        """
        return self.sVersion

    def getPlayingStatus(self):
        """
        :return: The current playing status which is 'playing', 'paused' or 'stopped'
        """
        iStatus = self.usercommand(104)
        if iStatus == 1:
            status = "playing"
        elif iStatus == 3:
            status = "paused"
        else:
            status = "stopped"
        return status

    def getTrackStatus(self):
        """
        :return: a tuple (total_length, current_position) where both are in msecs. By default the track length is in
        seconds.
        """
        iTotalLength = self.usercommand(105, 1) * 1000
        iCurrentPos = self.usercommand(105, 0)
        return iTotalLength, iCurrentPos

    def setCurrentTrack(self, iTrackNumber):
        """
        changes the track selection to the number specified
        """
        return self.usercommand(121, iTrackNumber)

    def getCurrentTrack(self):
        """
        :return: The position of currently playing track in the playlist, starting from 0
        """
        return self.usercommand(125)

    def getCurrentTrackName(self):
        """
        :return: Currently playing track name in format that is seen in Winamp's Window text. Usually in format
        '{track number}. {artist} - {track name} - Winamp'
        """
        return win32gui.GetWindowText(self.hWinamp)

    def seekWithinTrack(self, iPositionMsecs):
        """
        seeks within currently playing track to specified milliseconds since start
        """
        return self.usercommand(106, iPositionMsecs)

    def setVolume(self, iVolumeLevel):
        """
        sets the volume to number specified (range is 0 to 255)
        """
        return self.usercommand(122, iVolumeLevel)

    def getNumTracks(self):
        """
        returns number of tracks in current playlist
        """
        return self.usercommand(124)

    def getTrackInfo(self):
        """
        :return: Sample rate, bitrate and number of audio channels of currently playing song
        """
        iSampleRate = self.usercommand(126, 0)
        iBitRate = self.usercommand(126, 1)
        iNumChannels = self.usercommand(126, 2)
        return iSampleRate, iBitRate, iNumChannels

    def dumpList(self):
        """
        dumps the current playlist into WINAMPDIR/winamp.m3u
        WINAMPDIR is by default located in C:/Users/user/AppData/Roaming/Winamp/

        :return: The position of currently playing track in the playlist, starting from 0
        """
        return self.usercommand(120)

    @staticmethod
    def getTrackList(sPlaylistFilepath):
        """
        Open playlist file Winamp.m3u8 which is by default located in C:/Users/user/AppData/Roaming/Winamp/
        Open .m3u8 instead of .m3u because it supports utf-8 and is in plain text anyways. Open file with encoding
        utf-8-sig so the BOM characters \\ufeff are omitted and its easier to parse through the paths.

        :param sPlaylistFilepath: Path to the playlist file Winamp.m3u8
        :return: List of Absolute paths to all tracks in given playlist
        """
        with open(sPlaylistFilepath, "r", encoding="utf-8-sig") as playlist_file:
            lines = playlist_file.readlines()
        playlist = []
        for line in lines:
            if line[0] != "#":
                playlist.append(line[:-1])  # Ignore '\n' at the end of lines
        return playlist
