import numpy as np

def get_didv(self, T=0.01, write=True, nsuper=1, **kwargs):
    from ..transporttk.localprobe import LocalProbe
    lp = LocalProbe(self, T=T, **kwargs)
    lp.reuse_gf = True
    g = lp.H.geometry.get_supercell(nsuper)
    Hc = lp.H.copy()
    lp.H = self.H.get_supercell(nsuper)
    lp.H.get_gf = lambda **kwargs: Hc.get_gf(nsuper=nsuper, **kwargs)
    Gs = []
    for i in range(len(g.r)):
        lp.i = i
        Gs.append(lp.didv(**kwargs))
    if write:
        np.savetxt('DIDV.OUT', np.array([g.r[:, 0], g.r[:, 1], np.array(Gs)]).T)
    return (g.r[:, 0], g.r[:, 1], np.array(Gs))