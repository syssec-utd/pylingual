import justpy as jp

class PasswordWithToggle(jp.QInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'password'
        visibility_icon = jp.QIcon(name='visibility_off', classes='cursor-pointer')
        visibility_icon.password_input = self
        self.append_slot = visibility_icon
        visibility_icon.on('click', self.toggle_password)

    @staticmethod
    def toggle_password(self, msg):
        if self.name == 'visibility_off':
            self.name = 'visibility'
            self.password_input.type = 'text'
        else:
            self.name = 'visibility_off'
            self.password_input.type = 'password'

def input_test8(request):
    wp = jp.QuasarPage(data={'text': ''})
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)
    for i in range(1, 6):
        PasswordWithToggle(filled=True, type='password', a=c2, hint=f'Password with toggle #{i}')
    return wp
from examples.basedemo import Demo
Demo('input_test8', input_test8)