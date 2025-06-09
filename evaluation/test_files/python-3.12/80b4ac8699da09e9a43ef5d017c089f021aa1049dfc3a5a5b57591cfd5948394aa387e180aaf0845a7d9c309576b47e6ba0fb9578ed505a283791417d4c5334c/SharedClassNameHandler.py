import keyword
from javonet.core.generator.handler.AbstractGeneretatorHandler import AbstractGeneratorHandler

class SharedClassNameHandler(AbstractGeneratorHandler):

    def generate_command(self, analyzed_object, parent_command, handlers):
        return analyzed_object

    def generate_code(self, existing_string_builder, common_command, used_object, handlers):
        if keyword.iskeyword(used_object):
            used_object += used_object[-1]
        if '@' in used_object:
            used_object = used_object.replace('@', '')
        if '-' in used_object:
            used_object = used_object.replace('-', '_')
        if used_object[0].isdigit():
            pos = 0
            for i, x in enumerate(used_object):
                if x.isdigit():
                    pos = i
                break
            new_str = used_object[pos:]
            used_object = new_str
        if used_object[0].islower():
            used_object.capitalize()
        if used_object.isidentifier():
            existing_string_builder.append(used_object)
        else:
            raise NameError('SharedMethodNameHandlerError: Given name is not valid: ' + used_object)