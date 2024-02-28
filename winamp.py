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

from typing import Tuple

import win32api
import win32gui

# Wonder why win32 imports don't define these
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
        hexVersionNumber = hex(self.send_user_command(0))  # Returns Winamp version as 0x50yz for version 5.yz
        self.version = f"{hexVersionNumber[2]}.{hexVersionNumber[4:]}"

    def send_command(self, command):
        if command in self.winamp_commands:
            return win32api.SendMessage(self.hWinamp, WM_COMMAND, self.winamp_commands[command], 0)
        else:
            print("NoSuchWinampCommand")
            exit()

    def __getattr__(self, attr):
        self.send_command(attr)

    def send_user_command(self, id_: int, data: int = 0):
        return win32api.SendMessage(self.hWinamp, WM_USER, data, id_)

    def get_filepath(self):
        return self.send_user_command(0, 3031)

    def get_version(self):
        """
        Get Winamp version.

        :return: Winamp version number
        """

        return self.version

    def get_playing_status(self) -> str:
        """
        Get current playing status.

        :return: The current playing status which is 'playing', 'paused' or 'stopped'
        """

        status = self.send_user_command(104)

        if status == 1:
            playing_status = "playing"
        elif status == 3:
            playing_status = "paused"
        else:
            playing_status = "stopped"

        return playing_status

    def get_track_status(self) -> Tuple[int, int]:
        """
        Get the current track status.

        :return: A tuple (total_length, current_position) where both are in milliseconds.
        """

        track_length = self.send_user_command(105, 1) * 1000
        track_position = self.send_user_command(105, 0)

        return track_length, track_position

    def change_track(self, track_number: int):
        """
        Change the track to specific track number.

        :param: Track number in the playlist, starting from 0.
        """

        return self.send_user_command(121, track_number)

    def get_track_position(self):
        """
        Get current track position in the playlist.

        :return: The currently selected track position in the playlist, starting from 0.
        """

        return self.send_user_command(125)

    def get_current_track_title(self):
        """
        Get the current track title.

        :return: Currently playing track title in format that is seen in Winamp's Window text. Usually in format
        '{track number}. {artist} - {track name} - Winamp'
        """

        return win32gui.GetWindowText(self.hWinamp)

    def seek_track(self, position: int):
        """
        Seek current track position to position.

        :param position: Seek position in milliseconds.
        """

        return self.send_user_command(106, position)

    def set_volume(self, volume_level: int):
        """
        Set the playback volume.

        :param volume_level: Volume level in range from 0 to 255.
        """

        return self.send_user_command(122, volume_level)

    def get_playlist_length(self):
        """
        Get the number of tracks in current playlist.

        :return: Number of tracks
        """

        return self.send_user_command(124)

    def get_track_info(self) -> Tuple[int, int, int]:
        """
        Get the currently selected track technical information.

        :return: Sample rate, bitrate and number of audio channels of currently playing track.
        """

        sample_rate = self.send_user_command(126, 0)
        bitrate = self.send_user_command(126, 1)
        num_channels = self.send_user_command(126, 2)

        return sample_rate, bitrate, num_channels

    def dump_playlist(self) -> int:
        """
        Dump the current playlist into file WINAMPDIR/winamp.m3u. WINAMPDIR is by default located in
        C:/Users/user/AppData/Roaming/Winamp/.

        :return: The position of currently playing track in the playlist, starting from 0
        """

        return self.send_user_command(120)

    @staticmethod
    def get_playlist(playlist_filepath):
        """
        Get paths to tracks in a playlist. A playlist dump is required for this method except if a playlist file in
        specific location is desired.

        This method opens a playlist file in given path and decodes its contents into a list of track paths.
        The default location for playlist files is C:/Users/user/AppData/Roaming/Winamp/. For UTF-8 support, playlist
        file with extension .m3u8 should be used instead of .m3u.

        :param playlist_filepath: Path to the playlist file
        :return: List of absolute paths to all tracks in given playlist
        """

        # The playlist file is encoded in utf-8-sig and has redundant BOM characters
        with open(playlist_filepath, "r", encoding="utf-8-sig") as playlist_file:
            lines = playlist_file.read().splitlines()

        return [line for line in lines if line and not line.startswith("#")]  # Exclude comments and empty lines
