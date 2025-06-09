def finalize(self):
    """
        Resolve ports of discovered memories
        """
    ff_to_remove = 0
    res = self.resources
    for (m, addrDict) in self.memories.items():
        (rwSyncPorts, rSyncPorts, wSyncPorts) = (0, 0, 0)
        (rwAsyncPorts, rAsyncPorts, wAsyncPorts) = (0, 0, 0)
        (rSync_wAsyncPorts, rAsync_wSyncPorts) = (0, 0)
        for (_, (rSync, wSync, rAsync, wAsync)) in addrDict.items():
            if rSync:
                ff_to_remove += rSync * m._dtype.elmType.bit_length()
            rwSync = min(rSync, wSync)
            rSync -= rwSync
            wSync -= rwSync
            rwAsync = min(rAsync, wAsync)
            rAsync -= rwAsync
            wAsync -= rwAsync
            rSync_wAsync = min(rSync, wAsync)
            rSync -= rSync_wAsync
            wAsync -= rSync_wAsync
            rAsync_wSync = min(rAsync, wSync)
            rAsync -= rAsync_wSync
            wSync -= rAsync_wSync
            rwSyncPorts += rwSync
            rSyncPorts += rSync
            wSyncPorts += wSync
            rwAsyncPorts += rwAsync
            rAsyncPorts += rAsync
            wAsyncPorts += wAsync
            rSync_wAsyncPorts += rSync_wAsync
            rAsync_wSyncPorts += rAsync_wSync
        k = ResourceRAM(m._dtype.elmType.bit_length(), int(m._dtype.size), rwSyncPorts, rSyncPorts, wSyncPorts, rSync_wAsyncPorts, rwAsyncPorts, rAsyncPorts, wAsyncPorts, rAsync_wSyncPorts)
        res[k] = res.get(k, 0) + 1
    self.memories.clear()
    if ff_to_remove:
        ff_cnt = res[ResourceFF]
        ff_cnt -= ff_to_remove
        if ff_cnt:
            res[ResourceFF] = ff_cnt
        else:
            del res[ResourceFF]