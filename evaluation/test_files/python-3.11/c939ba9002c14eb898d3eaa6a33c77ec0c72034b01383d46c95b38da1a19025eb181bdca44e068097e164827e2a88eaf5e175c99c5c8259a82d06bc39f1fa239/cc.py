"""SCons.Tool.cc

Tool-specific initialization for generic Posix C compilers.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.
"""
__revision__ = '__FILE__ __REVISION__ __DATE__ __DEVELOPER__'
import SCons.Tool
import SCons.Defaults
import SCons.Util
CSuffixes = ['.c', '.m']
if not SCons.Util.case_sensitive_suffixes('.c', '.C'):
    CSuffixes.append('.C')

def add_common_cc_variables(env):
    """
    Add underlying common "C compiler" variables that
    are used by multiple tools (specifically, c++).
    """
    if '_CCCOMCOM' not in env:
        env['_CCCOMCOM'] = '$CPPFLAGS $_CPPDEFFLAGS $_CPPINCFLAGS'
        env['FRAMEWORKS'] = SCons.Util.CLVar('')
        env['FRAMEWORKPATH'] = SCons.Util.CLVar('')
        if env['PLATFORM'] == 'darwin':
            env['_CCCOMCOM'] = env['_CCCOMCOM'] + ' $_FRAMEWORKPATH'
    if 'CCFLAGS' not in env:
        env['CCFLAGS'] = SCons.Util.CLVar('')
    if 'SHCCFLAGS' not in env:
        env['SHCCFLAGS'] = SCons.Util.CLVar('$CCFLAGS')
compilers = ['cc']

def generate(env):
    """
    Add Builders and construction variables for C compilers to an Environment.
    """
    static_obj, shared_obj = SCons.Tool.createObjBuilders(env)
    for suffix in CSuffixes:
        static_obj.add_action(suffix, SCons.Defaults.CAction)
        shared_obj.add_action(suffix, SCons.Defaults.ShCAction)
        static_obj.add_emitter(suffix, SCons.Defaults.StaticObjectEmitter)
        shared_obj.add_emitter(suffix, SCons.Defaults.SharedObjectEmitter)
    add_common_cc_variables(env)
    if 'CC' not in env:
        env['CC'] = env.Detect(compilers) or compilers[0]
    env['CFLAGS'] = SCons.Util.CLVar('')
    env['CCCOM'] = '$CC -o $TARGET -c $CFLAGS $CCFLAGS $_CCCOMCOM $SOURCES'
    env['SHCC'] = '$CC'
    env['SHCFLAGS'] = SCons.Util.CLVar('$CFLAGS')
    env['SHCCCOM'] = '$SHCC -o $TARGET -c $SHCFLAGS $SHCCFLAGS $_CCCOMCOM $SOURCES'
    env['CPPDEFPREFIX'] = '-D'
    env['CPPDEFSUFFIX'] = ''
    env['INCPREFIX'] = '-I'
    env['INCSUFFIX'] = ''
    env['SHOBJSUFFIX'] = '.os'
    env['STATIC_AND_SHARED_OBJECTS_ARE_THE_SAME'] = 0
    env['CFILESUFFIX'] = '.c'

def exists(env):
    return env.Detect(env.get('CC', compilers))