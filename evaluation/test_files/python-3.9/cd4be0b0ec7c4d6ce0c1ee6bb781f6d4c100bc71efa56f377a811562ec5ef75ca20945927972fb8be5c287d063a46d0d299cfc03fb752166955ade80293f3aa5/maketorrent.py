from progress.bar import IncrementalBar
from torf import Torrent
from pathlib import Path
import time
from loguru import logger
import os

def make_private_torrent(filepath: str, torrentname: str, tracker='https://announce.leaguehd.com/announce.php'):
    """
    if os.path.isdir(filepath):
        logger.info('检测到路径制种，将先删除掉路径里面所有种子文件(torrent后缀)以及隐藏文件（.开头的文件）...')
        deletetorrent(filepath) 
    deletetorrent(os.path.dirname(torrentname))
    logger.info('即将开始制作种子...')
    """
    torrent_path = Path(torrentname)
    path = Path(filepath)
    piece_size = 4 * 1024 * 1024
    private = True
    created_by = 'Upload Machine'
    source = 'Upload Machine'
    trytime = 0
    filesize = 0
    while filesize == 0:
        trytime = trytime + 1
        if trytime > 10:
            logger.error('制作种子失败')
            return
        if trytime > 1:
            logger.warning('第' + str(trytime - 1) + '次制作种子失败')
        logger.info('正在第' + str(trytime) + '次制作种子:')
        if torrent_path.exists():
            logger.info('已存在种子文件，正在删除' + torrentname)
            try:
                os.remove(torrent_path)
            except Exception as r:
                logger.error('删除种子发生错误: %s' % r)
        if tracker:
            torrent = Torrent(path=str(path.absolute()), trackers=[tracker], piece_size=piece_size, private=private, created_by=created_by, source=source)
        else:
            torrent = Torrent(path=str(path.absolute()), piece_size=piece_size, private=private, created_by=created_by)
        bar = IncrementalBar(message='制种中:', max=torrent.pieces, suffix='%(index)d/%(max)d [%(eta_td)s]')

        def cb(__torrent: Torrent, path: str, hashed_pieces: int, total_pieces: int):
            bar.next()
        torrent.generate(callback=cb, interval=0)
        torrent.write(str(torrent_path))
        bar.finish()
        filesizetime = 0
        while filesize == 0:
            filesizetime = filesizetime + 1
            if filesizetime > 5:
                break
            if os.path.exists(torrentname):
                filesize = os.path.getsize(torrentname)
            else:
                filesize = 0
            if filesize == 0:
                time.sleep(1)
    logger.info('已完成制作种子' + torrentname)
    return