import sys
sys.path.append('../')
import ctypes
from ctypes import *

class g160Struct(Structure):
    _fields_ = [('tnlr', c_double), ('nplr', c_double), ('snri', c_double), ('dsn', c_double)]

def cal_g160(cleanFile, inFile, outFile, inOffset, outOffset, maxComNLevel=-48.0, speechPauseLevel=-35.0):
    """
    :param cleanFile: 干净语音文件
    :param inFile:  输入带噪语音文件
    :param outFile:  输出文件
    :param inOffset:  输入文件的样点延迟
    :param outOffset:   输出文件的样点延迟
    :param maxComNLevel:  最大舒适噪声，默认-48dbov
    :param speechPauseLevel:  非语音段最大的电平门限 -35dbov
    :return:
    """
    g160 = g160Struct()
    import platform
    mydll = None
    cur_paltform = platform.platform().split('-')[0]
    if cur_paltform == 'Windows':
        mydll = ctypes.windll.LoadLibrary(sys.prefix + '/g160.dll')
    if cur_paltform == 'macOS':
        mydll = CDLL(sys.prefix + '/g160.dylib')
    cleFile = c_char_p(bytes(cleanFile.encode('utf-8')))
    inputFile = c_char_p(bytes(inFile.encode('utf-8')))
    outputFile = c_char_p(bytes(outFile.encode('utf-8')))
    mydll.Noise_Compute(cleFile, inputFile, outputFile, inOffset, outOffset, c_double(maxComNLevel), c_double(speechPauseLevel), byref(g160))
    return (g160.tnlr, g160.nplr, g160.snri, g160.dsn)
if __name__ == '__main__':
    print(cal_g160('E:\\files\\cle_malePolqaWB.wav', 'E:\\files\\malePolqaWB.wav', 'E:\\files\\test_malePolqaWB.wav', 192, 192))