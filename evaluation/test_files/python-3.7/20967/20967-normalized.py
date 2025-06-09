def virtual_memory():
    """System virtual memory as a namedtuple."""
    (total, active, inactive, wired, free) = _psutil_osx.get_virtual_mem()
    avail = inactive + free
    used = active + inactive + wired
    percent = usage_percent(total - avail, total, _round=1)
    return nt_virtmem_info(total, avail, percent, used, free, active, inactive, wired)