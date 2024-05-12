from typing import List, Optional, List, Union
from actions.action import Action
from entities.generic import *
from entities.music import *
from providers.data_model import DataModel


class Music(Action):
    """
    The Music class contains all the methods of a virtual assistant agent in the music domain.
    This class define a specific API for the music domain and inherits from the markup Action class.
    This class defines an API to:

        * Play music (song, playlist, album, artist, genre, music type)
    """

    @classmethod
    def play_music(
        cls,
        album: Optional[Album] = None,
        artist: Optional[Artist] = None,
        genre: Optional[Genre] = None,
        playlist: Optional[Playlist] = None,
        song: Optional[Song] = None,
        date_time: Optional[DateTime] = None,
        music_type: Optional[MusicType] = None,
    ) -> List[MusicEntity]:
        """
        This class method plays a music: a song, an album, songs by an artists,
        a music genre, a playlist in a specific date and time.
        The given params: album, artist, genre, playlist and song are usually mutually exclusive
        and are not used in conjunction.

        Parameters
        ----------
        album : Album, optional
            The album to play
        artist : Artist, optional
            The artist to play
        genre : Genre, optional
            The genre to play
        playlist : Playlist, optional
            The playlist to play
        date_time : DateTime, optional
            The date and time to play the music
        music_type : MusicType, optional
            The type of music to play (usually anything that does not fit in the other categories)

        Returns
        -------
        List[MusicEntity]
            A list of MusicEntity objects that represent the music to play
        """
        music = MusicEntity(
            album=album,
            artist=artist,
            genre=genre,
            playlist=playlist,
            song=song,
            date_time=date_time,
            music_type=music_type,
        )
        data_model = DataModel()
        data_model.append(music)
        return music
