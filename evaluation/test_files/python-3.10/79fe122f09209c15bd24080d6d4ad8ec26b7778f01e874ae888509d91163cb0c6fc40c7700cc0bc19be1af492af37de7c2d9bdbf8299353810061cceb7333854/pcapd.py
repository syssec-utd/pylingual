from __future__ import print_function
import os
from six import PY3
import struct
import time
import sys
import logging
sys.path.append(os.getcwd())
from ios_device.util.lockdown import LockdownClient
from tempfile import mkstemp
from optparse import OptionParser
'\nstruct pcap_hdr_s {\n        guint32 magic_number;   /* magic number */\n        guint16 version_major;  /* major version number */\n        guint16 version_minor;  /* minor version number */\n        gint32  thiszone;       /* GMT to local correction */\n        guint32 sigfigs;        /* accuracy of timestamps */\n        guint32 snaplen;        /* max length of captured packets, in octets */\n        guint32 network;        /* data link type */\n} pcap_hdr_t;\ntypedef struct pcaprec_hdr_s {\n        guint32 ts_sec;         /* timestamp seconds */\n        guint32 ts_usec;        /* timestamp microseconds */\n        guint32 incl_len;       /* number of octets of packet saved in file */\n        guint32 orig_len;       /* actual length of packet */\n} pcaprec_hdr_t;\n'
LINKTYPE_ETHERNET = 1
LINKTYPE_RAW = 101

class PcapOut(object):

    def __init__(self, pipename='test.pcap'):
        self.pipe = open(pipename, 'wb')
        self.pipe.write(struct.pack('<LHHLLLL', 2712847316, 2, 4, 0, 0, 65535, LINKTYPE_ETHERNET))

    def __del__(self):
        self.pipe.close()

    def writePacket(self, packet):
        t = time.time()
        pkthdr = struct.pack('<LLLL', int(t), int(t * 1000000 % 1000000), len(packet), len(packet))
        data = pkthdr + packet
        l = self.pipe.write(data)
        self.pipe.flush()
        return True

class Win32Pipe(object):

    def __init__(self, pipename='\\\\.\\pipe\\wireshark'):
        self.pipe = win32pipe.CreateNamedPipe(pipename, win32pipe.PIPE_ACCESS_OUTBOUND, win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT, 1, 65536, 65536, 300, None)
        print('Connect wireshark to %s' % pipename)
        win32pipe.ConnectNamedPipe(self.pipe, None)
        win32file.WriteFile(self.pipe, struct.pack('<LHHLLLL', 2712847316, 2, 4, 0, 0, 65535, LINKTYPE_ETHERNET))

    def writePacket(self, packet):
        t = time.time()
        pkthdr = struct.pack('<LLLL', int(t), int(t * 1000000 % 1000000), len(packet), len(packet))
        (errCode, nBytesWritten) = win32file.WriteFile(self.pipe, pkthdr + packet)
        return errCode == 0
if __name__ == '__main__':
    if sys.platform == 'darwin':
        print('Why not use rvictl ?')
    parser = OptionParser(usage='%prog')
    parser.add_option('-u', '--udid', default=False, action='store', dest='device_udid', metavar='DEVICE_UDID', help='Device udid')
    parser.add_option('-o', '--output', dest='output', default=False, help='Output location', type='string')
    (options, args) = parser.parse_args()
    if sys.platform == 'win32':
        import win32pipe, win32file
        output = Win32Pipe()
    else:
        if options.output:
            path = options.output
        else:
            (_, path) = mkstemp(prefix='device_dump_', suffix='.pcap', dir='.')
        print('Recording data to: %s' % path)
        output = PcapOut(path)
    logging.basicConfig(level=logging.INFO)
    lockdown = LockdownClient(options.device_udid)
    pcap = lockdown.start_service('com.apple.pcapd')
    while True:
        d = pcap.recv_plist()
        if not d:
            break
        if not PY3:
            d = d.data
        (hdrsize, xxx, packet_size) = struct.unpack('>LBL', d[:9])
        (flags1, flags2, offset_to_ip_data, zero) = struct.unpack('>LLLL', d[9:25])
        assert hdrsize >= 25
        if PY3:
            interfacetype = d[25:hdrsize].strip(b'\x00')
        else:
            interfacetype = d[25:hdrsize].strip('\x00')
            interfacetype = "b'" + '\\x'.join(('{:02x}'.format(ord(c)) for c in interfacetype)) + "'"
        t = time.time()
        print(interfacetype, packet_size, t)
        packet = d[hdrsize:]
        assert packet_size == len(packet)
        if offset_to_ip_data == 0:
            if PY3:
                packet = b'\xbe\xef' * 6 + b'\x08\x00' + packet
            else:
                packet = '¾ï' * 6 + '\x08\x00' + packet
        if not output.writePacket(packet):
            break