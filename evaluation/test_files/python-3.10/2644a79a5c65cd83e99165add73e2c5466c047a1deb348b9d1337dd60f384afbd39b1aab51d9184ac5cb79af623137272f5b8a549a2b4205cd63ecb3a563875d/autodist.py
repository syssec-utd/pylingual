"""This module implements additional tests ala autoconf which can be useful.

"""
import textwrap

def check_inline(cmd):
    """Return the inline identifier (may be empty)."""
    cmd._check_compiler()
    body = textwrap.dedent('\n        #ifndef __cplusplus\n        static %(inline)s int static_func (void)\n        {\n            return 0;\n        }\n        %(inline)s int nostatic_func (void)\n        {\n            return 0;\n        }\n        #endif')
    for kw in ['inline', '__inline__', '__inline']:
        st = cmd.try_compile(body % {'inline': kw}, None, None)
        if st:
            return kw
    return ''

def check_restrict(cmd):
    """Return the restrict identifier (may be empty)."""
    cmd._check_compiler()
    body = textwrap.dedent('\n        static int static_func (char * %(restrict)s a)\n        {\n            return 0;\n        }\n        ')
    for kw in ['restrict', '__restrict__', '__restrict']:
        st = cmd.try_compile(body % {'restrict': kw}, None, None)
        if st:
            return kw
    return ''

def check_compiler_gcc4(cmd):
    """Return True if the C compiler is GCC 4.x."""
    cmd._check_compiler()
    body = textwrap.dedent('\n        int\n        main()\n        {\n        #if (! defined __GNUC__) || (__GNUC__ < 4)\n        #error gcc >= 4 required\n        #endif\n            return 0;\n        }\n        ')
    return cmd.try_compile(body, None, None)

def check_gcc_function_attribute(cmd, attribute, name):
    """Return True if the given function attribute is supported."""
    cmd._check_compiler()
    body = textwrap.dedent('\n        #pragma GCC diagnostic error "-Wattributes"\n        #pragma clang diagnostic error "-Wattributes"\n\n        int %s %s(void* unused)\n        {\n            return 0;\n        }\n\n        int\n        main()\n        {\n            return 0;\n        }\n        ') % (attribute, name)
    return cmd.try_compile(body, None, None) != 0

def check_gcc_function_attribute_with_intrinsics(cmd, attribute, name, code, include):
    """Return True if the given function attribute is supported with
    intrinsics."""
    cmd._check_compiler()
    body = textwrap.dedent('\n        #include<%s>\n        int %s %s(void)\n        {\n            %s;\n            return 0;\n        }\n\n        int\n        main()\n        {\n            return 0;\n        }\n        ') % (include, attribute, name, code)
    return cmd.try_compile(body, None, None) != 0

def check_gcc_variable_attribute(cmd, attribute):
    """Return True if the given variable attribute is supported."""
    cmd._check_compiler()
    body = textwrap.dedent('\n        #pragma GCC diagnostic error "-Wattributes"\n        #pragma clang diagnostic error "-Wattributes"\n\n        int %s foo;\n\n        int\n        main()\n        {\n            return 0;\n        }\n        ') % (attribute,)
    return cmd.try_compile(body, None, None) != 0