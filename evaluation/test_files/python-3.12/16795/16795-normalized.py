def watch_port_events(port, chip, pin_function_maps, event_queue, return_after_kbdint=False):
    """Waits for a port event. When a port event occurs it is placed onto the
    event queue.

    :param port: The port we are waiting for interrupts on (GPIOA/GPIOB).
    :type port: int
    :param chip: The chip we are waiting for interrupts on.
    :type chip: :class:`pifacecommon.mcp23s17.MCP23S17`
    :param pin_function_maps: A list of classes that have inheritted from
        :class:`FunctionMap`\\ s describing what to do with events.
    :type pin_function_maps: list
    :param event_queue: A queue to put events on.
    :type event_queue: :py:class:`multiprocessing.Queue`
    """
    gpio25 = open(GPIO_INTERRUPT_DEVICE_VALUE, 'r')
    epoll = select.epoll()
    epoll.register(gpio25, select.EPOLLIN | select.EPOLLET)
    while True:
        try:
            events = epoll.poll()
        except KeyboardInterrupt as e:
            if return_after_kbdint:
                return
            else:
                raise e
        except IOError as e:
            if e.errno != errno.EINTR:
                raise
        if port == pifacecommon.mcp23s17.GPIOA:
            interrupt_flag = chip.intfa.value
        else:
            interrupt_flag = chip.intfb.value
        if interrupt_flag == 0:
            continue
        else:
            if port == pifacecommon.mcp23s17.GPIOA:
                interrupt_capture = chip.intcapa.value
            else:
                interrupt_capture = chip.intcapb.value
            event_queue.add_event(InterruptEvent(interrupt_flag, interrupt_capture, chip, time.time()))
    epoll.close()