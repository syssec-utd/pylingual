import argparse
import importlib
import inspect
import ast
import nextcloud_talk_bot
from .nextcloud_talk_bot.first_run_setup import FirstRunSetup
from .i18n import _

class FirstSetup:

    @staticmethod
    def start_setup():
        FirstRunSetup.first_run()

class NextcloudCommands:
    """
    A class for printing the docstrings of classes and methods from specified modules.

    :param input_name: The name of the input used to map to a module.
    :param base_url: The base URL of your Nextcloud instance (optional).
    :param username: Your Nextcloud username (optional).
    :param password: Your Nextcloud password (optional).
    :param room_name: The name of the Nextcloud Talk room (optional).
    """

    def __init__(self, input_name):
        self.input_name = input_name
        if input_name:
            self.module_name = self.module_name = self.map_input_to_module(input_name)
            self.load_module()
        else:
            self.module_name = None
        self.bot = nextcloud_talk_bot.NextcloudTalkBot()
        if hasattr(self.bot, 'NEXTCLOUD_URL'):
            self.url = self.bot.NEXTCLOUD_URL
            self.username = self.bot.USERNAME
            self.password = self.bot.PASSWORD
            self.room_name = self.bot.ROOM_NAME
            self.room_token = self.bot.ROOM_TOKEN
        else:
            FirstRunSetup.first_run()

    def map_input_to_module(self, input_name):
        mapping = {'activities': 'nextcloud_activities', 'user': 'nextcloud_user', 'file': 'nextcloud_file_operations', 'meeting': 'nextcloud_meeting', 'messages': 'nextcloud_messages', 'poll': 'nextcloud_poll', 'requests': 'nextcloud_requests', 'extractor': 'nextcloud_talk_extractor', 'talkbot': 'Nextcloudtalkbot'}
        return mapping.get(input_name, input_name)

    def load_module(self):
        module_name = self.module_name
        self.module = importlib.import_module(f'nextcloud_talk_bot.{self.module_name}')

    def get_first_class(self):
        for (name, obj) in inspect.getmembers(self.module):
            if inspect.isclass(obj) and self.module_name in obj.__module__:
                return obj
        return None

    def print_first_class_docstring(self):
        cls = self.get_first_class()
        if cls:
            docstring = inspect.getdoc(cls)
            if docstring:
                print(f'{docstring}\n')
            else:
                print(f'{cls.__name__} has no docstring.')
        else:
            print(f"{_('No classes found in module ')}{self.module_name}.")

    def print_method_docstring(self, method_name):
        cls = self.get_first_class()
        if cls:
            method = getattr(cls, method_name, None)
            if method:
                docstring = inspect.getdoc(method)
                if docstring:
                    print(f'{docstring}\n')
                else:
                    print(f"{_('Function ')}{method_name}{_(' has no docstring.')}")
            else:
                print(f"Method '{method_name}' not found in class '{cls.__name__}'.")
        else:
            print(f"{_('No classes found in module ')}{self.module_name}.")

    def call_class_method(self, method_name, *args, **kwargs):
        unpacked_args = []
        for arg in args:
            if arg.startswith('[') and arg.endswith(']'):
                parsed_arg = ast.literal_eval(arg)
                if isinstance(parsed_arg, list):
                    unpacked_args.append(parsed_arg)
                else:
                    unpacked_args.append(arg)
            else:
                unpacked_args.append(arg)
        cls = self.get_first_class()
        if cls:
            instance = getattr(self.bot, self.input_name)
            method = getattr(instance, method_name, None)
            if method:
                if args:
                    print(*unpacked_args)
                    return method(*unpacked_args)
                else:
                    return method()
            else:
                print(f"{_('Function ')}{method_name}{_(' not found in class ')}{cls.__name__}'.")
        else:
            print(f"{_('No classes found in module ')}{self.module_name}.")

    def print_available_classes_and_methods(self):
        print(f"{_('Classes and methods in module ')}{self.module_name}:\n")
        for (name, obj) in inspect.getmembers(self.module):
            if inspect.isclass(obj) and self.module_name in obj.__module__:
                print(f'Class: {name}')
                for (method_name, method) in inspect.getmembers(obj, predicate=inspect.isfunction):
                    print(f'  - Method: {method_name}')

    def print_method_parameters(self, method_name):
        cls = self.get_first_class()
        if cls:
            method = getattr(cls, method_name, None)
            if method:
                signature = inspect.signature(method)
                print(f"{_('Parameters for function ')}{method_name}':\n{signature}")
            else:
                print(f"{_('Function ')}{method_name}{_(' not found in class ')}{cls.__name__}'.")
        else:
            print(f"{_('No classes found in module ')}{self.module_name}.")

    def print_available_classes(self):
        classes = ['activities', 'user', 'file', 'meeting', 'messages', 'poll', 'extractor']
        print(_('Available options:'))
        for options in classes:
            print(options)
        print(_('type options --list to get available functions'))
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=_('Call Nextcloud Commands via NextcloudTalkBot Framework'), add_help=False)
    parser.add_argument('input_name', help=_('Option name. Type --list to get all options.'), nargs='?', default=None)
    parser.add_argument('--function', '-f', dest='method_name', default=None, help=_('Function to call. Type option --list to get all parameters or option --help for help'))
    parser.add_argument('--args', '-a', nargs='*', default=[], help=_('Arguments to pass to the function.'))
    parser.add_argument('--help', '-h', dest='help_flag', action='store_true', help='Print help.')
    parser.add_argument('--list', '-l', dest='list_flag', action='store_true', help=_('List available options or functions.'))
    parser.add_argument('--setup', '-s', dest='setup_flag', action='store_true', help=_('First Run setup'))
    args = parser.parse_args()
    if args.input_name is not None:
        nextcloud_command = NextcloudCommands(args.input_name)
        if args.help_flag:
            if args.method_name:
                nextcloud_command.print_method_docstring(args.method_name)
            else:
                nextcloud_command.print_first_class_docstring()
        elif args.method_name and args.list_flag:
            nextcloud_command.print_method_parameters(args.method_name)
        elif args.method_name:
            result = nextcloud_command.call_class_method(args.method_name, *args.args)
            if result:
                print(f"{_('Result: ')}{result}")
        elif args.list_flag:
            nextcloud_command.print_available_classes_and_methods()
        else:
            parser.print_help()
    elif args.input_name is None:
        if args.list_flag:
            nextcloud_command = NextcloudCommands(args.input_name)
            nextcloud_command.print_available_classes()
        elif args.setup_flag:
            nextcloud_command = FirstSetup()
            nextcloud_command.start_setup()
        else:
            parser.print_help()