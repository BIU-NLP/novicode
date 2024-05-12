from entities.resolvable import Resolvable
from entities.entity import Entity


class Album(Entity, Resolvable):
    """
    The Album class is used to represent an album.
    It inherits from the Entity class and the Resolvable class.
    """

    pass


class Artist(Entity, Resolvable):
    """
    The Artist class is used to represent an artist.
    It inherits from the Entity class and the Resolvable class.
    """

    pass


class Genre(Entity, Resolvable):
    """
    The Genre class is used to represent a music genre.
    It inherits from the Entity class and the Resolvable class.
    """

    pass


class MusicType(Entity, Resolvable):
    """
    The MusicType class is used to represent a music type.
    It inherits from the Entity class and the Resolvable class.
    """

    pass


class MusicEntity(Entity):
    """
    The MusicEntity class is used to represent a music entity.
    This class is returned by the play_music method in the Music action class. It represents the music to play.
    It inherits from the Entity class.
    """

    pass


class Playlist(Entity, Resolvable):
    """
    The Playlist class is used to represent a playlist.
    It inherits from the Entity class and the Resolvable class.
    """

    pass


class Song(Entity, Resolvable):
    """
    The Song class is used to represent a song.
    It inherits from the Entity class and the Resolvable class.
    """

    pass
