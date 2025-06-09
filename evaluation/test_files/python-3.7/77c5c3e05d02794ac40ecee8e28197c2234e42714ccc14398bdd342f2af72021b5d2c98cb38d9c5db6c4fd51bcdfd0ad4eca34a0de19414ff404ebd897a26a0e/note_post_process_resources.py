import logging
from enex2notion.enex_types import EvernoteNote
from enex2notion.notion_blocks.uploadable import NotionUploadableBlock
logger = logging.getLogger(__name__)

def resolve_resources(note_blocks, note: EvernoteNote):
    for block in note_blocks.copy():
        if isinstance(block, NotionUploadableBlock) and block.resource is None:
            block.resource = note.resource_by_md5(block.md5_hash)
            if block.resource is None:
                logger.debug(f"Failed to resolve resource in '{note.title}'")
                note_blocks.remove(block)
        if block.children:
            resolve_resources(block.children, note)

def remove_banned_files(note_blocks, note: EvernoteNote):
    for block in note_blocks.copy():
        if isinstance(block, NotionUploadableBlock):
            if _is_banned_extension(block.resource.file_name):
                logger.warning("Cannot upload '{0}' from '{1}', this file extensions is banned by Notion".format(block.resource.file_name, note.title))
                note_blocks.remove(block)
        if block.children:
            remove_banned_files(block.children, note)

def _is_banned_extension(filename):
    file_ext = filename.split('.')[-1]
    return file_ext in {'exe', 'com', 'js', 'jar'}