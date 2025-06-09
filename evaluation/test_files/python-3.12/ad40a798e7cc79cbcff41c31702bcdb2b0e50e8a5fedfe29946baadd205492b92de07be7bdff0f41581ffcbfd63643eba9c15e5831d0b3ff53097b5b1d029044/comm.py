from enum import IntEnum
from .types import SerialOrNetwork
from .encoding import *
from serial import Serial
from crccheck.crc import Crc8Maxim
SENSOR_GONE = b'\xff\x7f'

class ReadtimeoutException(Exception):
    pass

class ChecksumNotMatchingException(Exception):
    pass

class InvalidHeaderException(Exception):
    pass

class IllegalArgumentException(Exception):
    pass

class ReaderState(IntEnum):
    LOOKING_FOR_HEADER = 0
    EXPECTING_MSG_NO = 1
    EXPECTING_TYPE = 2
    EXPECTING_AFTER_TYPE = 3
    EXPECTING_SIZE = 4
    READING_PAYLOAD = 5
    EXPECTING_CHECKSUM = 6
    ESCAPING = 7

class HanazederPacket:
    msg_no = None
    msg_type = None
    msg_size = None
    msg = None

class HanazederReader:
    state = ReaderState.LOOKING_FOR_HEADER
    packet: HanazederPacket = None

    def __init__(self, connection, header, debug):
        self.connection = connection
        self.header = header[0]
        self.debug = debug

    def read(self, byte: int) -> HanazederPacket:
        finished_packet = self.handle_byte(byte)
        if finished_packet:
            return finished_packet

    def handle_byte(self, byte: int) -> HanazederPacket:
        if self.state != ReaderState.ESCAPING and self.state != ReaderState.LOOKING_FOR_HEADER and (self.state != ReaderState.EXPECTING_CHECKSUM):
            self.crc.process(byte.to_bytes(1, byteorder='little'))
        if self.debug:
            print(f'Handle_byte {byte} state in {self.state}')
        if self.state == ReaderState.LOOKING_FOR_HEADER:
            if byte == self.header:
                self.packet = HanazederPacket()
                self.state = ReaderState.EXPECTING_MSG_NO
                self.crc = Crc8Maxim()
        elif self.state == ReaderState.EXPECTING_MSG_NO:
            self.packet.msg_no = byte
            self.state = ReaderState.EXPECTING_TYPE
        elif self.state == ReaderState.EXPECTING_TYPE:
            self.packet.msg_type = byte
            self.state = ReaderState.EXPECTING_SIZE
        elif self.state == ReaderState.EXPECTING_SIZE:
            self.packet.msg_size = byte
            self.packet.msg = bytearray()
            self.state = ReaderState.READING_PAYLOAD
        elif self.state == ReaderState.READING_PAYLOAD or self.state == ReaderState.ESCAPING:
            if byte == self.header and self.state == ReaderState.READING_PAYLOAD:
                self.state = ReaderState.ESCAPING
            else:
                self.packet.msg += bytearray(byte.to_bytes(1, byteorder='little'))
                self.packet.msg_size = self.packet.msg_size - 1
            if self.packet.msg_size <= 0:
                self.state = ReaderState.EXPECTING_CHECKSUM
            else:
                self.state = ReaderState.READING_PAYLOAD
        elif self.state == ReaderState.EXPECTING_CHECKSUM:
            self.state = ReaderState.LOOKING_FOR_HEADER
            calculated_crc = self.crc.finalbytes()
            if calculated_crc[0] != byte:
                print('Wrong checksum')
            else:
                return self.packet
        if self.debug:
            print(f'Handle_byte state out {self.state}')

def hanazeder_decode_num(header, value) -> float:
    if value == SENSOR_GONE:
        return None
    int_val = int.from_bytes(value, byteorder='little', signed=True)
    return int_val / 10

def hanazeder_decode_byte(byte: bytes) -> int:
    return int.from_bytes(byte, byteorder='little')

def hanazeder_read(expected_header: bytes, msg_num: int, connection: SerialOrNetwork) -> bytes:
    header = connection.read(4)
    if len(header) < 4:
        raise ReadtimeoutException('Could not read header')
    if header[0] is not expected_header[0]:
        raise InvalidHeaderException(f'Expecting header {expected_header[0]}, got {header[0]} instead')
    if header[1] != msg_num:
        raise InvalidHeaderException(f'Expecting message number {msg_num} but got {header[1]}')
    value_size = header[3]
    value = connection.read(value_size)
    checksum = connection.read(1)
    crc = Crc8Maxim()
    crc.process(header[1:])
    crc.process(value)
    calculated_crc = crc.finalbytes()
    if calculated_crc != checksum:
        raise ChecksumNotMatchingException(f'Expected checksum {calculated_crc} but got {checksum}')
    return value

def hanazeder_encode_msg(header: bytes, msg_num: int, request: bytes) -> bytes:
    if msg_num < 0 or msg_num > 255:
        raise IllegalArgumentException('msg_num must be between 0 and 255')
    if len(header) != 1:
        raise IllegalArgumentException('header must be single byte')
    msg = bytearray(header)
    msg.append(msg_num)
    msg += bytearray(request)
    checksum = Crc8Maxim.calcbytes(msg[1:])
    msg += bytearray(checksum)
    return bytes(msg)