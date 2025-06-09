import justpy as jp

class ButtonCounter(jp.Button):

    def __init__(self, **kwargs):
        self.count = 0
        super().__init__(**kwargs)
        self.on('click', self.button_clicked)

    def button_clicked(self, msg):
        self.count += 1

    def react1(self, data):
        self.text = f'You clicked me {self.count} times.'

async def button_counter_demo_c():
    wp = jp.WebPage(tailwind=False)
    for i in range(5):
        ButtonCounter(a=wp, count=i, style='margin: 10px')
    return wp
from examples.basedemo import Demo
Demo('button_counter_demo_c', button_counter_demo_c)