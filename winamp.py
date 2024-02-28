"""
MIT License

Copyright (c) 2024 Visperi
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

from enum import Enum
from typing import (
    Tuple,
    Union,
    Optional,
    List
)

import win32api
import win32gui

WM_COMMAND = 0x0111
WM_USER = 0x400


class WinampCommand(Enum):
    """
    Enum representing WM_COMMAND commands with correct data values. These commands are identical to pressing a
    button in the player GUI.
    """

    ToggleRepeat = 40022
    """
    Toggle track repeating.
    """
    ToggleShuffle = 40023
    """
    Toggle track shuffling.
    """
    PreviousTrack = 40044
    """
    Go to previous track.
    """
    Play = 40045
    """
    Play current track or start it over if already playing.
    """
    TogglePause = 40046
    """
    Toggle pause.
    """
    Stop = 40047
    """
    Stop the current track. Seeks the track position to zero position.
    """
    NextTrack = 40048
    """
    Go to next track.
    """
    RaiseVolume = 40058
    """
    Raise volume by 1%.
    """
    LowerVolume = 40059
    """
    Lower volume by 1%.
    """
    FastRewind = 40144
    """
    Rewind the current track by 5 seconds.
    """
    FadeOutAndStop = 40147
    """
    Fade out and stop after the track.
    """
    FastForward = 40148
    """
    Fast forward the current track by 5 seconds.
    """
    StopAfterTrack = 40157
    """
    Stop after the current track.
    """


class UserCommand(Enum):
    """
    Enum representing WM_USER user commands sent to Winamp. These commands are sent to Winamp API and are not strictly
    equal to pressing buttons in player GUI. Setter commands often need a separate value 'data' to have effect.
    """

    WinampVersion = 0
    """
    Current Winamp version in hexadecimal number.
    """
    PlayingStatus = 104
    """
    Current playing status. Returns 1 for playing, 3 for paused and otherwise stopped.
    """
    TrackStatus = 105
    """
    Get current tracks' status. Track position in milliseconds if data is set to 0, or track length in seconds if 
    data is 1. 
    """
    SeekTrack = 106
    """
    Seek current track to position in milliseconds specified in data.
    """
    DumpPlaylist = 120
    """
    Dump current playlist to WINAMPDIR/winamp.m3u and resepective .m3u8 files, and return the current playlist 
    position.
    """
    ChangeTrack = 121
    """
    Set the playlist position to position defined in data.
    """
    SetVolume = 122
    """
    Set the playback volume to value specified in data. The range is between 0 (muted) and 255 (max volume).
    """
    PlaylistLength = 124
    """
    Get the current playlist length in number of tracks.
    """
    PlaylistPosition = 125
    """
    Get the current playlist position in tracks.
    """
    TrackInfo = 126
    """
    Get technical information about the current track. Data values give following results: 0 for samplerate, 1 for 
    bitrate and 2 for number of channels.
    """


class PlayingStatus(Enum):
    """
    Enum representing the current playing status of Winamp player.
    """

    Stopped = 0
    """
    The player is stopped or not running. Although this enum value has zero value, the status in Winamp is 'otherwise' 
    stopped if it does not match playing or paused state.
    """
    Playing = 1
    """
    A track is currently playing. 
    """
    Paused = 3
    """
    Current track is paused.
    """


class Track:
    """
    A class representing a track.
    """

    def __init__(self, title: str, sample_rate: int, bitrate: int, channels: int, length: int):
        self.title = title
        self.sample_rate = sample_rate
        self.bitrate = bitrate
        self.channels = channels
        self.length = length


class CurrentTrack(Track):
    """
    A class representing current track in Winamp.
    """

    def __init__(self,
                 title: str,
                 sample_rate: int,
                 bitrate: int,
                 channels: int,
                 length: int,
                 current_position: int,
                 playlist_position: int
                 ):
        super().__init__(title, sample_rate, bitrate, channels, length)
        self.current_position = current_position
        self.playlist_position = playlist_position


class Winamp:
    """
    a controller class for an open Winamp client.
    """

    def __init__(self):
        """
        Initialize a Winamp controller class. If Winamp client is not open during the initialization, method
        Winamp.connect() must be called afterwards before commands can be sent.
        """

        self.window_id = None
        self._version = None
        self.connect()

    def connect(self):
        """
        Connect to a Winamp client.
        """
        self.window_id = win32gui.FindWindow("Winamp v1.x", None)
        self._version = self.fetch_version()

    def __ensure_connection(self):
        """
        Raise an exception if no Winamp client is connected, otherwise do nothing.
        """
        if self.window_id == 0:
            raise ValueError("No Winamp client connected")

    def send_command(self, command: Union[WinampCommand, int]) -> int:
        """
        Send WM_COMMAND command to Winamp.

        :param command: The command to send.
        :return: Response from Winamp.
        """
        self.__ensure_connection()

        if isinstance(command, WinampCommand):
            command = command.value

        return win32api.SendMessage(self.window_id, WM_COMMAND, command, 0)

    def send_user_command(self, command: Union[UserCommand, int], data: int = 0) -> int:
        """
        Send WM_USER command to Winamp API.

        :param command: The command to send.
        :param data: Data to send with the command. For some commands this value affects the returned information.
        :return: Response from the Winamp API.
        """

        self.__ensure_connection()

        if isinstance(command, UserCommand):
            command = command.value

        return win32api.SendMessage(self.window_id, WM_USER, data, command)

    @property
    def version(self) -> str:
        """
        The Winamp version.
        """
        self.__ensure_connection()

        return self._version

    @property
    def current_track(self) -> Optional[CurrentTrack]:
        """
        Fetch the current track.

        :return: CurrentTrack object that contains properties of the currently playing track, or None if no track is
        currently selected.
        """

        title = self.get_track_title()
        playlist_position = self.get_playlist_position()
        length, position = self.get_track_status()
        sample_rate, bitrate, num_channels = self.get_track_info()

        if not title and length == 0 and sample_rate == 0 and bitrate == 0:
            # No track selected
            return None

        return CurrentTrack(title, sample_rate, bitrate, num_channels, length, position, playlist_position)

    def fetch_version(self) -> str:
        """
        Fetch the Winamp version for currently open instance.

        :return: Winamp version number
        """

        # TODO: This can be improved to separate patch version from minor version
        # The version is formatted as 0x50yz for Winamp version 5.yz etc.
        hex_version = hex(self.send_user_command(UserCommand.WinampVersion))

        return f"{hex_version[2]}.{hex_version[4:]}"

    def get_playing_status(self) -> PlayingStatus:
        """
        Get current playing status.

        :return: The current playing status as PlayingStatus enumeration value.
        """

        status = self.send_user_command(104)

        try:
            return PlayingStatus(status)
        except ValueError:
            return PlayingStatus.Stopped

    def get_track_status(self) -> Tuple[int, int]:
        """
        Get the current track status.

        :return: A tuple (total_length, current_position), both in milliseconds.
        """

        track_position = self.send_user_command(UserCommand.TrackStatus, 0)
        track_length = self.send_user_command(UserCommand.TrackStatus, 1)

        if track_length == -1:
            raise ValueError("No track selected in Winamp")

        return track_length * 1000, track_position

    def change_track(self, track_number: int) -> int:
        """
        Change the track to specific track number. If the track number is negative or bigger than the index of last
        playlist tract index, the first or last track is selected.

        :param: Track number in the playlist, starting from 0.
        """

        return self.send_user_command(UserCommand.ChangeTrack, track_number)

    def get_playlist_position(self):
        """
        Get current track position in the playlist.

        :return: The currently selected track position in the playlist, starting from 0.
        """

        return self.send_user_command(UserCommand.PlaylistPosition)

    def get_track_title(self) -> str:
        """
        Get the current track title.

        :return: Currently playing track title in format that is seen in Winamp's Window text. Usually in format
        '{track number}. {artist} - {track name} - Winamp'
        """
        self.__ensure_connection()

        return win32gui.GetWindowText(self.window_id)

    def seek_track(self, position: int) -> int:
        """
        Seek current track position to position.

        :param position: Seek position in milliseconds.
        """

        return self.send_user_command(UserCommand.SeekTrack, position)

    def set_volume(self, volume_level: int) -> int:
        """
        Set the players' playback volume.

        :param volume_level: Volume level in range from 0 to 255.
        """

        return self.send_user_command(UserCommand.SetVolume, volume_level)

    def get_playlist_length(self) -> int:
        """
        Get the number of tracks in current playlist.

        :return: Number of tracks
        """

        return self.send_user_command(UserCommand.PlaylistLength)

    def get_track_info(self) -> Tuple[int, int, int]:
        """
        Get the currently selected track technical information.

        :return: Sample rate, bitrate and number of audio channels of currently playing track.
        """

        sample_rate = self.send_user_command(UserCommand.TrackInfo, 0)
        bitrate = self.send_user_command(UserCommand.TrackInfo, 1)
        num_channels = self.send_user_command(UserCommand.TrackInfo, 2)

        return sample_rate, bitrate, num_channels

    def dump_playlist(self) -> int:
        """
        Dump the current playlist into file WINAMPDIR/winamp.m3u. WINAMPDIR is by default located in
        C:/Users/user/AppData/Roaming/Winamp/.

        :return: The position of currently playing track in the playlist, starting from 0
        """

        return self.send_user_command(UserCommand.DumpPlaylist)

    @staticmethod
    def get_playlist(playlist_filepath) -> List[str]:
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
