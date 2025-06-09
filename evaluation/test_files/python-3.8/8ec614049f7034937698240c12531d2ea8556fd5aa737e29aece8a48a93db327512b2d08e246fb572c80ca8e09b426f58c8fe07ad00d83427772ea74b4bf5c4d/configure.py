"""Модуль функций работы с конфигурационным файлом"""
from . import __path__ as path
from . import __version__
from yandex_oauth import yao

def load_config():
    """Функция загрузки конфигурационного файла
    
    :returns: config или False, если нет кофигурационного файла
    """
    return yao.load_token(path[0])

def make_config():
    """Функция создания первичного конфигурационного файла"""
    print('\n\nПЕРВОНАЧАЛЬНАЯ КОНФИГУРАЦИЯ ПРИЛОЖЕНИЯ\n')
    print('1. Авторизуйтесь на Яндексе. Укажите логин и пароль администратора организации,\n   от имени которого будут выполняться запросы к API\n')
    print('      https://passport.yandex.ru/')
    print('\n')
    print('2. Зарегистрируйте приложение\n')
    print('      https://oauth.yandex.ru/client/new')
    print('\n   Заполните поля:')
    print('      Название сервиса: ya360')
    print('      Для какой платформы нужно приложение: Веб-сервисы')
    print('      Callback URI: https://oauth.yandex.ru/verification_code')
    print('      Какие данные вам нужны: Яндекс 360 Admin API, Яндекс 360 Directory API (отметить все галочки)')
    print('\n')
    print('3. Перейдите на страницу созданных приложений и выберете ya360\n')
    print('      https://oauth.yandex.ru/')
    print('\n')
    try:
        client_id = input('   Введите ClientID: ')
    except:
        print('\n')
        exit(0)
    try:
        client_secret = input('   Введите Client secret: ')
    except:
        print('\n')
        exit(0)
    try:
        adminemail = input('   Введите e-mail администратора организации, от имени которого будут выполняться запросы к API: ')
    except:
        print('\n')
        exit(0)
    url = 'https://oauth.yandex.ru/authorize?response_type=code&client_id=' + str(client_id) + '&login_hint=' + str(adminemail) + '&force_confirm=yes'
    print('\n4. Перейдите по следующей ссылке и получите код подтверждения\n')
    print('      ' + url)
    print('\n')
    try:
        code = input('   Введите код подтверждения: ')
    except:
        print('\n')
        exit(0)
    token = yao.get_token_by_code(code, client_id, client_secret)
    if 'error' in token and 'error_description' in token:
        print('\nОШИБКА ' + token['error'] + ': ' + token['error_description'] + '\n')
        exit(1)
    print('5. Зайдите в профиль организации\n')
    print('      https://admin.yandex.ru/company-profile\n')
    try:
        orgid = input('    Введите ID организации: ')
    except:
        print('\n')
        exit(0)
    token.update({'orgid': orgid, 'adminemail': adminemail})
    if yao.save_token(path[0], token):
        return True
    else:
        print('\nОшибка создания конфигурационного файла\n')
        exit(1)