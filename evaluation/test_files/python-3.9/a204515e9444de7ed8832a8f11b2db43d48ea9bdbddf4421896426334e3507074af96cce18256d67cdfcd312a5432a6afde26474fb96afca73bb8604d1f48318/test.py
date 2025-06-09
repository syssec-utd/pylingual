from ._encrypt256 import Encrypt
from random import randbytes
from os.path import abspath
from pathlib import Path as libpath

def test(__file__):
    plaTextList = ['黄', '黄河之水天上来' * 100, '黄河之水天上来' * 1000, '黄河之水天上来' * 10000, randbytes(1), randbytes(100), randbytes(1000), randbytes(10000)]
    passwordList = ['床', '床前明月光' * 100, '床前明月光' * 1000, '床前明月光' * 10000, randbytes(1), randbytes(100), randbytes(1000), randbytes(10000), 6, 71395003615, 323167948471395003615, 3546013789103174987223167948471395003615]
    checkSizeList = [0, 50, 100, 150, 200, 255]
    for plaText in plaTextList:
        for password in passwordList:
            for checkSize in checkSizeList:
                cipText = Encrypt(password=password).encrypt(text=plaText, checkSize=checkSize)
                NewPlaText = Encrypt(password=password).decrypt(text=cipText)
                assert plaText != cipText
                assert plaText == NewPlaText
    baseDir = abspath(libpath(__file__).parent)
    plaFile = f'{baseDir}/plaFile.temp'
    cipFile = f'{baseDir}/cipFile.temp'
    NewPlaFile = f'{baseDir}/NewPlaFile.temp'
    plaTextList = [randbytes(1), randbytes(100), randbytes(1000), randbytes(10000)]
    passwordList = ['床', '床前明月光' * 100, '床前明月光' * 1000, '床前明月光' * 10000, randbytes(1), randbytes(100), randbytes(1000), randbytes(10000), 6, 71395003615, 323167948471395003615, 3546013789103174987223167948471395003615]
    checkSizeList = [0, 50, 100, 150, 200, 255]
    for plaText in plaTextList:
        for password in passwordList:
            for checkSize in checkSizeList:
                libpath(plaFile).write_bytes(plaText)
                Encrypt(password=password).encryptFile(fpath=plaFile, outpath=cipFile, checkSize=checkSize)
                Encrypt(password=password).decryptFile(fpath=cipFile, outpath=NewPlaFile)
                assert plaText != libpath(cipFile).read_bytes()
                assert plaText == libpath(NewPlaFile).read_bytes()
    libpath(plaFile).unlink(missing_ok=True)
    libpath(cipFile).unlink(missing_ok=True)
    libpath(NewPlaFile).unlink(missing_ok=True)
    print('测试通过')