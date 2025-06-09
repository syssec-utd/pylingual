"""
 * Created by Synerty Pty Ltd
 *
 * This software is open source, the MIT license applies.
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
"""
import gc
import os
import tracemalloc
from collections import deque
from random import random
from typing import Optional
import psutil
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, Deferred
from twisted.python.failure import Failure
from twisted.trial import unittest
from vortex.Payload import Payload
from vortex.PayloadEndpoint import PayloadEndpoint
from vortex.VortexClientTcp import VortexClientTcp
from vortex.VortexServer import VortexServer
from vortex.VortexServerTcp import VortexTcpServerFactory

class MemoryCheckerTestMixin:

    def _memMark(self):
        self._process = psutil.Process(os.getpid())
        unreachable = gc.collect()
        self._initialMem = self._process.memory_info().rss
        self._initialUnreachable = unreachable
        self._lastMem = self._initialMem

    def _memCheck(self, grace=0):
        unreachable = gc.collect()
        self.assertLessEqual(unreachable, self._initialUnreachable, "The garbage collector couldn't release everything")
        self._memPrintIncrease()
        memNow = self._process.memory_info().rss
        self.assertLessEqual(memNow, self._initialMem + grace)

    def _memPrintIncrease(self, printOnlyOnGrowth=False):
        gc.collect()
        memNow = self._process.memory_info().rss
        thisDiff = memNow - self._initialMem
        lastDiff = self._lastMem - self._initialMem
        growth = thisDiff - lastDiff
        self._lastMem = memNow
        if not printOnlyOnGrowth or growth:
            print('Memory growth is %s, total growth %s, total %s' % ('{:,d}'.format(growth), '{:,d}'.format(thisDiff), '{:,d}'.format(memNow)))

    def _memCheckFunction(self, callable, loopCount, *args, **kwargs):
        assert loopCount >= 10, 'We need at least 10 loops to check this'
        startMemIndex = 5
        for index in range(loopCount):
            if index == startMemIndex:
                self._memMark()
            callable(*args, **kwargs)
            if startMemIndex <= index:
                self._memPrintIncrease(printOnlyOnGrowth=True)
        self._memCheck(grace=0)

class VortexTcpConnectTestMixin:

    @inlineCallbacks
    def _connect(self):
        port = 20000 + int(random() * 10000)
        self._vortexServer = VortexServer('test server')
        vortexTcpServerFactory = VortexTcpServerFactory(self._vortexServer)
        self._listenPort = reactor.listenTCP(port, vortexTcpServerFactory)
        self._vortexClient = VortexClientTcp('test client')
        yield self._vortexClient.connect('127.0.0.1', port)

    def _disconnect(self):
        self._listenPort.stopListening()
        del self._listenPort
        self._vortexServer.shutdown()
        del self._vortexServer
        self._vortexClient.close()
        del self._vortexClient

class VortexSendReceiveTestMixin:
    _loopbackFilt = {'key': 'unittest'}

    class _State:

        def __init__(self, testSelf, sendFromServerOnly):
            self.testSelf = testSelf
            self.sendFromServerOnly = sendFromServerOnly
            self.dataSizeStats = []
            self.vortexSizeStats = []
            self.dataQueue = deque()
            self.dataQueueEmptyDeferred = Deferred()
            self.totalSent = 0
            self.totalReceived = 0
            self.totalMessagesSent = 0
            self.totalMessagesReceived = 0
            self.totalMessagesOutOfOrder = 0
            self.highestOutOfOrderIndex = 0
            self.totalSentFromClient = 0
            self.totalSentFromServer = 0

        def vortex(self, dataLen: int):
            if not self.sendFromServerOnly and random() < 0.5:
                self.totalSentFromClient += dataLen
                return self.testSelf._vortexClient
            self.totalSentFromServer += dataLen
            return self.testSelf._vortexServer

    class _Checker:

        def __init__(self, testSelf, state, printStatusEveryXMessage):
            self.endpoint = None
            self.testSelf = testSelf
            self.state = state
            self.printStatusEveryXMessage = printStatusEveryXMessage

        def setEndpoint(self, endpoint):
            self.endpoint = endpoint

        @inlineCallbacks
        def process(self, payloadEnvelope, *args, **kwargs):
            try:
                payload = (yield payloadEnvelope.decodePayloadDefer())
                dataReceived = payload.tuples[0]
                self.state.totalReceived += len(dataReceived)
                self.state.totalMessagesReceived += 1
                dataSent = None
                for (index, item) in enumerate(self.state.dataQueue):
                    if item == dataReceived:
                        dataSent = dataReceived
                        if index:
                            self.state.totalMessagesOutOfOrder += 1
                            self.state.highestOutOfOrderIndex = max(self.state.highestOutOfOrderIndex, index)
                            self.state.dataQueue.remove(item)
                        else:
                            self.state.dataQueue.popleft()
                        break
                if not self.state.totalMessagesReceived % self.printStatusEveryXMessage:
                    print('Received message %s, this %s, total %s' % (self.state.totalMessagesReceived, '{:,d}'.format(len(dataReceived)), '{:,d}'.format(self.state.totalReceived)))
                self.testSelf.assertEqual(dataReceived, dataSent)
                if not self.state.dataQueue:
                    self.state.dataQueueEmptyDeferred.callback(True)
            except Exception as e:
                self.endpoint.shutdown()
                self.state.dataQueueEmptyDeferred.errback(Failure(e))

    @inlineCallbacks
    def _vortexTestTcpServerClient(self, printStatusEveryXMessage: Optional[int]=1000, maxMessageSizeBytes: Optional[int]=None, exactMessageSizeBytes: Optional[int]=None, totalBytesToSend: Optional[int]=None, totalMessagesToSend: Optional[int]=None, payloadCompression=9, sendFromServerOnly=False):
        assert totalBytesToSend or totalMessagesToSend, 'We must have a total to send'
        assert maxMessageSizeBytes or exactMessageSizeBytes, 'We must have a msg size'
        state = self._State(self, sendFromServerOnly)
        checker = self._Checker(self, state, printStatusEveryXMessage)
        endpoint = PayloadEndpoint(self._loopbackFilt, checker.process)
        checker.setEndpoint(endpoint)

        def makeData():
            size = random() * maxMessageSizeBytes if exactMessageSizeBytes is None else exactMessageSizeBytes
            packet = str(random())
            while len(packet) < size:
                packet += str(random())
            if exactMessageSizeBytes is not None:
                packet = packet[:exactMessageSizeBytes]
            return packet

        def check():
            if totalMessagesToSend and state.totalMessagesSent < totalMessagesToSend:
                return True
            if totalBytesToSend and state.totalSent < totalBytesToSend:
                return True
            return False
        while check():
            data = makeData()
            state.dataQueue.append(data)
            state.totalSent += len(data)
            state.totalMessagesSent += 1
            vortexMsg = (yield Payload(self._loopbackFilt, data).makePayloadEnvelopeVortexMsgDefer(compressionLevel=payloadCompression))
            state.dataSizeStats.append(len(data))
            state.vortexSizeStats.append(len(vortexMsg))
            state.vortex(len(data)).sendVortexMsg(vortexMsg)
            if not state.totalMessagesSent % printStatusEveryXMessage:
                print('Sent     message %s, this %s, total %s' % (state.totalMessagesSent, '{:,d}'.format(len(data)), '{:,d}'.format(state.totalSent)))
        yield state.dataQueueEmptyDeferred
        print('%s messages were out of order, the most out of order was %s' % (state.totalMessagesOutOfOrder, state.highestOutOfOrderIndex))
        print('Sent %s from the vortex client' % '{:,d}'.format(state.totalSentFromClient))
        print('Sent %s from the vortex server' % '{:,d}'.format(state.totalSentFromServer))
        print('Data     : count %s, total size %s, max size %s, min size %s, average %s' % (state.totalMessagesSent, '{:,d}'.format(state.totalSent), '{:,d}'.format(max(state.dataSizeStats)), '{:,d}'.format(min(state.dataSizeStats)), '{:,d}'.format(int(state.totalSent / state.totalMessagesSent))))
        totalVortexMsgs = sum(state.vortexSizeStats)
        print('VortexMsg: count %s, total size %s, max size %s, min size %s, average %s' % (state.totalMessagesSent, '{:,d}'.format(totalVortexMsgs), '{:,d}'.format(max(state.vortexSizeStats)), '{:,d}'.format(min(state.vortexSizeStats)), '{:,d}'.format(int(totalVortexMsgs / state.totalMessagesSent))))
        self.assertEqual(state.totalSent, state.totalReceived)
        self.assertFalse(len(state.dataQueue))
        endpoint.shutdown()
        del checker
        del state
        del endpoint
        gc.collect()

class VortexTcpConnectTest(unittest.TestCase, MemoryCheckerTestMixin, VortexTcpConnectTestMixin, VortexSendReceiveTestMixin):

    @inlineCallbacks
    def __vortexReconnect(self, count):
        self._memMark()
        for x in range(count):
            print('Reconnecting #%s' % x)
            yield self._connect()
            self._disconnect()
            self._memPrintIncrease()
        self._memPrintIncrease()

    @inlineCallbacks
    def test_vortexReconnect100(self):
        yield self.__vortexReconnect(100)

    @inlineCallbacks
    def __vortexReconnect_with_data(self, count):
        self._memMark()
        for x in range(count):
            print('Reconnecting #%s' % x)
            yield self._connect()
            yield self._vortexTestTcpServerClient(totalMessagesToSend=10, exactMessageSizeBytes=100 * 1024)
            self._disconnect()
            self._memPrintIncrease()
        self._memPrintIncrease()

    @inlineCallbacks
    def test_vortexReconnect100_with_data(self):
        yield self.__vortexReconnect_with_data(100)

class VortexTcpMemoryLeakTest(unittest.TestCase, MemoryCheckerTestMixin, VortexTcpConnectTestMixin, VortexSendReceiveTestMixin):

    @inlineCallbacks
    def __vortexSendMsgCountMsgSize(self, count, size, compression=9):
        self._memMark()
        yield self._connect()
        yield self._vortexTestTcpServerClient(totalMessagesToSend=count, printStatusEveryXMessage=1000, exactMessageSizeBytes=size, payloadCompression=compression)
        self._disconnect()
        self._memPrintIncrease()

    @inlineCallbacks
    def test_1vortexSend1_1kb_compression1(self):
        yield self.__vortexSendMsgCountMsgSize(1, 1 * 1024, 1)

    @inlineCallbacks
    def test_1vortexSend1_300kb_compression1(self):
        yield self.__vortexSendMsgCountMsgSize(1, 300 * 1024, 1)

    @inlineCallbacks
    def test_1vortexSend10000_1kb_compression1(self):
        yield self.__vortexSendMsgCountMsgSize(10000, 1 * 1024, 1)

    @inlineCallbacks
    def test_1vortexSend10000_100kb_compression1(self):
        yield self.__vortexSendMsgCountMsgSize(10000, 100 * 1024, 1)

    @inlineCallbacks
    def test_1vortexSend10000_1kb_compression9(self):
        yield self.__vortexSendMsgCountMsgSize(10000, 1 * 1024, 9)

    @inlineCallbacks
    def test_1vortexSend10000_100kb_compression9(self):
        yield self.__vortexSendMsgCountMsgSize(10000, 100 * 1024, 9)

    @inlineCallbacks
    def __vortexSendTotalSendMsgSize(self, totalSend, msgSize, compression=9, fromServer=False):
        self._memMark()
        yield self._connect()
        yield self._vortexTestTcpServerClient(totalBytesToSend=totalSend, printStatusEveryXMessage=1000, maxMessageSizeBytes=msgSize, sendFromServerOnly=fromServer, payloadCompression=compression)
        self._disconnect()
        self._memPrintIncrease()

    @inlineCallbacks
    def test_2vortexSend1mb_1kb(self):
        yield self.__vortexSendTotalSendMsgSize(1024 ** 2, 1 * 1024)

    @inlineCallbacks
    def test_2vortexSend1mb_100kb(self):
        yield self.__vortexSendTotalSendMsgSize(1024 ** 2, 100 * 1024)

    @inlineCallbacks
    def test_3vortexSend1mb_X10_yes_reconnect(self):
        mem = MemoryCheckerTestMixin()
        mem._memMark()
        print(' ===== START LOOP ===== ')
        for i in range(10):
            print(' ===== Running iteration %s ===== ' % i)
            self._memMark()
            yield self._connect()
            yield self._vortexTestTcpServerClient(totalBytesToSend=1024 ** 2, printStatusEveryXMessage=1000, maxMessageSizeBytes=100 * 1024)
            self._disconnect()
            self._memPrintIncrease()
        print(' ===== END LOOP ===== ')
        mem._memPrintIncrease()

    @inlineCallbacks
    def test_3vortexSend1mb_X10_no_reconnect(self):
        mem = MemoryCheckerTestMixin()
        mem._memMark()
        yield self._connect()
        print(' ===== START LOOP ===== ')
        for i in range(10):
            print(' ===== Running iteration %s ===== ' % i)
            self._memMark()
            yield self._vortexTestTcpServerClient(totalBytesToSend=1024 ** 2, printStatusEveryXMessage=1000, maxMessageSizeBytes=1 * 1024)
            self._memPrintIncrease()
        self._disconnect()
        print(' ===== END LOOP ===== ')
        mem._memPrintIncrease()

    @inlineCallbacks
    def test_4vortexSend10mb(self):
        yield self.__vortexSendTotalSendMsgSize(1024 ** 2 * 10, 100 * 1024)

    @inlineCallbacks
    def test_5vortexSend100mb(self):
        yield self.__vortexSendTotalSendMsgSize(1024 ** 2 * 100, 1024 ** 2)

    @inlineCallbacks
    def test_6vortexSend500mb(self):
        yield self.__vortexSendTotalSendMsgSize(1024 ** 2 * 500, 1024 ** 2)

class VortexTcpMemoryLeakLargeMessagesTest(unittest.TestCase, MemoryCheckerTestMixin, VortexTcpConnectTestMixin, VortexSendReceiveTestMixin):
    timeout = 30 * 60
    _patchedProcessData_dataReceivedLen = 0

    def _processData_patch(self):
        VortexTcpMemoryLeakLargeMessagesTest._patchedProcessData_dataReceivedLen += len(self._data)
        self._data = b''

    @inlineCallbacks
    def __vortexSend1g_oneway_maxmsg(self, msgSize, totalSize=1024 ** 2 * 500):
        tracemalloc.start(5)
        self._memMark()
        yield self._connect()
        yield self._vortexTestTcpServerClient(totalBytesToSend=totalSize, printStatusEveryXMessage=1000, exactMessageSizeBytes=msgSize, sendFromServerOnly=True, payloadCompression=0)
        self._disconnect()
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        print('[ Top 10 ]')
        for stat in top_stats[:10]:
            print(stat)
        tracemalloc.stop()
        for _ in range(5):
            d = Deferred()
            reactor.callLater(2, d.callback, True)
            print('Sleeping 2 seconds')
            yield d
            self._memPrintIncrease()

    @inlineCallbacks
    def test_1vortexSend50mb_oneway_msg10kb(self):
        yield self.__vortexSend1g_oneway_maxmsg(10 * 1024, totalSize=1024 ** 2 * 50)

    @inlineCallbacks
    def test_1vortexSend50mb_oneway_msg100kb(self):
        yield self.__vortexSend1g_oneway_maxmsg(100 * 1024, totalSize=1024 ** 2 * 50)

    @inlineCallbacks
    def test_1vortexSend50mb_oneway_msg1mb(self):
        yield self.__vortexSend1g_oneway_maxmsg(1 * 1024 ** 2, totalSize=1024 ** 2 * 50)

    @inlineCallbacks
    def test_1vortexSend50mb_oneway_msg3mb(self):
        yield self.__vortexSend1g_oneway_maxmsg(3 * 1024 ** 2, totalSize=1024 ** 2 * 50)

    @inlineCallbacks
    def test_1vortexSend50mb_oneway_msg10mb(self):
        yield self.__vortexSend1g_oneway_maxmsg(10 * 1024 ** 2, totalSize=1024 ** 2 * 50)

    @inlineCallbacks
    def test_1vortexSend50mb_oneway_msg50mb(self):
        yield self.__vortexSend1g_oneway_maxmsg(50 * 1024 ** 2, totalSize=1024 ** 2 * 50)

    @inlineCallbacks
    def test_1vortexSend500mb_oneway_msg10mb(self):
        yield self.__vortexSend1g_oneway_maxmsg(10 * 1024 ** 2, totalSize=500 * 1024 ** 2)

class VortexTcpMemoryLeakLargeTransfersTest(unittest.TestCase, MemoryCheckerTestMixin, VortexTcpConnectTestMixin, VortexSendReceiveTestMixin):

    @inlineCallbacks
    def __vortexSendTest(self, total, compression):
        self._memMark()
        yield self._connect()
        yield self._vortexTestTcpServerClient(totalBytesToSend=total, printStatusEveryXMessage=10000, maxMessageSizeBytes=10 * 1024 ** 2, payloadCompression=compression)
        self._disconnect()
        self._memPrintIncrease()

    @inlineCallbacks
    def test_2vortexSend1gb_compression1(self):
        yield self.__vortexSendTest(1024 ** 3, compression=1)

    @inlineCallbacks
    def test_3vortexSend3gb_compression1(self):
        yield self.__vortexSendTest(1024 ** 3 * 3, compression=1)