from math import sqrt
import os.path as osp
import numpy as np
from PyQt5.QtWidgets import QInputDialog
from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets
here = osp.dirname(osp.abspath(__file__))

def newIcon(icon):
    icons_dir = osp.join(here, '../icons')
    return QtGui.QIcon(osp.join(':/', icons_dir, '%s.png' % icon))

def newButton(text, icon=None, slot=None):
    b = QtWidgets.QPushButton(text)
    if icon is not None:
        b.setIcon(newIcon(icon))
    if slot is not None:
        b.clicked.connect(slot)
    return b

def newAction(parent, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, enabled=True, checked=False):
    """Create a new action and assign callbacks, shortcuts, etc."""
    a = QtWidgets.QAction(text, parent)
    if icon is not None:
        a.setIconText(text.replace(' ', '\n'))
        a.setIcon(newIcon(icon))
    if shortcut is not None:
        if isinstance(shortcut, (list, tuple)):
            a.setShortcuts(shortcut)
        else:
            a.setShortcut(shortcut)
    if tip is not None:
        a.setToolTip(tip)
        a.setStatusTip(tip)
    if slot is not None:
        a.triggered.connect(slot)
    if checkable:
        a.setCheckable(True)
    a.setEnabled(enabled)
    a.setChecked(checked)
    return a

def addActions(widget, actions):
    for action in actions:
        if action is None:
            widget.addSeparator()
        elif isinstance(action, QtWidgets.QMenu):
            widget.addMenu(action)
        else:
            widget.addAction(action)

def labelValidator():
    return QtGui.QRegExpValidator(QtCore.QRegExp('^[^ \\t].+'), None)

class struct(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def distance(p):
    return sqrt(p.x() * p.x() + p.y() * p.y())

def distancetoline(point, line):
    (p1, p2) = line
    p1 = np.array([p1.x(), p1.y()])
    p2 = np.array([p2.x(), p2.y()])
    p3 = np.array([point.x(), point.y()])
    if np.dot(p3 - p1, p2 - p1) < 0:
        return np.linalg.norm(p3 - p1)
    if np.dot(p3 - p2, p1 - p2) < 0:
        return np.linalg.norm(p3 - p2)
    if np.linalg.norm(p2 - p1) == 0:
        return 0
    return np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)

def fmtShortcut(text):
    (mod, key) = text.split('+', 1)
    return '<b>%s</b>+<b>%s</b>' % (mod, key)

def __action_func():
    pass

def newCheckableAction(parent, text, slot=None, shortcut=None, icon=None, tip=None, checkable=True, enabled=True, checked=False):
    """ 模仿上面写的一个功能 """
    a = QtWidgets.QAction(text, parent)
    if icon is not None:
        a.setIconText(text.replace(' ', '\n'))
        a.setIcon(newIcon(icon))
    if shortcut is not None:
        if isinstance(shortcut, (list, tuple)):
            a.setShortcuts(shortcut)
        else:
            a.setShortcut(shortcut)
    if tip is not None:
        a.setToolTip(tip)
        a.setStatusTip(tip)
    if slot is None:
        slot = lambda x: a.setChecked(x)
    if slot is not None:
        a.triggered.connect(slot)
    if checkable:
        a.setCheckable(True)
    a.setEnabled(enabled)
    a.setChecked(checked)
    return a

class XlActionFunc:
    """ 跟action有关的函数调用封装 （该类也可以作为基础的check版本使用）

    一般逻辑结构是这样：
        有个可运行功能的函数func，运行时会配置一些需要存储起来的变量值value
        并且功能需要关联action，绑定到menu等菜单中时，可以使用该装饰器

    220423周六19:15，以前写在pyxllib.gui.qt里的，现在发现似乎并不是很有必要、有用的通用组件，就丢到xllabelme存着
    """

    def __init__(self, parent, title, value=None, checked=None, **kwargs):
        self.parent = parent
        self.title = title
        self.value = value
        self.checked = bool(checked)
        self.checkable = checked is not None
        self.action = newAction(self.parent, self.parent.tr(self.title), self.__call__, checkable=self.checkable, checked=self.checked, **kwargs)

    def __call__(self, checked):
        self.checked = checked

class GetMultiLineTextAction(XlActionFunc):
    """ 该类value是直接存储原始的完整文本内容 """

    def __call__(self, checked):
        super().__call__(checked)
        self.value = self.value or ''
        inputs = QInputDialog.getMultiLineText(self.parent, self.title, '编辑文本：', self.value)
        if inputs[1]:
            self.value = inputs[0]

class GetItemsAction(XlActionFunc):
    """ 该类value目前是存储为list类型 """

    def __call__(self, checked):
        super().__call__(checked)
        self.value = self.value or []
        inputs = QInputDialog.getMultiLineText(self.parent, self.title, '编辑多行文本：', '\n'.join(self.value))
        if inputs[1]:
            self.value = inputs[0].splitlines()

class GetJsonAction(XlActionFunc):
    """ 该类value是直接存储原始的完整文本内容 """

    def __call__(self, checked):
        import json
        super().__call__(checked)
        self.value = self.value or ''
        inputs = QInputDialog.getMultiLineText(self.parent, self.title, '编辑json数据：', json.dumps(self.value, indent=2))
        if inputs[1]:
            self.value = json.loads(inputs[0])

def get_root_widget(widget):
    """ 从输入的组件找parent，一直往上检索到根结点
    常用语从一个组件，追溯到起始的QMainWindow，mainwin
    """
    p = widget
    while p.parent():
        p = p.parent()
    return p