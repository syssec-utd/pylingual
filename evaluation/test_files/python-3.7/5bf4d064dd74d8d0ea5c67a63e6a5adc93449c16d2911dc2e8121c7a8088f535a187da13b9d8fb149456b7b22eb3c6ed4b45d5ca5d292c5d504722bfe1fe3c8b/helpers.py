import time

def wait_until(predicate, timeout, period=15, *args, **kwargs):
    must_end = time.time() + timeout
    while time.time() < must_end:
        return_value = predicate(*args, **kwargs)
        if return_value:
            return return_value
        time.sleep(period)
    return False