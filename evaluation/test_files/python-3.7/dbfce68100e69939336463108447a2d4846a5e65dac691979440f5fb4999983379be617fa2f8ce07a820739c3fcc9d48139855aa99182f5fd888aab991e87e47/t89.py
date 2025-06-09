import numpy as np

def t89(iopt, ps, x, y, z):
    """
    Computes GSM components of the magnetic field produced by extra-
    terrestrial current systems in the geomagnetosphere. The model is
    valid up to geocentric distances of 70 Re and is based on the merged
    IMP-A,C,D,E,F,G,H,I,J (1966-1974), HEOS-1 and -2 (1969-1974),
    and ISEE-1 and -2  spacecraft data set.

    This is a modified version (t89c), which replaced the original one
    in 1992 and differs from it in the following:
    (1) ISEE-1,2 data were added to the original IMP-HEOS dataset
    (2) Two terms were added to the original tail field modes, allowing
        a modulation of the current by the geodipole tilt angle

    :param iopt: specifies the ground disturbance level:
        iopt= 1       2        3        4        5        6      7
                   correspond to:
        kp=  0,0+  1-,1,1+  2-,2,2+  3-,3,3+  4-,4,4+  5-,5,5+  &gt =6-
    :param ps: geo-dipole tilt angle in radius.
    :param x,y,z: GSM coordinates in Re (1 Re = 6371.2 km)
    :return: bx,by,bz. Field components in GSM system, in nT.

    Reference for the original model: N.A. Tsyganenko, A magnetospheric magnetic
        field model with a warped tail current sheet: planet.space sci., v.37, pp.5-20, 1989.

    This release of t89c is dated  Feb 12, 1996;
    Last update: May 9, 2006; a save statement was added in the subroutine t89c, to avoid runtime problems on some fortran compilers
    Author: Nikolai A. Tsyganenko, HSTX Corp./NASA GSFC
    """
    param = np.array([-116.53, -10719.0, 42.375, 59.753, -11363.0, 1.7844, 30.268, -0.035372, -0.066832, 0.016456, -1.3024, 0.0016529, 0.0020293, 20.289, -0.025203, 224.91, -9234.8, 22.788, 7.8813, 1.8362, -0.27228, 8.8184, 2.8714, 14.468, 32.177, 0.01, 0.0, 7.0459, 4.0, 20.0, -55.553, -13198.0, 60.647, 61.072, -16064.0, 2.2534, 34.407, -0.038887, -0.094571, 0.027154, -1.3901, 0.001346, 0.0013238, 23.005, -0.030565, 55.047, -3875.7, 20.178, 7.9693, 1.4575, 0.89471, 9.4039, 3.5215, 14.474, 36.555, 0.01, 0.0, 7.0787, 4.0, 20.0, -101.34, -13480.0, 111.35, 12.386, -24699.0, 2.6459, 38.948, -0.03408, -0.12404, 0.029702, -1.4052, 0.0012103, 0.0016381, 24.49, -0.037705, -298.32, 4400.9, 18.692, 7.9064, 1.3047, 2.4541, 9.7012, 7.1624, 14.288, 33.822, 0.01, 0.0, 6.7442, 4.0, 20.0, -181.69, -12320.0, 173.79, -96.664, -39051.0, 3.2633, 44.968, -0.046377, -0.16686, 0.048298, -1.5473, 0.0010277, 0.0031632, 27.341, -0.050655, -514.1, 12482.0, 16.257, 8.5834, 1.0194, 3.6148, 8.6042, 5.5057, 13.778, 32.373, 0.01, 0.0, 7.3195, 4.0, 20.0, -436.54, -9001.0, 323.66, -410.08, -50340.0, 3.9932, 58.524, -0.038519, -0.26822, 0.074528, -1.4268, -0.0010985, 0.0096613, 27.557, -0.056522, -867.03, 20652.0, 14.101, 8.3501, 0.72996, 3.8149, 9.2908, 6.4674, 13.729, 28.353, 0.01, 0.0, 7.4237, 4.0, 20.0, -707.77, -4471.9, 432.81, -435.51, -60400.0, 4.6229, 68.178, -0.088245, -0.21002, 0.11846, -2.6711, 0.0022305, 0.01091, 27.547, -0.05408, -424.23, 1100.2, 13.954, 7.5337, 0.89714, 3.7813, 8.2945, 5.174, 14.213, 25.237, 0.01, 0.0, 7.0037, 4.0, 20.0, -1190.4, 2749.9, 742.56, -1110.3, -77193.0, 7.6727, 102.05, -0.096015, -0.74507, 0.11214, -1.3614, 0.0015157, 0.022283, 23.164, -0.074146, -2219.1, 48253.0, 12.714, 7.6777, 0.57138, 2.9633, 9.3909, 9.7263, 11.123, 21.558, 0.01, 0.0, 4.4518, 4.0, 20.0])
    param = param.reshape((30, 7), order='F')
    id = 1
    a = param[:, iopt - 1]
    xi = np.array([x, y, z, ps])
    (bx, by, bz, der) = extern(id, a, xi)
    return (bx, by, bz)

def extern(id, a, xi):
    """
    Calculates dependent model variables and their derivatives
    for given independent variables and model parameters.
    Specifies model functions with free parameters which
    must be determined by means of least squares fits (RMS
    minimization procedure).

    :param id: number of the data point in a set (initial assignments are performed
        only for ID=1, saving thus CPU time)
    :param a: input vector containing model parameters
    :param xi: input vector containing independent variables
    :return: fx,fy,fz. Vector containing calculated values of dependent variables;
        der. Vector containing calculated values for derivatives
            of dependent variables with respect to model parameters;

    T89 represents external magnetospheric magnetic field in Cartesian SOLAR MAGNETOSPHERIC coordinates
    (Tsyganenko N.A., Planet. Space Sci., 1989, v.37, p.5-20; the "T89 model" with the warped
    tail current sheet) + a modification added in April 1992 (see below)

    Model formulas for the magnetic field components contain in total
    30 free parameters (17 linear and 13 nonlinear parameters).

    Linear parameters:
        a[0]-a[1]: correspond to contribution from the tail current system
        a[2]-a[3]: the amplitudes of symmetric and antisymmetric terms in the contribution from the closure currents
        a[4]: the ring current amplitude
        a[5]-a[14]: define Chapman-Ferraro+Birkeland current field.
            The coefficients c16-c19  (see Formula 20 in the original paper), due to DivB=0
            condition, are expressed through a[5]-a[14] and hence are not independent ones.
        a[15]-a[16]: the terms which yield the tilt angle dependence of the tail current intensity (added on April 9, 1992)

    Nonlinear parameters:
        a[17]: dx - characteristic scale of the Chapman-Ferraro field along the x-axis
        a[18]: ADR (aRC) - Characteristic radius of the ring current
        a[19] : D0 - Basic half-thickness of the tail current sheet
        a[20] : DD (GamRC)- defines rate of thickening of the ring current, as we go from night- to dayside
        a[21] : Rc - an analog of "hinging distance" entering formula (11)
        a[22] : G - amplitude of tail current warping in the Y-direction
        a[23] : aT - Characteristic radius of the tail current
        a[24] : Dy - characteristic scale distance in the Y direction entering in W(x,y) in (13)
        a[25] : Delta - defines the rate of thickening of the tail current sheet in the Y-direction (in T89 it was fixed at 0.01)
        a[26] : Q - this parameter was fixed at 0 in the final version of T89; initially it was introduced for making Dy to depend on X
        a[27] : Sx (Xo) - enters in W(x,y) ; see (13)
        a[28] : Gam (GamT) - enters in DT in (13) and defines rate of tail sheet thickening on going from night to dayside; in T89 fixed at 4.0
        a[29] : Dyc - the Dy parameter for closure current system; in T89 fixed at 20.0

    Author: N.A. Tsyganenko, Dec 8-10, 1991
    """
    (a02, xlw2, yn, rpi, rt) = [25.0, 170.0, 30.0, 0.31830989, 30.0]
    (xd, xld2) = [0.0, 40.0]
    (sxc, xlwc2) = [4.0, 50.0]
    dxl = 20.0
    der = np.zeros((3, 30))
    dyc = a[29]
    dyc2 = dyc ** 2
    dx = a[17]
    ha02 = 0.5 * a02
    rdx2m = -1.0 / dx ** 2
    rdx2 = -rdx2m
    rdyc2 = 1 / dyc2
    hlwc2m = -0.5 * xlwc2
    drdyc2 = -2 * rdyc2
    drdyc3 = 2 * rdyc2 * np.sqrt(rdyc2)
    hxlw2m = -0.5 * xlw2
    adr = a[18]
    d0 = a[19]
    dd = a[20]
    rc = a[21]
    g = a[22]
    at = a[23]
    dt = d0
    p = a[24]
    delt = a[25]
    q = a[26]
    sx = a[27]
    gam = a[28]
    hxld2m = -0.5 * xld2
    (adsl, xghs, h, hs, gamh) = [0.0] * 5
    dbldel = 2.0 * delt
    w1 = -0.5 / dx
    w2 = w1 * 2.0
    w4 = -1.0 / 3.0
    w3 = w4 / dx
    w5 = -0.5
    w6 = -3.0
    (ak1, ak2, ak3, ak4, ak5, ak6, ak7, ak8, ak9, ak10, ak11, ak12, ak13, ak14, ak15, ak16, ak17) = a[0:17]
    (sxa, sya, sza) = [0.0] * 3
    ak610 = ak6 * w1 + ak10 * w5
    ak711 = ak7 * w2 - ak11
    ak812 = ak8 * w2 + ak12 * w6
    ak913 = ak9 * w3 + ak13 * w4
    rdxl = 1.0 / dxl
    hrdxl = 0.5 * rdxl
    a6h = ak6 * 0.5
    a9t = ak9 / 3.0
    ynp = rpi / yn * 0.5
    ynd = 2.0 * yn
    (x, y, z, tilt) = xi[0:4]
    tlt2 = tilt ** 2
    sps = np.sin(tilt)
    cps = np.cos(tilt)
    x2 = x * x
    y2 = y * y
    z2 = z * z
    tps = sps / cps
    htp = tps * 0.5
    gsp = g * sps
    xsm = x * cps - z * sps
    zsm = x * sps + z * cps
    xrc = xsm + rc
    xrc16 = xrc ** 2 + 16
    sxrc = np.sqrt(xrc16)
    y4 = y2 * y2
    y410 = y4 + 10000.0
    sy4 = sps / y410
    gsy4 = g * sy4
    zs1 = htp * (xrc - sxrc)
    dzsx = -zs1 / sxrc
    zs = zs1 - gsy4 * y4
    d2zsgy = -sy4 / y410 * 40000.0 * y2 * y
    dzsy = g * d2zsgy
    xsm2 = xsm ** 2
    dsqt = np.sqrt(xsm2 + a02)
    fa0 = 0.5 * (1 + xsm / dsqt)
    ddr = d0 + dd * fa0
    dfa0 = ha02 / dsqt ** 3
    zr = zsm - zs
    tr = np.sqrt(zr ** 2 + ddr ** 2)
    rtr = 1 / tr
    ro2 = xsm2 + y2
    adrt = adr + tr
    adrt2 = adrt ** 2
    fk = 1 / (adrt2 + ro2)
    dsfc = np.sqrt(fk)
    fc = fk ** 2 * dsfc
    facxy = 3 * adrt * fc * rtr
    xzr = xsm * zr
    yzr = y * zr
    dbxdp = facxy * xzr
    der[1, 4] = facxy * yzr
    xzyz = xsm * dzsx + y * dzsy
    faq = zr * xzyz - ddr * dd * dfa0 * xsm
    dbzdp = fc * (2 * adrt2 - ro2) + facxy * faq
    der[0, 4] = dbxdp * cps + dbzdp * sps
    der[2, 4] = dbzdp * cps - dbxdp * sps
    dely2 = delt * y2
    d = dt + dely2
    if np.abs(gam) >= 1e-06:
        xxd = xsm - xd
        rqd = 1 / (xxd ** 2 + xld2)
        rqds = np.sqrt(rqd)
        h = 0.5 * (1 + xxd * rqds)
        hs = -hxld2m * rqd * rqds
        gamh = gam * h
        d = d + gamh
        xghs = xsm * gam * hs
        adsl = -d * xghs
    d2 = d ** 2
    t = np.sqrt(zr ** 2 + d2)
    xsmx = xsm - sx
    rdsq2 = 1 / (xsmx ** 2 + xlw2)
    rdsq = np.sqrt(rdsq2)
    v = 0.5 * (1 - xsmx * rdsq)
    dvx = hxlw2m * rdsq * rdsq2
    om = np.sqrt(np.sqrt(xsm2 + 16) - xsm)
    oms = -om / (om * om + xsm) * 0.5
    rdy = 1 / (p + q * om)
    omsv = oms * v
    rdy2 = rdy ** 2
    fy = 1 / (1 + y2 * rdy2)
    w = v * fy
    yfy1 = 2 * fy * y2 * rdy2
    fypr = yfy1 * rdy
    fydy = fypr * fy
    dwx = dvx * fy + fydy * q * omsv
    ydwy = -v * yfy1 * fy
    ddy = dbldel * y
    att = at + t
    s1 = np.sqrt(att ** 2 + ro2)
    f5 = 1 / s1
    f7 = 1 / (s1 + att)
    f1 = f5 * f7
    f3 = f5 ** 3
    f9 = att * f3
    fs = zr * xzyz - d * y * ddy + adsl
    xdwx = xsm * dwx + ydwy
    rtt = 1 / t
    wt = w * rtt
    brrz1 = wt * f1
    brrz2 = wt * f3
    dbxc1 = brrz1 * xzr
    dbxc2 = brrz2 * xzr
    der[1, 0] = brrz1 * yzr
    der[1, 1] = brrz2 * yzr
    der[1, 15] = der[1, 0] * tlt2
    der[1, 16] = der[1, 1] * tlt2
    wtfs = wt * fs
    dbzc1 = w * f5 + xdwx * f7 + wtfs * f1
    dbzc2 = w * f9 + xdwx * f1 + wtfs * f3
    der[0, 0] = dbxc1 * cps + dbzc1 * sps
    der[0, 1] = dbxc2 * cps + dbzc2 * sps
    der[2, 0] = dbzc1 * cps - dbxc1 * sps
    der[2, 1] = dbzc2 * cps - dbxc2 * sps
    der[0, 15] = der[0, 0] * tlt2
    der[0, 16] = der[0, 1] * tlt2
    der[2, 15] = der[2, 0] * tlt2
    der[2, 16] = der[2, 1] * tlt2
    zpl = z + rt
    zmn = z - rt
    rogsm2 = x2 + y2
    spl = np.sqrt(zpl ** 2 + rogsm2)
    smn = np.sqrt(zmn ** 2 + rogsm2)
    xsxc = x - sxc
    rqc2 = 1 / (xsxc ** 2 + xlwc2)
    rqc = np.sqrt(rqc2)
    fyc = 1 / (1 + y2 * rdyc2)
    wc = 0.5 * (1 - xsxc * rqc) * fyc
    dwcx = hlwc2m * rqc2 * rqc * fyc
    dwcy = drdyc2 * wc * fyc * y
    szrp = 1 / (spl + zpl)
    szrm = 1 / (smn - zmn)
    xywc = x * dwcx + y * dwcy
    wcsp = wc / spl
    wcsm = wc / smn
    fxyp = wcsp * szrp
    fxym = wcsm * szrm
    fxpl = x * fxyp
    fxmn = -x * fxym
    fypl = y * fxyp
    fymn = -y * fxym
    fzpl = wcsp + xywc * szrp
    fzmn = wcsm + xywc * szrm
    der[0, 2] = fxpl + fxmn
    der[0, 3] = (fxpl - fxmn) * sps
    der[1, 2] = fypl + fymn
    der[1, 3] = (fypl - fymn) * sps
    der[2, 2] = fzpl + fzmn
    der[2, 3] = (fzpl - fzmn) * sps
    ex = np.exp(x / dx)
    ec = ex * cps
    es = ex * sps
    ecz = ec * z
    esz = es * z
    eszy2 = esz * y2
    eszz2 = esz * z2
    ecz2 = ecz * z
    esy = es * y
    der[0, 5] = ecz
    der[0, 6] = es
    der[0, 7] = esy * y
    der[0, 8] = esz * z
    der[1, 9] = ecz * y
    der[1, 10] = esy
    der[1, 11] = esy * y2
    der[1, 12] = esy * z2
    der[2, 13] = ec
    der[2, 14] = ec * y2
    der[2, 5] = ecz2 * w1
    der[2, 9] = ecz2 * w5
    der[2, 6] = esz * w2
    der[2, 10] = -esz
    der[2, 7] = eszy2 * w2
    der[2, 11] = eszy2 * w6
    der[2, 8] = eszz2 * w3
    der[2, 12] = eszz2 * w4
    sx1 = ak6 * der[0, 5] + ak7 * der[0, 6] + ak8 * der[0, 7] + ak9 * der[0, 8]
    sy1 = ak10 * der[1, 9] + ak11 * der[1, 10] + ak12 * der[1, 11] + ak13 * der[1, 12]
    sz1 = ak14 * der[2, 13] + ak15 * der[2, 14] + ak610 * ecz2 + ak711 * esz + ak812 * eszy2 + ak913 * eszz2
    bxcl = ak3 * der[0, 2] + ak4 * der[0, 3]
    bycl = ak3 * der[1, 2] + ak4 * der[1, 3]
    bzcl = ak3 * der[2, 2] + ak4 * der[2, 3]
    bxt = ak1 * der[0, 0] + ak2 * der[0, 1] + bxcl + ak16 * der[0, 15] + ak17 * der[0, 16]
    byt = ak1 * der[1, 0] + ak2 * der[1, 1] + bycl + ak16 * der[1, 15] + ak17 * der[1, 16]
    bzt = ak1 * der[2, 0] + ak2 * der[2, 1] + bzcl + ak16 * der[2, 15] + ak17 * der[2, 16]
    fx = bxt + ak5 * der[0, 4] + sx1 + sxa
    fy = byt + ak5 * der[1, 4] + sy1 + sya
    fz = bzt + ak5 * der[2, 4] + sz1 + sza
    return (fx, fy, fz, der)