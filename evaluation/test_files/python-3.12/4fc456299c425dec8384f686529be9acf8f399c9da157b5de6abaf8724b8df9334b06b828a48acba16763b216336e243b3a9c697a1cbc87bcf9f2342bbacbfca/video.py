"""This module contains an object that represents a Telegram Video."""
from typing import Optional
from telegram._files._basethumbedmedium import _BaseThumbedMedium
from telegram._files.photosize import PhotoSize
from telegram._utils.types import JSONDict

class Video(_BaseThumbedMedium):
    """This object represents a video file.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`file_unique_id` is equal.

    Args:
        file_id (:obj:`str`): Identifier for this file, which can be used to download
            or reuse the file.
        file_unique_id (:obj:`str`): Unique identifier for this file, which
            is supposed to be the same over time and for different bots.
            Can't be used to download or reuse the file.
        width (:obj:`int`): Video width as defined by sender.
        height (:obj:`int`): Video height as defined by sender.
        duration (:obj:`int`): Duration of the video in seconds as defined by sender.
        thumb (:class:`telegram.PhotoSize`, optional): Video thumbnail.

            .. deprecated:: 20.2
               |thumbargumentdeprecation| :paramref:`thumbnail`.
        file_name (:obj:`str`, optional): Original filename as defined by sender.
        mime_type (:obj:`str`, optional): MIME type of a file as defined by sender.
        file_size (:obj:`int`, optional): File size in bytes.
        thumbnail (:class:`telegram.PhotoSize`, optional): Video thumbnail.

            .. versionadded:: 20.2

    Attributes:
        file_id (:obj:`str`): Identifier for this file, which can be used to download
            or reuse the file.
        file_unique_id (:obj:`str`): Unique identifier for this file, which
            is supposed to be the same over time and for different bots.
            Can't be used to download or reuse the file.
        width (:obj:`int`): Video width as defined by sender.
        height (:obj:`int`): Video height as defined by sender.
        duration (:obj:`int`): Duration of the video in seconds as defined by sender.
        file_name (:obj:`str`): Optional. Original filename as defined by sender.
        mime_type (:obj:`str`): Optional. MIME type of a file as defined by sender.
        file_size (:obj:`int`): Optional. File size in bytes.
        thumbnail (:class:`telegram.PhotoSize`): Optional. Video thumbnail.

            .. versionadded:: 20.2
    """
    __slots__ = ('duration', 'file_name', 'height', 'mime_type', 'width')

    def __init__(self, file_id: str, file_unique_id: str, width: int, height: int, duration: int, thumb: PhotoSize=None, mime_type: str=None, file_size: int=None, file_name: str=None, thumbnail: PhotoSize=None, *, api_kwargs: JSONDict=None):
        super().__init__(file_id=file_id, file_unique_id=file_unique_id, file_size=file_size, thumb=thumb, thumbnail=thumbnail, api_kwargs=api_kwargs)
        with self._unfrozen():
            self.width: int = width
            self.height: int = height
            self.duration: int = duration
            self.mime_type: Optional[str] = mime_type
            self.file_name: Optional[str] = file_name