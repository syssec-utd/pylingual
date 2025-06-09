"""

关于命名
~~~~~~~~~~~~~~~
V2{X}Schema 返回的 model 都是 v2 版本的 Model 实例，也就是从 feeluown.library
模块导入进来的 Model 类。

{X}SchemaForV3 的数据来源都是 api uri_v3 接口获取的数据。
"""
import logging
from datetime import datetime
from marshmallow import Schema, post_load, fields, EXCLUDE
from feeluown.library import SongModel, BriefAlbumModel, BriefArtistModel, ModelState, BriefSongModel, VideoModel, AlbumModel, ArtistModel, PlaylistModel, BriefUserModel
from feeluown.media import Quality, MediaType, Media
logger = logging.getLogger(__name__)

class BaseSchema(Schema):
    source = fields.Str(missing='netease')

    class Meta:
        unknown = EXCLUDE
Schema = BaseSchema
Unknown = 'Unknown'

def create_model(model_cls, data, fields_to_cache=None):
    """
    maybe this function should be provided by feeluown

    :param fields_to_cache: list of fields name to be cached
    """
    if fields_to_cache is not None:
        cache_data = {}
        for field in fields_to_cache:
            value = data.pop(field)
            if value is not None:
                cache_data[field] = value
        model = model_cls(**data)
        for field, value in cache_data.items():
            model.cache_set(field, value)
    else:
        model = model_cls(**data)
    return model

class V2MvSchema(Schema):
    identifier = fields.Int(required=True, data_key='id')
    title = fields.Str(required=True, data_key='name')
    cover = fields.Str(required=True)
    brs = fields.Dict(required=True)
    artists = fields.List(fields.Nested('V2BriefArtistSchema'))
    duration = fields.Int(required=True)

    @post_load
    def create_model(self, data, **kwargs):
        brs = data.pop('brs')
        q_media_mapping = {}
        for q, url in brs.items():
            media = Media(url, type_=MediaType.video)
            if q == '1080':
                quality = Quality.Video.fhd
            elif q == '720':
                quality = Quality.Video.hd
            elif q == '480':
                quality = Quality.Video.sd
            elif q == '240':
                quality = Quality.Video.ld
            else:
                logger.warning('There exists another quality:%s mv.', q)
                quality = Quality.Video.sd
            q_media_mapping[quality] = media
        data['q_media_mapping'] = q_media_mapping
        data['identifier'] = 'mv_' + str(data['identifier'])
        return create_model(VideoModel, data, ['q_media_mapping'])

class V2BriefAlbumSchema(Schema):
    identifier = fields.Int(required=True, data_key='id')
    name = fields.Str(required=True, allow_none=True)
    artist = fields.Dict()

    @post_load
    def create_v2_model(self, data, **kwargs):
        if data['name'] is None:
            data['name'] = Unknown
        if 'artist' in data:
            artist = data.pop('artist')
            data['artists_name'] = artist['name']
        return BriefAlbumModel(**data)

class V2BriefArtistSchema(Schema):
    identifier = fields.Int(required=True, data_key='id')
    name = fields.Str(required=True, allow_none=True)

    @post_load
    def create_v2_model(self, data, **kwargs):
        if data['name'] is None:
            data['name'] = Unknown
        return BriefArtistModel(**data)

class V2SongSchema(Schema):
    identifier = fields.Int(required=True, data_key='id')
    title = fields.Str(required=True, data_key='name', allow_none=True)
    duration = fields.Float(required=True)
    album = fields.Nested('V2BriefAlbumSchema')
    artists = fields.List(fields.Nested('V2BriefArtistSchema'))
    mv_id = fields.Int(required=True, data_key='mvid')
    comment_thread_id = fields.Str(data_key='commentThreadId', allow_none=True, missing=None)

    @post_load
    def create_v2_model(self, data, **kwargs):
        if data['title'] is None:
            data['title'] = Unknown
        return create_model(SongModel, data, ['mv_id', 'comment_thread_id'])

class V2SongSchemaForV3(Schema):
    identifier = fields.Int(required=True, data_key='id')
    title = fields.Str(required=True, data_key='name')
    duration = fields.Float(required=True, data_key='dt')
    album = fields.Nested('V2BriefAlbumSchema', data_key='al')
    artists = fields.List(fields.Nested('V2BriefArtistSchema'), data_key='ar')
    mv_id = fields.Int(required=True, data_key='mv')

    @post_load
    def create_v2_model(self, data, **kwargs):
        return create_model(SongModel, data, ['mv_id'])

class V2AlbumSchema(Schema):
    identifier = fields.Int(required=True, data_key='id')
    name = fields.Str(required=True)
    cover = fields.Str(data_key='picUrl', allow_none=True)
    artists = fields.List(fields.Nested('V2BriefArtistSchema'))
    songs = fields.List(fields.Nested('V2SongSchema'), allow_none=True)
    description = fields.Str(missing='')
    released = fields.Int(data_key='publishTime', missing=0)

    @post_load
    def create_v2_model(self, data, **kwargs):
        released = data['released']
        if released:
            released_date = datetime.fromtimestamp(released / 1000)
            released_str = released_date.strftime('%Y-%m-%d')
            data['released'] = released_str
        return AlbumModel(**data)

class V2ArtistSchema(Schema):
    identifier = fields.Int(required=True, data_key='id')
    name = fields.Str()
    pic_url = fields.Str(data_key='picUrl', allow_none=True)
    hot_songs = fields.List(fields.Nested('V2SongSchema'), data_key='songs')
    aliases = fields.List(fields.Str(), missing=[])
    description = fields.Str(missing='')

    @post_load
    def create_v2_model(self, data, **kwargs):
        return ArtistModel(**data)

class NAlbumSchemaV3(Schema):
    identifier = fields.Int(required=True, data_key='id')
    name = fields.Str(required=True, allow_none=True)

    @post_load
    def create_model(self, data, **kwargs):
        album = BriefAlbumModel(**data)
        if album.identifier == 0:
            album.state = ModelState.not_exists
            album.name = ''
        return album

class NeteaseDjradioSchema(Schema):
    identifier = fields.Int(required=True, data_key='id')
    name = fields.Str(required=True)
    desc = fields.Str(required=False)
    cover = fields.Str(required=False, data_key='picUrl')

    @post_load
    def create_model(self, data, **kwargs):
        return NRadioModel(**data)

class NDjradioSchema(Schema):
    main_song = fields.Dict(required=True, data_key='mainSong')
    radio = fields.Dict(required=True, data_key='radio')

    @post_load
    def create_model(self, data, **kwargs):

        def to_duration_ms(duration):
            seconds = duration / 1000
            m, s = (seconds / 60, seconds % 60)
            return '{:02}:{:02}'.format(int(m), int(s))
        song = data.pop('main_song')
        album_name = data.pop('radio')['name']
        artists_name = ','.join([artist['name'] for artist in song['artists']])
        return BriefSongModel(identifier=song['id'], title=song['name'], duration_ms=to_duration_ms(song['duration']), artists_name=artists_name, album_name=album_name, state=ModelState.cant_upgrade, **data)

class NCloudSchema(Schema):
    main_song = fields.Dict(required=True, data_key='simpleSong')
    album_name = fields.Str(required=True, data_key='album')
    artists_name = fields.Str(required=True, data_key='artist')

    @post_load
    def create_model(self, data, **kwargs):

        def to_duration_ms(duration):
            seconds = duration / 1000
            m, s = (seconds / 60, seconds % 60)
            return '{:02}:{:02}'.format(int(m), int(s))
        song = data.pop('main_song')
        return BriefSongModel(identifier=song['id'], title=song['name'], duration_ms=to_duration_ms(song['dt']), state=ModelState.cant_upgrade, **data)

class V2PlaylistCreatorScehma(Schema):
    identifier = fields.Int(required=True, data_key='userId')
    name = fields.Str(required=True, data_key='nickname')

    @post_load
    def create_v2_model(self, data, **kwargs):
        data['identifier'] = str(data['identifier'])
        return BriefUserModel(**data)

class V2PlaylistSchema(Schema):
    identifier = fields.Int(required=True, data_key='id')
    creator = fields.Nested(V2PlaylistCreatorScehma, missing=None)
    name = fields.Str(required=True)
    description = fields.Str(required=True, allow_none=True, data_key='description')
    cover = fields.Url(required=True, data_key='coverImgUrl')

    @post_load
    def create_v2_model(self, data, **kwargs):
        if data.get('description') is None:
            data['description'] = ''
        return PlaylistModel(**data)

class NeteaseUserSchema(Schema):
    identifier = fields.Int(required=True, data_key='id')
    name = fields.Str(required=True)
    playlists = fields.List(fields.Nested(V2PlaylistSchema))
    fav_playlists = fields.List(fields.Nested(V2PlaylistSchema))
    cookies = fields.Dict()

    @post_load
    def create_model(self, data, **kwargs):
        return NUserModel(**data)

class NeteaseSearchSchema(Schema):
    """搜索结果 Schema"""
    songs = fields.List(fields.Nested(V2SongSchema))
    albums = fields.List(fields.Nested(V2BriefAlbumSchema))
    artists = fields.List(fields.Nested(V2BriefArtistSchema))
    playlists = fields.List(fields.Nested(V2PlaylistSchema))

    @post_load
    def create_model(self, data, **kwargs):
        return NSearchModel(**data)
from .models import NUserModel, NSearchModel, NRadioModel