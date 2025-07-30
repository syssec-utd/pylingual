from collections.abc import MutableMapping
from copy import deepcopy
from xdis import iscode
from xdis.cross_types import UnicodeForPython3, LongTypeForPython3

from pylingual.editable_bytecode import Inst
from pylingual.editable_bytecode.utils import comprehension_names, find_loadconst_codeobj_from_makefunc


# added type-sensitivity to the dict to differentiate true/1 and false/0
class TypeSensitiveDict(MutableMapping):
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return self.store[self._key_transform(key)]

    def __setitem__(self, key, value):
        self.store[self._key_transform(key)] = value

    def __delitem__(self, key):
        del self.store[self._key_transform(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __contains__(self, key):
        return self._key_transform(key) in self.store

    def keys(self) -> list:
        return [self._key_restore(key) for key in self.store.keys()]

    def items(self):
        return ((self._key_restore(key), value) for key, value in self.store.items())

    def values(self):
        return self.store.values()

    def _key_transform(self, key):
        if type(key) == UnicodeForPython3:
            return (key.value.decode("utf-8"), str)
        if type(key) == LongTypeForPython3:
            return (key.value, int)
        return (key, type(key))

    def _key_restore(self, key):
        return key[0]


#### Main Masker
class Masker:
    blacklist = [
        "__doc__",
        "__annotations__",
        "__qualname__",
        "__class__",
        "return",  # for return annotations
        True,
        False,
        None,
    ]

    def __init__(self, global_table: TypeSensitiveDict | None = None):
        self.global_tab = global_table if global_table is not None else TypeSensitiveDict()

    def mask(self, tok):
        """Mask a token, must be in the global_table."""
        return self.global_tab[tok] if not any(tok == t and type(tok) == type(t) for t in self.blacklist) else tok

    def unmask(self, value):
        """Unmask a token, value must be a metatoken value in the global_table; or this function will fail loudly"""
        key = list(self.global_tab.keys())[list(self.global_tab.values()).index(value)]
        return key

    def parse_MAKE_FUNCTION_info(self, inst: Inst) -> str:
        """Parses out information about MAKE_FUNCTION, like args and flags
        Used in get_model_view()"""
        if inst.opcode != inst.bytecode.opcode.MAKE_FUNCTION:
            raise ValueError("Inst is not type MAKE_FUNCTION")

        target_inst = find_loadconst_codeobj_from_makefunc(inst)
        if target_inst is None:
            raise ValueError("Could not find target LOAD_CONST codeobj from MAKE_FUNCTION")
        target_co = target_inst.argval

        func_info = []  # list of info fields to use as argval for MAKE_FUNCTION

        flags_make_func = int(inst.argval)
        if bool(flags_make_func & 0b0001):  # b_default_vals
            func_info.append("defaults")
        if bool(flags_make_func & 0b0010):  # b_kwonly_defaults
            func_info.append("kwonly_defaults")
        if bool(flags_make_func & 0b0100):  # b_param_annotations
            if self.future_annotations:
                func_info.append("annotations-FUTURE")
            else:
                func_info.append("annotations")
        if bool(flags_make_func & 0b1000):  # b_free_vars
            func_info.append("closures")

        # flags from the target code object
        flags_co = int(target_co.co_flags)
        if bool(flags_co & 0b10000000):  # coroutine
            func_info.append("coroutine")
        if bool(flags_co & 0b1000000000):  # async_generator
            func_info.append("async_generator")

        posargcount = target_co.co_argcount
        if not hasattr(target_co, "co_posonlyargcount"):
            setattr(target_co, "co_posonlyargcount", 0)
        argcount = posargcount + target_co.co_kwonlyargcount

        # parse args
        if argcount:
            args = [self.mask(inst.bytecode.resolve_namespace(arg)) for arg in target_co.co_varnames[:argcount]]
            end = 0
            if posargcount:
                begin, end = 0, posargcount
                func_info.append(f"args: [{', '.join(args[begin:end])}]")
            if target_co.co_posonlyargcount:
                begin, end = end, end + target_co.co_posonlyargcount
                func_info.append(f"posonly: [{', '.join(args[begin:end])}]")
            if target_co.co_kwonlyargcount:
                begin, end = end, end + target_co.co_kwonlyargcount
                func_info.append(f"kwonly: [{', '.join(args[begin:end])}]")

        # kwargs and varargs
        has_kwargs = bool(flags_co & 0b0100)
        if has_kwargs:
            func_info.append(f"kwarg: [*{self.mask(inst.bytecode.resolve_namespace(target_co.co_varnames[argcount]))}]")
        if bool(flags_co & 0b1000):
            func_info.append(f"vararg: [**{self.mask(inst.bytecode.resolve_namespace(target_co.co_varnames[argcount + int(has_kwargs)]))}]")

        return ", ".join(func_info)

    def get_model_view(self, inst: Inst) -> str:
        """Get a dissassembled view of the instruction as the model will view it
        - Replaces literals, varnames, consts etc with a mask defined in the global_table arg.
            Will recursively replace items in list-like objects as well
        - Brings necessary information for function definitions up from the child code obj
        - Simplifies jump args
        - Removes Offset notation except for jump_targets

        :param inst: Instruction we are trying to view

        """
        view = ""

        if inst.opcode == inst.bytecode.opcode.MAKE_FUNCTION:
            # bring up necessary information from child bytecode for function def creation
            view = f"{inst.opname} , {inst.arg}"
            # parse for load const with our target bytecode
            func_info = self.parse_MAKE_FUNCTION_info(inst)
            if func_info:
                view += f" ({func_info})"

        elif inst.optype in ("nargs", "vargs", "compare"):
            view = f"{inst.opname} , {inst.argrepr if inst.argrepr else inst.argval}"

        elif inst.optype == "name":
            view = f"{inst.opname} , {self.mask(inst.bytecode.resolve_namespace(inst.argval))}"
            # additional import context to differ some import syntax
            if inst.opname == "IMPORT_NAME" and "." in inst.argval:
                view += "-DOT"
            elif inst.opname == "LOAD_NAME" and inst.argval == "__annotations__" and self.future_annotations:
                view += "-FUTURE"

        elif inst.optype in ("const", "local"):
            if iscode(inst.argval):
                if inst.argval.co_name in comprehension_names:
                    view = f"{inst.opname} , <codeobj:{inst.argval.co_name}>"
                else:
                    view = f"{inst.opname} , <codeobj:{self.mask(inst.bytecode.resolve_namespace(inst.argval.co_name))}>"

            elif isinstance(inst.argval, str) and inst.argval in self.global_tab:  # have to do this check incase string is varname of type annotation
                view = f"{inst.opname} , {repr(self.mask(inst.argval))}"

            elif type(inst.argval) in (list, tuple, frozenset, set):
                # do recursive in-place replacement of list elems if they are strs or bytestrs

                def replace_list(consts):
                    """recursive replacement of elements in arbitrary list-like objects"""
                    for idx, const in enumerate(consts):
                        if isinstance(const, str):
                            consts[idx] = repr(self.mask(inst.bytecode.resolve_namespace(const)))
                        elif const is None:
                            continue  # don't mask None
                        elif type(const) in (list, tuple, frozenset):
                            consts[idx] = type(const)(replace_list(list(const)))
                        else:
                            consts[idx] = self.mask(const)
                    return consts

                consts = list(deepcopy(inst.argval))
                consts = replace_list(consts)

                if inst.bytecode.version < (3, 11):
                    # Format keyword argument list
                    # We left pad the list of kwargs so the model doesnt have to "look ahead"
                    next_insts = inst.next_instructions
                    next_inst = next_insts[0] if next_insts != [] else None
                    if next_inst is not None and inst.opname == "LOAD_CONST" and next_inst.opname == "CALL_FUNCTION_KW":
                        consts = ["<KWARG_PAD>"] * (next_inst.argval - len(consts)) + consts

                # cast back to original type and print repr
                # demote quotes one layer
                arg_repr = repr(type(inst.argval)(consts)).replace("'", "").replace('"', "'")
                view = f"{inst.opname} , {arg_repr}"
            else:
                view = f"{inst.opname} , {self.mask(inst.bytecode.resolve_namespace(inst.argval))}"

        # inst has other arg type, format
        elif inst.has_arg:
            # check for jump to use simplified jump format
            if inst.is_jump:
                jump_direction_indicator = "v~>" if inst.target.offset > inst.offset else "^~>"
                view = f"{inst.opname} {inst.argrepr} {jump_direction_indicator}"
            elif inst.optype is None or inst.optype == "??" or inst.optype == "encoded_arg":
                # don't mask IS_OP args
                view = f"{inst.opname} , {inst.argrepr if inst.argrepr else inst.argval}"
            else:
                if inst.argval in self.global_tab:
                    view = f"{inst.opname} , {self.mask(inst.argval)}"
                else:
                    view = f"{inst.opname} , {inst.argrepr}"
        # inst sets up annotations and __future__ annotations imported
        elif inst.opname == "SETUP_ANNOTATIONS" and self.future_annotations:
            view = "SETUP_ANNOTATIONS-FUTURE"
        # no arg case
        else:
            view = f"{inst.opname}"

        # add offset if inst is a jump target
        if inst.is_jump_target:
            view = f"{inst.offset} {view}"
            # create list of offsets greater than or less than inst, for all jump origins to this inst
            jumps_greater_or_less = [i.offset < inst.offset for i in inst.jumped_to_from_insts]
            if any(jumps_greater_or_less):  # 1 in list
                view = f"^~> {view}"
            if not all(jumps_greater_or_less):  # 0 in list
                view = f"v~> {view}"

        # Add exception table information
        if inst.bytecode.named_exception_table is not None:
            if inst.exception_target:
                view = f"E-> {view}"
            if inst.exception_end:
                view = f"{view} E-END"

            # check if next instruction is the start of entry in exception_table
            next_inst = None
            for inst in inst.next_instructions:
                if inst.opname not in ("CACHE", "PRECALL"):
                    next_inst = inst
                    break

            if next_inst is not None and next_inst.exception_start:
                view = f"{view} E-> {next_inst.exception_start}"

        return view
