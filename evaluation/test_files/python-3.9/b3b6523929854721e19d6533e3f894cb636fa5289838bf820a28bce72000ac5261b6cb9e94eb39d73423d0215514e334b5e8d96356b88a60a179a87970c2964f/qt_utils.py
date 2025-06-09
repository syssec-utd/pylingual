from PyQt5.QtCore import QFile, QIODevice, QTextStream

def load_qt_text(text_path: str) -> str:
    try:
        file = QFile(text_path)
        text = ''
        if file.open(QIODevice.ReadOnly | QFile.Text):
            text_stream = QTextStream(file)
            text_stream.setCodec('utf-8')
            text_stream.setAutoDetectUnicode(True)
            text = text_stream.readAll()
            file.close()
        return text
    except:
        return ''