import numpy as np
import scipy.linalg as lg
import scipy.sparse.linalg as slg
import os
from .operators import operator2list
from . import operators
from . import parallel
from . import kpm
from . import timing
from . import algebra
from . import densitymatrix
from .fermisurface import multi_fermi_surface
arpack_tol = 1e-05
arpack_maxiter = 10000

def fermi_surface(h, write=True, output_file='FERMI_MAP.OUT', e=0.0, nk=50, nsuper=1, reciprocal=True, delta=None, refine_delta=1.0, operator=None, mode='eigen', num_waves=2, info=False):
    """Calculates the Fermi surface of a 2d system"""
    if operator is not None:
        operator = h.get_operator(operator)
        if not operator.linear:
            if mode == 'full':
                mode = 'eigen'
    elif mode == 'full':
        operator = np.matrix(np.identity(h.intra.shape[0]))
    if h.dimensionality != 2:
        raise
    hk_gen = h.get_hk_gen()
    kxs = np.linspace(-nsuper, nsuper, nk)
    kys = np.linspace(-nsuper, nsuper, nk)
    iden = np.identity(h.intra.shape[0], dtype=np.complex)
    kxout = []
    kyout = []
    if reciprocal:
        R = h.geometry.get_k2K_generator()
    else:
        R = lambda x: x
    if delta is None:
        delta = 3.0 / refine_delta * 2.0 / nk
    if mode == 'full':

        def get_weight(hk, k=None):
            gf = algebra.inv((e + 1j * delta) * iden - hk)
            gf = gf - algebra.inv((e - 1j * delta) * iden - hk)
            if callable(operator):
                tdos = -operator(gf, k=k).imag
            else:
                tdos = -(operator * gf).imag
            return np.trace(tdos).real
    elif mode == 'eigen':

        def get_weight(hk, k=None):
            if operator is None:
                es = algebra.eigvalsh(hk)
                return np.sum(delta / ((e - es) ** 2 + delta ** 2))
            else:
                tmp, ds = h.get_dos(ks=[k], operator=operator, energies=[e], delta=delta)
                return ds[0]
    elif mode == 'lowest':

        def get_weight(hk, **kwargs):
            es, waves = slg.eigsh(hk, k=num_waves, sigma=e, tol=arpack_tol, which='LM', maxiter=arpack_maxiter)
            return np.sum(delta / ((e - es) ** 2 + delta ** 2))
    else:
        raise
    rs = []
    for x in kxs:
        for y in kxs:
            rs.append([x, y, 0.0])

    def getf(r):
        k = R(r)
        hk = hk_gen(k)
        return get_weight(hk, k=k)
    rs = np.array(rs)
    from . import parallel
    kxout = rs[:, 0]
    kyout = rs[:, 1]
    if parallel.cores == 1:
        if info:
            ts = timing.Testimator(maxite=len(kxs) * len(kys), title='FS')
        kdos = []
        for r in rs:
            if info:
                ts.iterate()
            kdos.append(getf(r))
    else:
        kdos = parallel.pcall(getf, rs)
    if write:
        f = open(output_file, 'w')
        for x, y, d in zip(kxout, kyout, kdos):
            f.write(str(x) + '   ' + str(y) + '   ' + str(d) + '\n')
        f.close()
    return (kxout, kyout, np.array(kdos))

def boolean_fermi_surface(h, write=True, output_file='BOOL_FERMI_MAP.OUT', e=0.0, nk=50, nsuper=1, reciprocal=False, delta=None):
    """Calculates the Fermi surface of a 2d system"""
    if h.dimensionality != 2:
        raise
    hk_gen = h.get_hk_gen()
    kxs = np.linspace(-nsuper, nsuper, nk)
    kys = np.linspace(-nsuper, nsuper, nk)
    kdos = []
    kxout = []
    kyout = []
    if reciprocal:
        R = h.geometry.get_k2K()
    if delta is None:
        delta = 8.0 / np.max(np.abs(h.intra)) / nk
    for x in kxs:
        for y in kxs:
            r = np.matrix([x, y, 0.0]).T
            k = np.array((R * r).T)[0]
            hk = hk_gen(k)
            evals = lg.eigvalsh(hk)
            de = np.abs(evals - e)
            de = de[de < delta]
            if len(de) > 0:
                kdos.append(1.0)
            else:
                kdos.append(0.0)
            kxout.append(x)
            kyout.append(y)
    if write:
        f = open(output_file, 'w')
        for x, y, d in zip(kxout, kyout, kdos):
            f.write(str(x) + '   ' + str(y) + '   ' + str(d) + '\n')
        f.close()
    return (kxout, kyout, d)
from .bandstructure import braket_wAw

def selected_bands2d(h, output_file='BANDS2D_', nindex=[-1, 1], nk=50, nsuper=1, reciprocal=True, operator=None, k0=[0.0, 0.0]):
    """ Calculate a selected bands in a 2d Hamiltonian"""
    if h.dimensionality != 2:
        raise
    hk_gen = h.get_hk_gen()
    kxs = np.linspace(-nsuper, nsuper, nk) + k0[0]
    kys = np.linspace(-nsuper, nsuper, nk) + k0[1]
    kdos = []
    kxout = []
    kyout = []
    if reciprocal:
        R = h.geometry.get_k2K()
    else:
        R = np.array(np.identity(3))
    operator = operator2list(operator)
    os.system('rm -f ' + output_file + '*')
    fo = [open(output_file + '_' + str(i) + '.OUT', 'w') for i in nindex]
    for x in kxs:
        for y in kxs:
            r = np.array([x, y, 0.0])
            k = np.array(R) @ r
            hk = hk_gen(k)
            if not h.is_sparse:
                evals, waves = lg.eigh(hk)
            else:
                evals, waves = slg.eigsh(hk, k=max(np.abs(nindex)) * 2, sigma=0.0, tol=arpack_tol, which='LM')
            waves = waves.transpose()
            epos, wfpos = ([], [])
            eneg, wfneg = ([], [])
            for e, w in zip(evals, waves):
                if e > 0.0:
                    epos.append(e)
                    wfpos.append(w)
                else:
                    eneg.append(e)
                    wfneg.append(w)
            wfpos = [yy for xx, yy in sorted(zip(epos, wfpos))]
            wfneg = [yy for xx, yy in sorted(zip(-np.array(eneg), wfneg))]
            epos = sorted(epos)
            eneg = -np.array(sorted(-np.array(eneg)))
            for i, j in zip(nindex, range(len(nindex))):
                fo[j].write(str(x) + '     ' + str(y) + '   ')
                if i > 0:
                    fo[j].write(str(epos[i - 1]) + '  ')
                    for op in operator:
                        c = op.braket(wfpos[i - 1]).real
                        fo[j].write(str(c) + '  ')
                    fo[j].write('\n')
                if i < 0:
                    fo[j].write(str(eneg[abs(i) - 1]) + '\n')
                    for op in operator:
                        c = op.braket(wfpos[abs(i) - 1]).real
                        fo[j].write(str(c) + '  ')
                    fo[j].write('\n')
    [f.close() for f in fo]
get_bands = selected_bands2d

def ev2d(h, nk=50, nsuper=1, reciprocal=False, operator=None, k0=[0.0, 0.0], kreverse=False):
    """ Calculate the expectation value of a certain operator"""
    if h.dimensionality != 2:
        raise
    hk_gen = h.get_hk_gen()
    kxs = np.linspace(-nsuper, nsuper, nk, endpoint=True) + k0[0]
    kys = np.linspace(-nsuper, nsuper, nk, endpoint=True) + k0[1]
    if kreverse:
        kxs, kys = (-kxs, -kys)
    kdos = []
    kxout = []
    kyout = []
    if reciprocal:
        R = h.geometry.get_k2K()
    else:
        R = np.matrix(np.identity(3))
    operator = operator2list(operator)
    fo = open('EV2D.OUT', 'w')
    for x in kxs:
        for y in kxs:
            print('Doing', x, y)
            r = np.matrix([x, y, 0.0]).T
            k = np.array((R * r).T)[0]
            hk = hk_gen(k)
            if not h.is_sparse:
                evals, waves = lg.eigh(hk)
            else:
                evals, waves = slg.eigsh(hk, k=max(nindex) * 2, sigma=0.0, tol=arpack_tol, which='LM')
            waves = waves.transpose()
            eneg, wfneg = ([], [])
            for e, w in zip(evals, waves):
                if e < 0:
                    eneg.append(e)
                    wfneg.append(w)
            fo.write(str(x) + '     ' + str(y) + '   ')
            for op in operator:
                c = sum([braket_wAw(w, op) for w in wfneg]).real
                fo.write(str(c) + '  ')
            fo.write('\n')
    fo.close()

def ev(h, operator=None, nk=30, **kwargs):
    """Calculate the expectation value of a certain number of operators"""
    dm = densitymatrix.full_dm(h, nk=nk, **kwargs)
    if operator is None:
        operator = []
    elif not isinstance(operator, list):
        operator = [operator]
    out = [np.trace(dm @ op) for op in operator]
    out = np.array(out)
    out = out.reshape(out.shape[0])
    return out

def real_space_vev(h, operator=None, nk=1, nrep=3, name='REAL_SPACE_VEV.OUT', **kwargs):
    """Compute the expectation value in real space"""
    if nk > 1:
        raise
    dm = densitymatrix.full_dm(h, nk=nk, **kwargs)
    operator = operators.Operator(operator)
    rho = operator(dm, k=[0.0, 0.0, 0.0])
    rho = np.diag(rho).real
    rho = h.full2profile(rho)
    h.geometry.write_profile(rho, nrep=5, name=name)
    return rho

def total_energy(h, nk=10, nbands=None, use_kpm=False, random=False, kp=None, mode='mesh', tol=0.1, fermi=0.0):
    """Return the total energy"""
    if nbands is None:
        h.turn_dense()
    if h.is_sparse and (not use_kpm):
        if nbands is None:
            print('Sparse Hamiltonian but no bands given, taking 20')
            nbands = 20
    f = h.get_hk_gen()
    etot = 0.0
    iv = 0

    def enek(k):
        """Compute energy in this kpoint"""
        hk = f(k)
        if use_kpm:
            return kpm.total_energy(hk, scale=10.0, ntries=20, npol=100)
        else:
            if nbands is None:
                vv = algebra.eigvalsh(hk)
            else:
                vv, aa = slg.eigsh(hk, k=4 * nbands, which='LM', sigma=0.0)
                vv = -np.sort(-vv[vv < fermi])
                vv = vv[0:nbands]
            return np.sum(vv[vv < fermi])
    if mode == 'mesh':
        from .klist import kmesh
        kp = kmesh(h.dimensionality, nk=nk)
        etot = np.mean(parallel.pcall(enek, kp))
    elif mode == 'random':
        kp = [np.random.random(3) for i in range(nk)]
        etot = np.mean(parallel.pcall(enek, kp))
    elif mode == 'integrate':
        from scipy import integrate
        if h.dimensionality == 1:
            etot = integrate.quad(enek, -1.0, 1.0, epsabs=tol, epsrel=tol)[0]
        elif h.dimensionality == 2:
            etot = integrate.dblquad(lambda x, y: enek([x, y]), -1.0, 1.0, -1.0, 1.0, epsabs=tol, epsrel=tol)[0]
        else:
            raise
    else:
        raise
    return etot

def eigenvalues(h0, nk=10, notime=True):
    """Return all the eigenvalues of a Hamiltonian"""
    from . import klist
    h = h0.copy()
    h.turn_dense()
    ks = klist.kmesh(h.dimensionality, nk=nk)
    hkgen = h.get_hk_gen()
    if parallel.cores == 1:
        es = []
        if not notime:
            est = timing.Testimator(maxite=len(ks))
        for k in ks:
            if not notime:
                est.iterate()
            es += algebra.eigvalsh(hkgen(k)).tolist()
    else:
        f = lambda k: algebra.eigvalsh(hkgen(k))
        es = parallel.pcall(f, ks)
        es = np.array(es)
        es = es.reshape(es.shape[0] * es.shape[1])
    return es

def reciprocal_map(h, f, nk=40, reciprocal=True, nsuper=1, filename='MAP.OUT', write=True, verbosity=0, grid=False):
    """ Calculates the reciprocal map of something"""
    if reciprocal:
        fR = h.geometry.get_k2K_generator()
    else:
        fR = lambda x: x
    if write:
        fo = open(filename, 'w')
    nt = nk * nk
    ik = 0
    ks = []
    from . import parallel
    for x in np.linspace(-nsuper, nsuper, nk, endpoint=False):
        for y in np.linspace(-nsuper, nsuper, nk, endpoint=False):
            ks.append([x, y, 0.0])
    ks = np.array(ks)
    tr = timing.Testimator(filename.replace('.OUT', ''), maxite=len(ks), silent=verbosity == 0)

    def fp(ki):
        if parallel.cores == 1:
            tr.iterate()
        else:
            print('Doing', ki)
        k = fR(ki)
        return f(k)
    bs = np.array(parallel.pcall(fp, ks))
    if write:
        for b, k in zip(bs, ks):
            fo.write(str(k[0]) + '   ' + str(k[1]) + '     ' + str(b.real))
            fo.write('     ' + str(b.imag) + '\n')
            fo.flush()
        fo.close()
    if grid:
        from .interpolation import points2grid
        kx, ky, bs = points2grid(ks[:, 0], ks[:, 1], bs, n=int(np.sqrt(len(bs))))
        ks = np.array([kx, ky])
    return (ks, bs)

def singlet_map(h, nk=40, nsuper=3, mode='abs'):
    """Compute a map with the superconducting singlet pairing"""
    hk = h.get_hk_gen()
    from .superconductivity import extract_pairing

    def f(k):
        m = hk(k)
        uu, dd, ud = extract_pairing(m)
        if mode == 'trace':
            return ud.trace()[0, 0]
        elif mode == 'det':
            return np.linalg.det(ud)
        elif mode == 'abs':
            return np.sum(np.abs(ud))
    reciprocal_map(h, f, nk=nk, nsuper=nsuper, filename='SINGLET_MAP.OUT')

def pairing_map(h, **kwargs):
    """Compute a map with the superconducting singlet pairing"""
    h0 = h.copy()
    h0.remove_nambu()
    h0.setup_nambu_spinor()
    h = h - h0
    hk = h.get_hk_gen()

    def f(k):
        m = hk(k)
        es = algebra.eigvalsh(m)
        return np.max(np.abs(es))
    reciprocal_map(h, f, filename='PAIRING_MAP.OUT', **kwargs)

def set_filling(h, filling=0.5, nk=10, extrae=0.0, mode='ED', **kwargs):
    """
    Set the filling of a Hamiltonian
    - nk = 10, number of kpoints in each direction
    - filling = 0.5, filling of the lattice
    - extrae = 0.0, number of extra electrons
    """
    if h.has_eh:
        ef = h.get_fermi4filling(filling, nk=nk)
        h.add_onsite(-ef)
        return
    fill = filling + extrae / h.intra.shape[0]
    n = h.intra.shape[0]
    use_kpm = False
    if n > algebra.maxsize:
        mode = 'KPM'
        print('Using KPM in set_filling')
    if mode == 'KPM':
        es, ds = h.get_dos(energies=np.linspace(-5.0, 5.0, 1000), mode='KPM', nk=nk, **kwargs)
        from scipy.integrate import cumtrapz
        di = cumtrapz(ds, es)
        ei = (es[0:len(es) - 1] + es[1:len(es)]) / 2.0
        di /= di[len(di) - 1]
        from scipy.interpolate import interp1d
        f = interp1d(di, ei)
        efermi = f(fill)
    elif mode == 'ED':
        es = eigenvalues(h, nk=nk, notime=True)
        efermi = get_fermi_energy(es, fill)
    else:
        raise
    h.shift_fermi(-efermi)

def get_fermi_energy(es, filling, fermi_shift=0.0):
    """Return the Fermi energy"""
    ne = len(es)
    ifermi = int(round(ne * filling))
    if ifermi >= ne:
        ifermi = ne - 1
    sorte = np.sort(es)
    if ifermi == 0:
        return sorte[0] + fermi_shift
    fermi = (sorte[ifermi - 1] + sorte[ifermi]) / 2.0 + fermi_shift
    return fermi

def get_fermi4filling(h, filling, nk=8):
    """Return the fermi energy for a certain filling"""
    if h.has_eh:
        h0 = h.copy()
        h0.remove_nambu()
        return get_fermi4filling(h0, filling, nk=nk)
    else:
        es = eigenvalues(h, nk=nk, notime=True)
        return get_fermi_energy(es, filling)

def get_filling(h, **kwargs):
    """Get the filling of a Hamiltonian at this energy"""
    if h.check_mode('spinless_nambu'):
        from .sctk import spinless
        return spinless.get_filling(h, **kwargs)
    elif h.check_mode('spinful_nambu'):
        raise
    else:
        es = eigenvalues(h, **kwargs)
        es = np.array(es)
        esf = es[es < 0.0]
        return len(esf) / len(es)

def eigenvalues_kmesh(h, nk=20):
    """Get the eigenvalues in a kmesh"""
    if h.dimensionality != 2:
        raise
    ne = h.intra.shape[0]
    es = np.zeros((nk, nk, ne))
    hkgen = h.get_hk_gen()
    kx = np.linspace(0.0, 1.0, nk, endpoint=False)
    ky = np.linspace(0.0, 1.0, nk, endpoint=False)
    for i in range(nk):
        ik = kx[i]
        for j in range(nk):
            jk = ky[j]
            hk = hkgen([ik, jk])
            ei = algebra.eigvalsh(hk)
            es[i, j, :] = ei
    return es

def lowest_energies(h, n=4, k=None, **kwargs):
    """Return the lowest energy states in a k-point"""
    if k is None:
        raise
    es, ws = h.get_eigenvectors(kpoints=False, k=k, numw=2 * n, **kwargs)
    es = [y for x, y in sorted(zip(np.abs(es), es))][0:n]
    es = np.sort(es)
    return es

def get_bandwidth(self, **kwargs):
    """Return the bandwidth of the Hamiltonian"""
    from .gap import optimize_energy
    self.turn_dense()
    emin = optimize_energy(self, mode='bottom', **kwargs)
    emax = optimize_energy(self, mode='top', **kwargs)
    return (emin, emax)