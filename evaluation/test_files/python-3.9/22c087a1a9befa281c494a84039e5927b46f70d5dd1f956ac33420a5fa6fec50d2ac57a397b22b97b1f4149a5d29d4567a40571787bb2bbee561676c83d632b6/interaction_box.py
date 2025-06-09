import vmat
from PySide2.QtGui import Qt, QImage, QColor, QPainter

def read_png() -> QImage:
    """读取*.png文件"""
    file_name = vmat.askOpenFile('*.png')
    if file_name is not None:
        image = QImage(file_name)
        if image:
            return image

def LeftButtonPressRelease(**kwargs):
    if kwargs['picked'] is image_box:
        png = read_png()
        if png is not None:
            image_box.draw(png)
    elif kwargs['picked'] is click_box:
        options = ['单击', '再击', '三击']
        options = dict(zip(options, [*options[1:], options[0]]))
        click_box.draw_text(options[click_box.text()])
    elif kwargs['picked'] is value_box:
        global value
        v = vmat.askInt(0, value, 100)
        if v is not None:
            value = vmat.askInt(0, value, 100)
            draw_value()

def NoButtonWheel(**kwargs):
    if kwargs['picked'] is value_box:
        global value
        value = min(max(value + kwargs['delta'], 0), 100)
        draw_value()

def draw_value():
    """自定义绘图"""
    value_box.draw_text(text='滚轮或单击：{}'.format(value))
    (w, h) = (value_draw_box.size()[0] * view.width(), value_draw_box.size()[1] * view.height())
    painter = QPainter()
    image = QImage(w, h, value_draw_box.image().format())
    painter.begin(image)
    painter.fillRect(0, 0, w, h, QColor('white'))
    painter.fillRect(0, 0, value / 100 * w, h, QColor('lightskyblue'))
    painter.end()
    value_draw_box.draw(image)
if __name__ == '__main__':
    png = read_png()
    if png is None:
        vmat.appexit()
    view = vmat.View()
    mesh_prop = vmat.PolyActor(view, color=[1, 1, 0.6])
    mesh_prop.setData(vmat.ccCylinder(5, 20, [0, 0, 0], [0, -1, -1]))
    image_box = vmat.ImageBox(view, image=png, size=[0.2, 0.4], pos=[1, 0.1], anchor=[1, 0], pickable=True)
    image_box.mouse['LeftButton']['PressRelease'] = LeftButtonPressRelease
    text_box = vmat.TextBox(view, text='静态文本' + ' ' * 10, fore_color=QColor('white'), back_color=QColor('crimson'), bold=True, italic=True, underline=True, size=[0.2, 0.04], pos=[0, 0.1], anchor=[0, 0])
    click_box = vmat.TextBox(view, text='单击', text_align=Qt.AlignCenter, size=[0.2, 0.04], pos=[0, 0.14], anchor=[0, 0], pickable=True)
    click_box.mouse['LeftButton']['PressRelease'] = LeftButtonPressRelease
    value = 50
    value_box = vmat.TextBox(view, size=[0.2, 0.04], pos=[0, 0.45], anchor=[0, 0], pickable=True)
    value_box.mouse['LeftButton']['PressRelease'] = LeftButtonPressRelease
    value_box.mouse['NoButton']['Wheel'] = NoButtonWheel
    value_draw_box = vmat.ImageBox(view, size=[0.2, 0.01], pos=[0, 0.49], anchor=[0, 0])
    draw_value()
    view.setCamera_FitAll()
    vmat.appexec(view)
    vmat.appexit()