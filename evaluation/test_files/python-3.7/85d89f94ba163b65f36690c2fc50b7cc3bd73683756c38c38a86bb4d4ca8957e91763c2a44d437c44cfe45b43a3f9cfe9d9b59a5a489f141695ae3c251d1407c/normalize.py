from xdnlp.utils import md5, package_path, read_lines
import os

class Normalize(object):

    def __init__(self):
        self.__character_map = {}
        self.__chinese_map = {}
        self.__pinyin_map = {}
        self.__load_data()

    def normalize(self, query: str) -> str:
        result = ''
        for c in query:
            s = md5(c)
            c = self.__character_map.get(s, c)
            c = self.__chinese_map.get(s, c)
            result += c
        return result

    def pinyin(self, query: str, sep: str=' ') -> str:
        result = []
        for c in query:
            result.append(self.__pinyin_map.get(c, c))
        result = sep.join(result)
        return result

    def pinyin_with_space(self, query: str) -> str:
        result = []
        for c in query:
            result.append(self.__pinyin_map.get(c, c))
        return ' '.join(result)

    def __load_data(self):
        for line in read_lines(os.path.join(package_path, 'data/letter_mapping.txt')):
            temp = line.strip().split('\t')
            if len(temp) == 3:
                if temp[-1] == '0':
                    self.__character_map[temp[0]] = temp[1]
                elif temp[-1] == '1':
                    self.__chinese_map[temp[0]] = temp[1]
        for line in read_lines(os.path.join(package_path, 'data/pinyin.txt')):
            temp = line.strip().split(',')
            if len(temp) >= 2:
                self.__pinyin_map[temp[0]] = temp[1]
if __name__ == '__main__':
    norm = Normalize()
    print(norm.normalize('Nhận Cày Thuê Liên Quân Mobile Uy Tín - Giá Rẻ - Nhanh Chóng\nSdt/Zalo: 0363 099 883 liên hệ để biết thông tin chi tiết.'))