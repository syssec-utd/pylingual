import codecs
import os
import argparse
'\n    {\n        "2.22.10.73": "LX/4Ne;",\n        "method": [\n            "sec()Ljavax/crypto/SecretKey;",\n            "md()[B"\n        ],\n        "string": ""PkTwKSZqUfAUyR0rPQ8hYJ0wNsQQ3dW1+3SCnyTXIfEAxxS75FwkDf47wNv/c8pP3p0GXKR6OOQmhyERwx74fw1RYSU10I4r1gyBVDbRJ40pidjM41G1I1oN"",\n        "2.22.22.77": "LX/2Fr;"\n    }\n'
extends = ['smali']
blacklist = ['.idea', '.git', 'build', 'assets', 'kotlin', 'lib', 'META-INF', 'original', 'res', 'unknown', 'AndroidManifest.xml', 'apktool.yml', 'smali_classes5', 'smali_classes6', 'smali_classes7']
find_file_list = []
targetStr = 'PkTwKSZqUfAUyR0rPQ8hYJ0wNsQQ3dW1+3SCnyTXIfEAxxS75FwkDf47wNv/c8pP3p0GXKR6OOQmhyERwx74fw1RYSU10I4r1gyBVDbRJ40pidjM41G1I1oN'
code1 = '\n    invoke-static {}, Lcom/gbwhatsapp/yo/yo;->sec()Ljavax/crypto/SecretKey;\n    '
code2 = '\n    invoke-static {}, Lcom/gbwhatsapp/yo/yo;->md()[B\n    '

def find_file(from_dir, targetStr, file_list):
    """
    from_dir:目标目录
    targetStr：指定字符串
    file_list:用于存放查到的目标文件集合
    """
    listdir = os.listdir(from_dir)
    for filename in listdir:
        fpath = str(os.path.join(from_dir, filename))
        if filename not in blacklist:
            if os.path.isdir(fpath):
                find_file(fpath, targetStr, file_list)
            elif os.path.isfile(fpath):
                if fpath.split('.')[-1] in extends:
                    with codecs.open(fpath, mode='r', encoding='utf-8') as rf:
                        data = rf.read()
                        if data.__contains__(targetStr):
                            file_list.append(fpath)

def insert_code(file_list):
    for fpath in file_list:
        enableWrite = False
        with codecs.open(fpath, mode='r', encoding='utf-8') as rf:
            lines = list(map(lambda x: x.replace('\n', ''), rf.readlines()))
            for i in range(0, len(lines)):
                line = str(lines[i]).rstrip()
                if line.endswith('([B[BII)Ljavax/crypto/SecretKey;'):
                    line = str(lines[i + 2])
                    if line.__contains__('move-result'):
                        enableWrite = True
                        targetLine = lines[i + 1]
                        line = targetLine.replace(str(lines[i + 1]), code1)
                        lines[i + 1] = line
                elif line.endswith('(Landroid/content/Context;)[B'):
                    line = str(lines[i + 2])
                    if line.__contains__('move-result'):
                        enableWrite = True
                        targetLine = lines[i + 1]
                        line = targetLine.replace(targetLine, code2)
                        lines[i + 1] = line
        if enableWrite:
            with open(fpath, 'w') as f:
                f.write('\n'.join(lines))
                print('写入' + fpath)

def sign(from_dir):
    find_file(from_dir, targetStr, find_file_list)
    insert_code(find_file_list)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('from_dir')
    args = parser.parse_args()
    sign(args.from_dir)