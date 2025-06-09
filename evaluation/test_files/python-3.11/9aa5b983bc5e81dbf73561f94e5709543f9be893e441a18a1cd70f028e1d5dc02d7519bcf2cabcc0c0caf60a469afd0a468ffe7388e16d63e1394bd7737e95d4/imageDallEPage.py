import openai
from qtpy.QtWidgets import QWidget, QPushButton, QComboBox, QPlainTextEdit, QSpinBox, QFormLayout, QTextEdit, QLabel
from qtpy.QtCore import Signal, QThread
from pyqt_openai.notifier import NotifierWidget

class DallEThread(QThread):
    replyGenerated = Signal(str)

    def __init__(self, openai_arg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__openai_arg = openai_arg

    def run(self):
        response = openai.Image.create(**self.__openai_arg)
        for image_data in response['data']:
            image_url = image_data['url']
            self.replyGenerated.emit(image_url)

class ImageDallEPage(QWidget):
    submitDallE = Signal(str)
    notifierWidgetActivated = Signal()

    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__nSpinBox = QSpinBox()
        self.__nSpinBox.setRange(1, 10)
        self.__sizeCmbBox = QComboBox()
        self.__sizeCmbBox.addItems(['256x256', '512x512', '1024x1024'])
        self.__sizeCmbBox.currentTextChanged.connect(self.__sizeChanged)
        self.__promptWidget = QPlainTextEdit()
        self.__submitBtn = QPushButton('Submit')
        self.__submitBtn.clicked.connect(self.__submit)
        lay = QFormLayout()
        lay.addRow('Total', self.__nSpinBox)
        lay.addRow('Size', self.__sizeCmbBox)
        lay.addRow(QLabel('Prompt'))
        lay.addRow(self.__promptWidget)
        lay.addRow(self.__submitBtn)
        self.setLayout(lay)

    def __nChanged(self, v):
        pass

    def __sizeChanged(self, v):
        width, height = v.split('x')

    def __submit(self):
        openai_arg = {'prompt': self.__promptWidget.toPlainText(), 'n': self.__nSpinBox.value(), 'size': self.__sizeCmbBox.currentText()}
        self.__t = DallEThread(openai_arg)
        self.__submitBtn.setEnabled(False)
        self.__t.start()
        self.__t.replyGenerated.connect(self.__afterGenerated)

    def __afterGenerated(self, image_url):
        self.submitDallE.emit(image_url)
        if not self.isVisible():
            self.__notifierWidget = NotifierWidget(informative_text='Response 👌', detailed_text='Click this!')
            self.__notifierWidget.show()
            self.__notifierWidget.doubleClicked.connect(self.notifierWidgetActivated)
        self.__submitBtn.setEnabled(True)