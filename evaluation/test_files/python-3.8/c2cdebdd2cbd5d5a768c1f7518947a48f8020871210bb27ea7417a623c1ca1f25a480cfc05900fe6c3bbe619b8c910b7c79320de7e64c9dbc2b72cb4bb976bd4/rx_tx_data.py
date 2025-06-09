import re
import struct
from functools import reduce, partial
from typing import Iterable, Tuple

def array_to_integer(element_bit_width: int, data: Iterable[int]) -> Tuple[int]:
    return (reduce(lambda x, y: (x << element_bit_width) + y, data, 0),)

class TxData:
    """Models the tx data that is exchanged. It it primarily a descriptor that knows how to convert structured
    data into a list of raw bytes"""

    def __init__(self, cmd_id, descriptor, device_busy_delay=0.0, slave_address=None, ignore_ack=False):
        self._cmd_id = cmd_id
        self._command_width = 2
        if descriptor.startswith('>B'):
            self._command_width = 1
        self._descriptor = descriptor
        self._slave_address = slave_address
        self._device_busy_delay = device_busy_delay
        self._ignore_acknowledge = ignore_ack

    def pack(self, argument_list=[]):
        data_to_pack = [self._cmd_id]
        for arg in argument_list:
            if isinstance(arg, (list, tuple)):
                data_to_pack.extend(arg)
            else:
                data_to_pack.append(arg)
        return bytearray(struct.pack(self._descriptor, *data_to_pack))

    @property
    def command_width(self):
        return self._command_width

    @property
    def slave_address(self):
        return self._slave_address

    @property
    def device_busy_delay(self):
        return self._device_busy_delay

    @property
    def ignore_acknowledge(self):
        return self._ignore_acknowledge

class RxData:
    """Descriptor for data to be received"""
    is_array = re.compile('>\\d+(?P<INT_TYPE>(B|H|I))$')
    field_match = re.compile('(?P<length>\\d*)(?P<descriptor>(h|H|b|B|i|I|\\?|s|q|Q|f|d))')
    element_size_map = {'B': 8, 'I': 32, 'H': 16}

    def __init__(self, descriptor=None, convert_to_int=False):
        self._descriptor = descriptor
        self._rx_length = 0
        self._conversion_function = None
        if self._descriptor is None:
            return
        self._rx_length = struct.calcsize(self._descriptor)
        if not convert_to_int:
            return
        match = RxData.is_array.match(descriptor)
        if not match:
            return
        bit_width = RxData.element_size_map[match.group('INT_TYPE')]
        self._conversion_function = partial(array_to_integer, element_bit_width=bit_width)

    @property
    def rx_length(self):
        return self._rx_length

    def unpack(self, data):
        data = struct.unpack(self._descriptor, data)
        if self._conversion_function is None:
            return data
        return self._conversion_function(data=data)

    def unpack_dynamic_sized(self, data):
        byte_order_specifier = self._descriptor[0]
        (descriptor_pos, data_pos) = (1, 0)
        unpacked = []
        match = self.field_match.match(self._descriptor, descriptor_pos)
        while match:
            descriptor = f"{byte_order_specifier}{match.group('descriptor')}"
            elem_size = struct.calcsize(descriptor)
            length = match.group('length')
            descriptor_pos += len(length) + len(descriptor)
            if length:
                field_len = 0
                for i in range(data_pos, min(data_pos + elem_size * int(length), len(data))):
                    if data[i] == 0 and descriptor == 's':
                        break
                    field_len += 1
                descriptor = f'{field_len // elem_size}{descriptor}'
                elem_size = struct.calcsize(descriptor)
            unpacked.extend(struct.unpack_from(descriptor, data, data_pos))
            data_pos += elem_size
            match = self.field_match.match(self._descriptor, descriptor_pos)
        if self._conversion_function:
            return self._conversion_function(unpacked)
        return tuple(unpacked)