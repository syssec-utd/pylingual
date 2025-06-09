def oscilate(sig, period=10 * Time.ns, initWait=0):
    """
    Oscillative simulation driver for your signal
    (usually used as clk generator)
    """

    def oscillateStimul(s):
        s.write(False, sig)
        halfPeriod = period / 2
        yield s.wait(initWait)
        while True:
            yield s.wait(halfPeriod)
            s.write(True, sig)
            yield s.wait(halfPeriod)
            s.write(False, sig)
    return oscillateStimul