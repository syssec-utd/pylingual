import functools
import re
from typing import Union
from eth_abi import encode_abi as eth_abi_encode_abi
from eth_abi.exceptions import EncodingError
from eth_utils import to_hex, function_abi_to_4byte_selector
from hexbytes import HexBytes
from trx_utils import is_text, encode_hex
from trx_utils.typing import HexStr
from tronpytool.common.abi import filter_by_name, filter_by_encodability, filter_by_argument_count, get_fallback_func_abi, abi_to_signature, get_abi_input_types, check_if_arguments_can_be_encoded, map_abi_data, merge_args_and_kwargs
from tronpytool.common.normalizers import abi_address_to_hex, abi_bytes_to_bytes, abi_string_to_text
from tronpytool.common.toolz import pipe, valmap

class FallbackFn:
    pass

def find_match_tron_address(test_str: str) -> str:
    regex = '\\T.[a-zA-Z0-9]{32}'
    matches = re.search(regex, test_str)
    if matches:
        print('Match was found at {start}-{end}: {match}'.format(start=matches.start(), end=matches.end(), match=matches.group()))
        for groupNum in range(0, len(matches.groups())):
            groupNum = groupNum + 1
            print('Group {groupNum} found at {start}-{end}: {group}'.format(groupNum=groupNum, start=matches.start(groupNum), end=matches.end(groupNum), group=matches.group(groupNum)))
    return matches

def find_matching_fn_abi(abi, fn_identifier=None, args=None, kwargs=None):
    args = args or tuple()
    kwargs = kwargs or dict()
    filters = []
    num_arguments = len(args) + len(kwargs)
    diagnosis = None
    if fn_identifier is FallbackFn:
        return get_fallback_func_abi(abi)
    if not is_text(fn_identifier):
        raise TypeError('Unsupported function identifier')
    name_filter = functools.partial(filter_by_name, fn_identifier)
    arg_count_filter = functools.partial(filter_by_argument_count, num_arguments)
    encoding_filter = functools.partial(filter_by_encodability, args, kwargs)
    filters.extend([name_filter, arg_count_filter, encoding_filter])
    function_candidates = pipe(abi, *filters)
    if len(function_candidates) == 1:
        return function_candidates[0]
    else:
        matching_identifiers = name_filter(abi)
        matching_function_signatures = [abi_to_signature(func) for func in matching_identifiers]
        arg_count_matches = len(arg_count_filter(matching_identifiers))
        encoding_matches = len(encoding_filter(matching_identifiers))
        if arg_count_matches == 0:
            diagnosis = '\nFunction invocation failed due to improper number of arguments.'
        elif encoding_matches == 0:
            diagnosis = '\nFunction invocation failed due to no matching argument types.'
        elif encoding_matches > 1:
            diagnosis = '\nAmbiguous argument encoding. Provided arguments can be encoded to multiple functions matching this call.'
        message = '\nCould not identify the intended function with name `{name}`, positional argument(s) of type `{arg_types}` and keyword argument(s) of type `{kwarg_types}`.\nFound {num_candidates} function(s) with the name `{name}`: {candidates}{diagnosis}'.format(name=fn_identifier, arg_types=tuple(map(type, args)), kwarg_types=valmap(type, kwargs), num_candidates=len(matching_identifiers), candidates=matching_function_signatures, diagnosis=diagnosis)
        raise ValueError(message)

def encode_abi(tron, abi, arguments, data=None) -> Union[HexStr, str]:
    argument_types = get_abi_input_types(abi)
    if not check_if_arguments_can_be_encoded(abi, arguments, {}):
        raise TypeError('One or more arguments could not be encoded to the necessary ABI type.  Expected types are: {0}'.format(', '.join(argument_types)))
    try:
        normalizers = [abi_address_to_hex, abi_bytes_to_bytes, abi_string_to_text]
        normalized_arguments = map_abi_data(normalizers, argument_types, arguments)
        encoded_arguments = eth_abi_encode_abi(argument_types, normalized_arguments)
    except EncodingError as e:
        raise TypeError('One or more arguments could not be encoded to the necessary ABI type: {0}'.format(str(e)))
    if data:
        return to_hex(HexBytes(data) + encoded_arguments)
    else:
        return encode_hex(encoded_arguments)

def get_function_info(fn_name, contract_abi=None, fn_abi=None, args=None, kwargs=None):
    if args is None:
        args = tuple()
    if kwargs is None:
        kwargs = {}
    if fn_abi is None:
        fn_abi = find_matching_fn_abi(contract_abi, fn_name, args, kwargs)
    fn_selector = encode_hex(function_abi_to_4byte_selector(fn_abi))
    fn_arguments = merge_args_and_kwargs(fn_abi, args, kwargs)
    return (fn_abi, fn_selector, fn_arguments)