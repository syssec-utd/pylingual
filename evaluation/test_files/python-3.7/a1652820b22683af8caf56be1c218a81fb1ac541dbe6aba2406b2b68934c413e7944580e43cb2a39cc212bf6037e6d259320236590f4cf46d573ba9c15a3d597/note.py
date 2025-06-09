from __future__ import annotations
from typing import TYPE_CHECKING, AsyncIterator, Optional
from mipac.abc.action import AbstractAction
from mipac.exception import ParameterError
from mipac.http import HTTPClient, Route
from mipac.manager.favorite import FavoriteManager
from mipac.manager.file import MiFile
from mipac.manager.reaction import ReactionManager
from mipac.models.note import Note, NoteReaction
from mipac.models.poll import Poll
from mipac.types.note import ICreatedNote, INote
__all__ = ['NoteActions']
from mipac.util import cache, check_multi_arg, remove_dict_empty
if TYPE_CHECKING:
    from mipac.client import ClientActions

def create_note_body(content: Optional[str]=None, visibility: str='public', visible_user_ids: Optional[list[str]]=None, cw: Optional[str]=None, local_only: bool=False, extract_mentions: bool=True, extract_hashtags: bool=True, extract_emojis: bool=True, reply_id: Optional[str]=None, renote_id: Optional[str]=None, channel_id: Optional[str]=None, files: Optional[list[MiFile]]=None, poll: Optional[Poll]=None):
    file_ids = None
    if files:
        file_ids = [file.file_id for file in files]
    body = {'visibility': visibility, 'visibleUserIds': visible_user_ids, 'text': content, 'cw': cw, 'localOnly': local_only, 'noExtractMentions': not extract_mentions, 'noExtractHashtags': not extract_hashtags, 'noExtractEmojis': not extract_emojis, 'replyId': reply_id, 'renoteId': renote_id, 'channelId': channel_id, 'fileIds': file_ids}
    if not check_multi_arg(content, files, renote_id, poll):
        raise ParameterError('ノートの送信にはcontent, file_ids, renote_id またはpollのいずれか1つが無くてはいけません')
    if poll and type(Poll):
        poll_data = remove_dict_empty({'choices': poll.choices, 'multiple': poll.multiple, 'expiresAt': poll.expires_at, 'expiredAfter': poll.expired_after})
        body['poll'] = poll_data
    return remove_dict_empty(body)

class ClientNoteActions(AbstractAction):

    def __init__(self, note_id: Optional[str]=None, *, session: HTTPClient, client: ClientActions):
        self._note_id: Optional[str] = note_id
        self._session: HTTPClient = session
        self._client: ClientActions = client

    async def add_clips(self, clip_id: str, note_id: Optional[str]=None) -> bool:
        """
        クリップに追加します

        Parameters
        ----------
        note_id : Optional[str], default=None
                追加するノートのID
        clip_id : str
            クリップのID
        note_id : Optional[str], default=None
            追加したいノートのID

        Returns
        -------
        bool
            成功したか否か
        """
        note_id = note_id or self._note_id
        data = {'noteId': note_id, 'clipId': clip_id}
        return bool(await self._session.request(Route('POST', '/api/clips/add-note'), json=data, auth=True))

    async def delete(self, note_id: Optional[str]=None) -> bool:
        """
        ノートを削除します

        Parameters
        ----------
        note_id : Optional[str], default=None
            削除したいノートのID

        Returns
        -------
        bool
            削除に成功したか否か
        """
        note_id = note_id or self._note_id
        data = {'noteId': note_id}
        res = await self._session.request(Route('POST', '/api/notes/delete'), json=data, auth=True)
        return bool(res)

    async def create_renote(self, note_id: Optional[str]=None) -> Note:
        """
        リノートを作成します

        Parameters
        ----------
        note_id : Optional[str], default=None
            ノートのID

        Returns
        -------
        Note
            作成したリノート
        """
        body = create_note_body(renote_id=note_id)
        res: ICreatedNote = await self._session.request(Route('POST', '/api/notes/create'), json=body, auth=True, lower=True)
        return Note(res['created_note'], client=self._client)

    async def get_reaction(self, reaction: str, note_id: Optional[str]=None) -> list[NoteReaction]:
        note_id = note_id or self._note_id
        return await ReactionManager(note_id=note_id, client=self._client, session=self._session).get_reaction(reaction)

    async def reply(self, content: Optional[str]=None, visibility: str='public', visible_user_ids: Optional[list[str]]=None, cw: Optional[str]=None, local_only: bool=False, extract_mentions: bool=True, extract_hashtags: bool=True, extract_emojis: bool=True, file_ids: Optional[list[str]]=None, poll: Optional[Poll]=None, reply_id: Optional[str]=None) -> Note:
        reply_id = reply_id or self._note_id
        body = create_note_body(content=content, cw=cw, visibility=visibility, visible_user_ids=visible_user_ids, extract_emojis=extract_emojis, extract_hashtags=extract_mentions, extract_mentions=extract_mentions, poll=poll, local_only=local_only, reply_id=reply_id)
        print(body)
        res: ICreatedNote = await self._session.request(Route('POST', '/api/notes/create'), json=body, lower=True, auth=True)
        return Note(res['created_note'], client=self._client)

    async def create_quote(self, content: Optional[str]=None, visibility: str='public', visible_user_ids: Optional[list[str]]=None, cw: Optional[str]=None, local_only: bool=False, extract_mentions: bool=True, extract_hashtags: bool=True, extract_emojis: bool=True, file_ids: Optional[list[str]]=None, poll: Optional[Poll]=None, note_id: Optional[str]=None) -> Note:
        """
        Create a note quote.

        Parameters
        ----------
        content: Optional[str], default=None
            text
        visibility: str, default='public'
            Disclosure range
        visible_user_ids: Optional[list[str]], default=None
            List of users to be published
        cw: Optional[str], default=None
            Text to be displayed when warning is given
        local_only: bool, default=False
            Whether to show only locally or not
        extract_mentions: bool, default=True
            Whether to expand the mention
        extract_hashtags: bool, default=True
            Whether to expand the hashtag
        extract_emojis: bool, default=True
            Whether to expand the emojis
        file_ids: Optional[list[str]], default=None
            The ID list of files to be attached
        poll: Optional[Poll], default=None
            Questionnaire to be created
        note_id: Optional[str], default=None
            Note IDs to target for renote and citations
        """
        note_id = note_id or self._note_id
        body = create_note_body(content=content, cw=cw, visibility=visibility, visible_user_ids=visible_user_ids, extract_emojis=extract_emojis, extract_hashtags=extract_mentions, extract_mentions=extract_mentions, poll=poll, local_only=local_only, renote_id=note_id)
        res: ICreatedNote = await self._session.request(Route('POST', '/api/notes/create'), json=body, auth=True, lower=True)
        return Note(res['created_note'], client=self._client)

class NoteActions(ClientNoteActions):

    def __init__(self, note_id: Optional[str]=None, *, session: HTTPClient, client: ClientActions):
        self.favorite = FavoriteManager(note_id=note_id, session=session, client=client)
        self.reaction = ReactionManager(note_id=note_id, session=session, client=client)
        super().__init__(note_id=note_id, session=session, client=client)

    async def send(self, content: Optional[str]=None, visibility: str='public', visible_user_ids: Optional[list[str]]=None, cw: Optional[str]=None, local_only: bool=False, extract_mentions: bool=True, extract_hashtags: bool=True, extract_emojis: bool=True, reply_id: Optional[str]=None, renote_id: Optional[str]=None, channel_id: Optional[str]=None, files: Optional[list[MiFile]]=None, poll: Optional[Poll]=None) -> Note:
        """
        ノートを投稿します。

        Parameters
        ----------
        content : Optional[str], default=None
            投稿する内容
        visibility : str, optional
            公開範囲, by default "public"
            Enum: "public" "home" "followers" "specified"
        visible_user_ids : Optional[list[str]], optional
            公開するユーザー, by default None
        cw : Optional[str], optional
            閲覧注意の文字, by default None
        local_only : bool, optional
            ローカルにのみ表示するか, by default False
        extract_mentions : bool, optional
            メンションを展開するか, by default False
        extract_hashtags : bool, optional
            ハッシュタグを展開するか, by default False
        extract_emojis : bool, optional
            絵文字を展開するか, by default False
        reply_id : Optional[str], optional
            リプライ先のid, by default None
        renote_id : Optional[str], optional
            リノート先のid, by default None
        channel_id : Optional[str], optional
            チャンネルid, by default None
        files : list[MiFile], optional
            添付するファイルのリスト, by default None
        poll : Optional[Poll], optional
            アンケート, by default None

        Returns
        -------
        Note
            投稿したノート

        Raises
        ------
        ContentRequired
            [description]
        """
        body = create_note_body(content=content, cw=cw, channel_id=channel_id, visibility=visibility, visible_user_ids=visible_user_ids, extract_emojis=extract_emojis, extract_hashtags=extract_hashtags, extract_mentions=extract_mentions, files=files, poll=poll, local_only=local_only, renote_id=renote_id, reply_id=reply_id)
        res: ICreatedNote = await self._session.request(Route('POST', '/api/notes/create'), json=body, auth=True, lower=True)
        return Note(res['created_note'], client=self._client)

    @cache(group='get_note')
    async def get(self, note_id: Optional[str]=None) -> Note:
        """
        ノートを取得します

        Parameters
        ----------
        note_id : Optional[str], default=None
            ノートのID

        Returns
        -------
        Note
            取得したノートID
        """
        note_id = note_id or self._note_id
        res = await self._session.request(Route('POST', '/api/notes/show'), json={'noteId': note_id}, auth=True, lower=True)
        return Note(res, client=self._client)

    @cache(group='get_note', override=True)
    async def fetch(self, note_id: Optional[str]=None) -> Note:
        note_id = note_id or self._note_id
        res = await self._session.request(Route('POST', '/api/notes/show'), json={'noteId': note_id}, auth=True, lower=True)
        return Note(res, client=self._client)

    async def get_replies(self, since_id: Optional[str]=None, until_id: Optional[str]=None, limit: int=10, note_id: Optional[str]=None) -> list[Note]:
        """
        ノートに対する返信を取得します

        Parameters
        ---------
        since_id : Optional[str], default=None
            指定すると、その投稿を投稿を起点としてより新しい投稿を取得します
        until_id : Optional[str], default=None
            指定すると、その投稿を投稿を起点としてより古い投稿を取得します
        limit : int, default=10
            取得する上限
        note_id: Optional[str], default=None
            返信を取得したいノートのID

        Returns
        -------
        list[Note]
            返信のリスト
        """
        note_id = note_id or self._note_id
        res = await self._session.request(Route('POST', '/api/notes/replies'), json={'noteId': note_id, 'sinceId': since_id, 'untilId': until_id, 'limit': limit}, auth=True, lower=True)
        return [Note(i, client=self._client) for i in res]

    async def gets(self, local: bool=False, reply: bool=False, renote: bool=False, with_files: bool=False, poll: bool=False, limit: int=100, since_id: str | None=None, until_id: str | None=None, *, all: bool=False) -> AsyncIterator[Note]:
        if limit > 100:
            raise ParameterError('limit は100以下である必要があります')

        async def request(body) -> list[Note]:
            res: list[INote] = await self._session.request(Route('POST', '/api/notes'), lower=True, auth=True, json=body)
            return [Note(note, client=self._client) for note in res]
        body = remove_dict_empty({'local': local, 'reply': reply, 'renote': renote, 'withFiles': with_files, 'poll': poll, 'limit': limit, 'sinceId': since_id, 'untilId': until_id})
        if all is True:
            body['limit'] = 100
        first_req = await request(body)
        for note in first_req:
            yield note
        if all is True and len(first_req) == 100:
            body['untilId'] = first_req[-1].id
            while True:
                res = await request(body)
                if len(res) <= 100:
                    for note in res:
                        yield note
                if len(res) == 0:
                    break
                body['untilId'] = res[-1].id