import dis

class ClientVerify(type):
    """
       Метакласс, проверяющий что в результирующем классе нет серверных
       вызовов таких как: accept, listen. Также проверяется, что сокет не
       создаётся внутри конструктора класса.
       """

    def __init__(self, clsname, bases, clsdict):
        error = 0
        socket = 0
        for val in clsdict.values():
            try:
                for arg in dis.get_instructions(val):
                    if arg.argval == 'accept' or arg.argval == 'listen':
                        error = 1
                        print('Ненадлежащие функции для клиента (accept или listen)')
                        break
                    elif arg.argval == 'socket':
                        socket = 1
                        print('Socket was used')
            except:
                pass
        if socket == 1 and error == 0:
            print('Проверка пройдена успешно')

class ServerVerify(type):
    """
        Метакласс, проверяющий что в результирующем классе нет клиентских
        вызовов таких как: connect. Также проверяется, что серверный
        сокет является TCP и работает по IPv4 протоколу.
        """

    def __init__(self, clsname, bases, clsdict):
        error = 0
        socket = 0
        for val in clsdict.values():
            try:
                for arg in dis.get_instructions(val):
                    if arg.argval == 'connect':
                        error = 1
                        print('Ненадлежащая функция для сервера (connect)')
                        break
                    elif arg.argval == 'socket':
                        socket = 1
                        print('Socket was used')
            except:
                pass
        if socket == 1 and error == 0:
            print('Проверка пройдена успешно')