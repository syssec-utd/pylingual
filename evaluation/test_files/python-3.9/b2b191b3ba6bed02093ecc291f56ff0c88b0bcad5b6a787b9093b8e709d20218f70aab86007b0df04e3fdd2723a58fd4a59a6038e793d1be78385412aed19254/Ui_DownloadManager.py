from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_DownloadManager(object):

    def setupUi(self, DownloadManager):
        DownloadManager.setObjectName('DownloadManager')
        DownloadManager.resize(600, 400)
        DownloadManager.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(DownloadManager)
        self.gridLayout.setObjectName('gridLayout')
        self.downloadsView = EricTableView(DownloadManager)
        self.downloadsView.setObjectName('downloadsView')
        self.gridLayout.addWidget(self.downloadsView, 0, 0, 1, 3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        self.cleanupButton = QtWidgets.QPushButton(DownloadManager)
        self.cleanupButton.setEnabled(False)
        self.cleanupButton.setAutoDefault(False)
        self.cleanupButton.setObjectName('cleanupButton')
        self.horizontalLayout_2.addWidget(self.cleanupButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.infoLabel = QtWidgets.QLabel(DownloadManager)
        self.infoLabel.setText('')
        self.infoLabel.setObjectName('infoLabel')
        self.gridLayout.addWidget(self.infoLabel, 1, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName('horizontalLayout')
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(DownloadManager)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setObjectName('buttonBox')
        self.horizontalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 2, 1, 1)
        self.retranslateUi(DownloadManager)
        self.buttonBox.rejected.connect(DownloadManager.close)
        QtCore.QMetaObject.connectSlotsByName(DownloadManager)
        DownloadManager.setTabOrder(self.downloadsView, self.cleanupButton)
        DownloadManager.setTabOrder(self.cleanupButton, self.buttonBox)

    def retranslateUi(self, DownloadManager):
        _translate = QtCore.QCoreApplication.translate
        DownloadManager.setWindowTitle(_translate('DownloadManager', 'Download Manager'))
        self.cleanupButton.setToolTip(_translate('DownloadManager', 'Press to clean up the list of downloads'))
        self.cleanupButton.setText(_translate('DownloadManager', 'Clear List'))
from eric7.EricWidgets.EricTableView import EricTableView