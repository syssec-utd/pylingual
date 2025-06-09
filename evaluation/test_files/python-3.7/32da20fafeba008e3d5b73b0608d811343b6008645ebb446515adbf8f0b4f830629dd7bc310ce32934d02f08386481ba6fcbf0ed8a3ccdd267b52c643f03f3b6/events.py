"""
Events for pyaware.
Events are internal pub/sub style messages that are parsed internally to the process.
They are built on the asyncio event loop, so the software must be running an event loop to work.
There can be multiple subscribers to each topic and any thread can publish to any topic, even if there are no
subscribers on that topic.

# Usage
```
import events
import asyncio
import time

@events.subscribe(topic="Hello/World")
async def yo(value):
    await asyncio.sleep(1)
    print(value)

@events.subscribe(topic="#", in_thread=True)
def yo_all(**kwargs)
    time.sleep(0.1)
    print(f"All: {kwargs}")
async def main():
    events.start()
    await events.publish("Hello/World").all()

# Topic Specification

Topic names follow the MQTT style structure taken from
http://public.dhe.ibm.com/software/dw/webservices/ws-mqtt/MQTT_V3.1_Protocol_Specific.pdf

Topic Level Separator
---------------------
The forward slash (/) is used to separate each level within a topic tree and provide
a hierarchical structure to the topic space. The use of the topic level separator is
significant when the two wildcard characters are encountered in topics specified by
subscribers.

Multi-Level Wildcard
--------------------
The number sign (#) is a wildcard character that matches any number of levels
within a topic. For example, if you subscribe to finance/stock/ibm/#, you receive
messages on these topics:
 finance/stock/ibm
 finance/stock/ibm/closingprice
 finance/stock/ibm/currentprice
The multi-level wildcard can represent zero or more levels. Therefore, finance/#
can also match the singular finance, where # represents zero levels. The topic
level separator is meaningless in this context, because there are no levels to
separate.
The multi-level wildcard can be specified only on its own or next to the topic level
separator character. Therefore, # and finance/# are both valid, but finance# is not
valid. The multi-level wildcard must be the last character used within the topic tree.
For example, finance/# is valid but finance/#/closingprice is not valid

Single-Level Wildcard
---------------------
The plus sign (+) is a wildcard character that matches only one topic level. For
example, finance/stock/+ matches finance/stock/ibm and finance/stock/xyz, but
not finance/stock/ibm/closingprice. Also, because the single-level wildcard
matches only a single level, finance/+ does not match finance.
The single-level wildcard can be used at any level in the topic tree, and in
conjunction with the multilevel wildcard. It must be used next to the topic level
separator, except when it is specified on its own. Therefore, + and finance/+ are
both valid, but finance+ is not valid. The single-level wildcard can be used at the
end of the topic tree or within the topic tree. For example, finance/+ and
finance/+/ibm are both valid.

Uses a pub/sub/await style to allow you to synchronise events across pyaware with
"""
import asyncio
import re
from functools import partial
from collections import deque, defaultdict
import pyaware
import logging
import inspect
import threading
from pyaware.exceptions import StopException
log = logging.getLogger(__file__)
evt_stop = threading.Event()

def matches(topic, a_filter):
    topic = topic.casefold()
    return matches_case_sensitive(topic, a_filter)

def matches_case_sensitive(topic, a_filter):
    if '#' not in a_filter and '+' not in a_filter:
        return a_filter == topic
    else:
        match_pattern = re.compile(a_filter.replace('#', '.*').replace('$', '\\$').replace('+', '[/\\$\\s\\w\\d]+'))
        return match_pattern.match(topic)

class TopicTasks:

    def __init__(self, futures):
        self.futures = futures

    async def all(self, timeout=None):
        if self.futures:
            (done, pending) = await asyncio.wait(self.futures, timeout=timeout, return_when=asyncio.ALL_COMPLETED)
            return [x.result() for x in done]

    async def first(self, timeout=None):
        if self.futures:
            (done, pending) = await asyncio.wait(self.futures, timeout=timeout, return_when=asyncio.FIRST_COMPLETED)
            return next(iter(done)).result()

    async def as_completed(self):
        return asyncio.as_completed(self.futures)

class Topic:

    def __init__(self):
        """
        Can only be created once the event loop is running
        """
        self.handles_executor = {}
        self.handles_async = {}
        self._waiters = deque()
        self._cancel = False
        self._last = None

    def publish(self, topic, **data):
        """Set the internal flag to true. All coroutines waiting for it to
        become true are awakened. Coroutine that call wait() once the flag is
        true will not block at all.
        """
        futures = []
        self._last = data
        for fut in self._waiters:
            if not fut.done():
                fut.set_result(data)
        if _loop is None:
            return futures
        if pyaware.from_coroutine():
            if not _loop.is_running() or evt_stop.is_set():
                reset()
                raise asyncio.CancelledError('Event loop is stopped, Raising cancelled Error')
            for (handle, parse_topic) in self.handles_async.values():
                if parse_topic:
                    futures.append(_loop.create_task(pyaware.async_call(handle, topic=topic, **data)))
                else:
                    futures.append(_loop.create_task(pyaware.async_call(handle, **data)))
            for (handle, parse_topic) in self.handles_executor.values():
                if parse_topic:
                    futures.append(_loop.run_in_executor(None, partial(handle, topic=topic, **data)))
                else:
                    futures.append(_loop.run_in_executor(None, partial(handle, **data)))
        else:
            for (handle, parse_topic) in self.handles_async.values():
                if not _loop.is_running() or evt_stop.is_set():
                    reset()
                    raise StopException('Event loop is stopped, Raising error in all connected threads')
                if parse_topic:
                    futures.append(_loop.call_soon_threadsafe(_loop.create_task, pyaware.async_call(handle, topic=topic, **data)))
                else:
                    futures.append(_loop.call_soon_threadsafe(_loop.create_task, pyaware.async_call(handle, **data)))
            for (handle, parse_topic) in self.handles_executor.values():
                if not _loop.is_running() or evt_stop.is_set():
                    reset()
                    raise StopException('Event loop is stopped, Raising error in all connected threads')
                if parse_topic:
                    futures.append(_loop.call_soon_threadsafe(_loop.run_in_executor(None, partial(handle, topic=topic, **data))))
                else:
                    futures.append(_loop.call_soon_threadsafe(_loop.run_in_executor(None, partial(handle, **data))))
        return futures

    def subscribe(self, handle, in_thread=False, parse_topic=False):
        """
        Subscribe to this topic, The handle must only take one positional parameter which is the topic data
        :param handle:
        :param in_thread: Set to true to run this in a threadpool executor
        :return:
        """
        if in_thread:
            self.handles_executor[id(handle)] = (handle, parse_topic)
        else:
            self.handles_async[id(handle)] = (handle, parse_topic)

    def unsubscribe(self, handle):
        if isinstance(handle, partial):
            handle = partial.args[0]
        try:
            del self.handles_executor[id(handle)]
            return
        except KeyError:
            pass
        try:
            del self.handles_async[id(handle)]
            return
        except KeyError:
            pass
        raise ValueError(f"{handle} didn't exist in subscriptions")

    def wait(self, timeout):
        if pyaware.from_coroutine():
            return self._wait_async(timeout)
        else:
            return self._wait_sync(timeout)

    async def _wait_async(self, timeout):
        global _loop
        fut = _loop.create_future()
        self._waiters.append(fut)
        try:
            return await asyncio.wait_for(fut, timeout)
        finally:
            self._waiters.remove(fut)

    def last(self):
        return self._last

    def _wait_sync(self, timeout):
        global _loop
        fut = asyncio.run_coroutine_threadsafe(self._wait_async(timeout), _loop)
        return fut.result()

    def cancel(self):
        for fut in self._waiters:
            if not fut.done():
                fut.cancel()

    def delete(self):
        self.handles_executor.clear()
        self.handles_async.clear()
        self.cancel()

    def __del__(self):
        self.delete()

def publish(__topic: str, **data):
    """
    Publish data to a given topic.
    Key word only arguments for published data. Use data by convention to keep consistent across pub subs
    :param __topic:
    :param data:
    :return:
    """
    log.debug(f'Publishing {__topic}:{data}')
    futures = []
    if not _loop.is_running() or evt_stop.is_set():
        reset()
        raise StopException('Event loop is stopped, Raising error in all connected threads')
    for topic in tuple(_topics.keys()):
        if matches(__topic, topic):
            futures.extend(_topics[topic].publish(topic=__topic, **data))
    return TopicTasks(futures)

def _form_subscription_topic(topic):
    topic = topic.casefold()
    if '#' in topic and (not topic.endswith('#')):
        raise ValueError(f"Invalid topic {topic}, '#' wildcard must be last character")
    if topic != '+':
        if '+' in topic:
            if '/+' not in topic and '+/' not in topic:
                raise ValueError(f"Invalid topic {topic}, '+' wildcard must occupy an entire level")
    return topic

def subscribe(*handles, topic: str, in_thread=False, parse_topic=False):
    """
    Subscribe to a topic to call a handle when the event topic has some data published to it.
    Usage
    >>>data = "Hello"
    >>>def do_thing(data):
    >>>    print(data)
    >>>subscribe(do_thing, topic="test", in_thread=True)
    >>>@subscribe(topic="test")
    >>>def do_other_thing(data):
    >>>    print(f"Decorated {data}")
    >>>publish("test", data=data)
    >>>@enable
    >>>class TestThing:
    >>>    @subscribe(topic="test")
    >>>    def do_other_thing(self, data):
    >>>        print(f"Decorated method {data}")
    :param handle: Handles to execute
    :param topic: Topic as a string to subscribe to
    :param in_thread: If True, will execute the callback in an threadpool executor
    :return:
    """
    topic = _form_subscription_topic(topic)
    for handle in handles:
        log.info(f'Subscribing {topic}:{id(handle)}')
        _topics[_form_subscription_topic(topic)].subscribe(handle, in_thread, parse_topic)
    else:

        def _tmp(handle):
            param = None
            for param in inspect.signature(handle).parameters:
                break
            if param == 'self':
                handle.topic = topic
                handle.in_thread = in_thread
                handle.parse_topic = parse_topic
                return handle
            else:
                _topics[topic].subscribe(handle, in_thread, parse_topic)
                return handle
        return _tmp

def unsubscribe(topic, handle):
    """
    Removes subscription callbacks from a given topic. Does not remove tasks that are currently waiting on the topic
    :param topic:
    :param handle:
    :return:
    """
    return _topics[topic].unsubscribe(handle)

def enable(cls):
    """
    Creates a __new__ method on the class which subscribes to the topics on the functions when the class is instantiated
    :param cls:
    :return:
    """

    def __new__(cls, *args, **kwargs):
        inst = object.__new__(cls)
        log.debug(f'Calling __new__ on enabled {cls}')
        for attr in dir(inst):
            try:
                handle = getattr(inst, attr)
                _topics[handle.topic.format(id=id(inst))].subscribe(handle, handle.in_thread, handle.parse_topic)
                log.info(f'Subscribed to {handle.topic}:{id(handle)}')
            except AttributeError:
                pass
        return inst
    log.debug(f'Enabling {cls}')
    setattr(cls, '__new__', __new__)
    return cls

def reset():
    """
    Resets the events back to a fresh state and deletes all active topics. The next publish will create a new topic
    :return:
    """
    [topic.delete() for topic in _topics.values()]

def start(loop=None):
    """
    Starts the events by setting the event loop to the current event.
    Produces a runtime error if event loop is not currently running through asyncio.run()
    :return:
    """
    set_event_loop(loop or asyncio.get_running_loop())

def stop():
    """
    Causes all events to raise cancelled errors in all threads that are attempting to publish events
    :return:
    """
    evt_stop.set()

def delete(topic):
    """
    Cancels all waiting co-routines and removes all the subscriptions for a given topic
    :return:
    """
    for top in _topics:
        if matches(top, topic):
            _topics[top].delete()
            del _topics[top]

def cancel(topic):
    """
    Cancels all coroutines currently waiting for an event from the topic
    :param topic:
    :return:
    """
    for top in _topics:
        if matches(top, topic):
            _topics[top].cancel()

def wait(topic, timeout):
    """
    Waits until a topic to publish data. This will block from a thread and yield control from a co-routine
    :param topic: Topic name to wait for
    :param timeout: Time in seconds to wait before raising a TimeoutError
    :return:
    """
    return _topics[topic].wait(timeout)

def last(topic):
    return _topics[topic].last()

def set_event_loop(loop):
    """
    Sets the event loop to use for the events. Must be called at least once before events will work
    :param loop:
    :return:
    """
    global _loop
    _loop = loop
_loop = None
_topics = defaultdict(Topic)