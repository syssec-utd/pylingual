from zbus_cli.verb import VerbExtension
from argparse import ArgumentTypeError
import zmq
import time
import threading
import math
import msgpack
DEFAULT_WINDOW_SIZE = 10000

def positive_int(string):
    try:
        value = int(string)
    except ValueError:
        value = -1
    if value <= 0:
        raise ArgumentTypeError('value must be a positive integer')
    return value

class DelayVerb(VerbExtension):
    """Display delay of topic from timestamp in header."""

    def add_arguments(self, parser, cli_name):
        arg = parser.add_argument('topic', help='Topic name to calculate the delay for')
        parser.add_argument('--window', '-w', dest='window_size', type=positive_int, default=DEFAULT_WINDOW_SIZE, help='window size, in # of messages, for calculating rate, string to (default: %d)' % DEFAULT_WINDOW_SIZE)

    def main(self, *, args, addr):
        topic = args.topic
        window_size = args.window_size
        topic_delay = TopicDelay(topic=topic, window_size=window_size)
        topic_delay.loop(addr)

class TopicDelay(object):

    def __init__(self, topic, window_size):
        self.lock = threading.Lock()
        self.last_msg_tn = 0
        self.msg_t0 = -1.0
        self.msg_tn = 0
        self.delays = []
        self.topic = topic
        self.window_size = window_size

    def loop(self, addr):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect(addr['sub'])
        socket.subscribe(self.topic)
        while True:
            timeout = 1 * 1000000000.0
            enter_t = time.time_ns()
            while time.time_ns() - enter_t < timeout:
                message = socket.recv_multipart()
                topic = message[0].decode('utf8')
                if topic == self.topic:
                    msg = msgpack.loads(message[1])
                    self.callback_delay(msg)
            self.print_delay()

    def callback_delay(self, msg):
        """
        Calculate delay time.

        :param msg: Message instance
        """
        if 'header' not in msg.keys():
            raise RuntimeError('msg does not have header')
        curr = time.time_ns()
        if self.msg_t0 < 0 or self.msg_t0 > curr:
            self.msg_t0 = curr
            self.msg_tn = curr
            self.delays = []
        else:
            duration = curr - self.time_from_msg(msg['header']['stamp'])
            self.delays.append(duration)
            self.msg_tn = curr
        if len(self.delays) > self.window_size:
            self.delays.pop(0)

    def time_from_msg(self, stamp) -> float:
        return stamp['sec'] * 1.0 * 1000000000.0 + stamp['nanosec']

    def get_delay(self):
        """
        Calculate the average publising delay.

        :returns: tuple of stat results
            (rate, min_delta, max_delta, standard deviation, window number)
            None when waiting for the first message or there is no new one
        """
        if self.msg_tn == self.last_msg_tn:
            return
        if not self.delays:
            return
        n = len(self.delays)
        mean = sum(self.delays) / n
        std_dev = math.sqrt(sum(((x - mean) ** 2 for x in self.delays)) / n)
        max_delta = max(self.delays)
        min_delta = min(self.delays)
        self.last_msg_tn = self.msg_tn
        return (mean, min_delta, max_delta, std_dev, n)

    def print_delay(self):
        """Print the average publishing delay to screen."""
        if not self.delays:
            return
        ret = self.get_delay()
        if ret is None:
            print('no new messages')
            return
        (delay, min_delta, max_delta, std_dev, window) = ret
        print('average delay: %.3f\n\tmin: %.3fs max: %.3fs std dev: %.5fs window: %s' % (delay * 1e-09, min_delta * 1e-09, max_delta * 1e-09, std_dev * 1e-09, window))