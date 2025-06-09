"""
Defines the command line interface to "irrep".
"""
import sys
import numpy as np
import datetime
import math
import click
from monty.serialization import dumpfn, loadfn
from .spacegroup import SpaceGroup
from .bandstructure import BandStructure
from .utility import str2bool, str2list, short
from . import __version__ as version

class LoadContextFromConfig(click.Command):
    """
    Custom class to allow supplying command context from an
    input file. Thanks to https://stackoverflow.com/a/46391887
    for concept.
    """

    def invoke(self, ctx):
        config_file = ctx.params['config']
        if config_file is not None:
            config_data = loadfn(config_file)
            config_data = {k.lower(): v for k, v in config_data.items()}
            for param, value in ctx.params.items():
                if param in config_data:
                    ctx.params[param] = config_data[param]
        return super(LoadContextFromConfig, self).invoke(ctx)

@click.version_option(version)
@click.command(cls=LoadContextFromConfig, help='\n\n\x08\n            # ###   ###   #####  ###\n            # #  #  #  #  #      #  #\n            # ###   ###   ###    ###\n            # #  #  #  #  #      #\n            # #   # #   # #####  #\n\n\x08\nversion {version}\n\x08\nCalculates the expectation values of symmetry operations \n<Psi_nk | T(g) | Psi_nk >  as well as irreducible representations,\nWannier charge centers (1D) Zak phases and many more.\n\n\x08\nExamples:\nirrep -Ecut=50 -code=abinit -fWFK=Bi_WFK -refUC=0,-1,1,1,0,-1,-1,-1,-1 -kpoints=11 -IBend=5 -kpnames="GM" \nirrep -Ecut=50 -code=espresso -prefix=Bi -refUC=0,-1,1,1,0,-1,-1,-1,-1 -kpoints=11 -IBend=5 -kpnames="GM" \n\nIf you have interest in the code and not sure how to use it, \ndo not hesitate to contact the author:\n\n\x08\n> Stepan S. Tsirkin  \n> University of Zurich  \n> stepan.tsirkin@physik.uzh.ch\n'.format(version=version))
@click.option('-Ecut', type=float, help='Energy cut-off in eV used in the calculation. A value of 50 eV is recommended. If not set, will default to the cut-off used in the DFT calculation.')
@click.option('-fWAV', type=str, default='WAVECAR', help='Filename for wavefunction in VASP WAVECAR format. Only used if code is "vasp".')
@click.option('-fPOS', type=str, default='POSCAR', help='Filename for wavefunction in VASP POSCAR format. Only used if code is "vasp".')
@click.option('-fWFK', type=str, help='Filename for wavefunction in ABINIT WFK format. Only used if code is "abinit".')
@click.option('-prefix', type=str, help='Prefix used for Quantum Espresso calculations (data should be in prefix.save) or seedname of Wannier90 files. ')
@click.option('-IBstart', type=int, default=0, help='The first band to be considered. If <= 0 starting from the lowest band (count from one).')
@click.option('-IBend', type=int, default=0, help='The last band to be considered. If <=0 up to  the highest band (count from one).')
@click.option('-code', type=click.Choice(['vasp', 'abinit', 'espresso', 'wannier90']), default='vasp', help='Set which electronic structure code to interface with. If using ABINIT, always use "istwfk=1".')
@click.option('-spinor', flag_value=True, default=False, help='Indicate the wavefunctions are spinor. Only used if code is "vasp".')
@click.option('-kpoints', type=str, help='Comma-separated list of k-point indices (starting from 1).')
@click.option('-kpnames', type=str, default=None, help='Comma-separated list of k-point names (as in the tables) with one entry per each value in the k-points list. Important! K-points is assumed to be an ordered list!')
@click.option('-refUC', type=str, default=None, help='The lattice vectors of the reference unit cell (as given in the crystallographic tables) expressed in terms of the unit cell vectors used in the calculation. Nine comma-separated numbers.')
@click.option('-shiftUC', type=str, default=None, help='The vector to shift the calculated unit cell origin (in units of the calculated lattice), to get the unit cell as defined in crystallographic tables. Three comma-separated numbers.')
@click.option('-isymsep', help='Index of the symmetry to separate the eigenstates. Works well only for norm-conserving potentials as in ABINIT.')
@click.option('-onlysym', flag_value=True, default=False, help='Only calculate the symmetry operations')
@click.option('-ZAK', flag_value=True, default=False, help='Calculate Zak phase')
@click.option('-WCC', flag_value=True, default=False, help='Calculate Wannier charge centres')
@click.option('-plotbands', flag_value=True, default=False, help='Write gnuplottable files with all symmetry eigenvalues')
@click.option('-plotFile', type=str, help='file where bands for plotting will be written.In development...!')
@click.option('-EF', type=str, default='0.0', help="Fermi energy to shift energy-levels. Default: 0.0. If it is set to a number, this value will be used to shift the energy-levels. If it is set to 'auto', the code will try to parse it from DFT files and set it to 0.0 if it could not do so.")
@click.option('-degenThresh', type=float, default=0.0001, help='Threshold to decide whether energy-levels are degenerate. Default: 1e-4')
@click.option('-groupKramers', flag_value=True, default=True, help='Group wave-functions in pairs of Kramers. Default: True.')
@click.option('-symmetries', type=str, help='Indices of symmetries to be printed. Default: all detected symmetries.')
@click.option('-suffix', type=str, default='tognuplot', help='Suffix to name files containing data for band plotting. Default: tognuplot')
@click.option('-config', type=click.Path(), help='Define irrep inputs from a configuration file in YAML or JSON format.')
def cli(ecut, fwav, fpos, fwfk, prefix, ibstart, ibend, code, spinor, kpoints, kpnames, refuc, shiftuc, isymsep, onlysym, zak, wcc, plotbands, plotfile, ef, degenthresh, groupkramers, symmetries, suffix, config):
    """
    Defines the "irrep" command-line tool interface.
    """
    if refuc:
        refuc = np.array(refuc.split(','), dtype=float).reshape((3, 3))
    if shiftuc:
        shiftuc = np.array(shiftuc.split(','), dtype=float).reshape(3)
    if kpnames is None:
        identify_irreps = False
        print('Warning: kpnames not specified. Only traces of symmetry operations will be calculated. Remember that kpnames must be specified to identify irreps')
    else:
        identify_irreps = True
    if symmetries:
        symmetries = str2list(symmetries)
    if kpoints:
        kpoints = str2list(kpoints)
    if isymsep:
        isymsep = str2list(isymsep)
    if kpnames:
        kpnames = kpnames.split(',')
    try:
        print(fwfk.split('/')[0].split('-'))
        preline = ' '.join((s.split('_')[1] for s in fwfk.split('/')[0].split('-')[:3]))
    except Exception as err:
        print(err)
        preline = ''
    json_data = {}
    bandstr = BandStructure(fWAV=fwav, fWFK=fwfk, prefix=prefix, fPOS=fpos, Ecut=ecut, IBstart=ibstart, IBend=ibend, kplist=kpoints, spinor=spinor, code=code, EF=ef, onlysym=onlysym, refUC=refuc, shiftUC=shiftuc, identify_irreps=identify_irreps)
    json_data['spacegroup'] = bandstr.spacegroup.show(symmetries=symmetries)
    if onlysym:
        exit()
    with open('irreptable-template', 'w') as f:
        f.write(bandstr.spacegroup.str())
    subbands = {(): bandstr}
    if isymsep is not None:
        json_data['separated by symmetry'] = True
        json_data['separating symmetries'] = isymsep
        for isym in isymsep:
            print('Separating by symmetry operation # ', isym)
            subbands = {tuple(list(s_old) + [s_new]): sub for s_old, bands in subbands.items() for s_new, sub in bands.Separate(isym, degen_thresh=degenthresh, groupKramers=groupkramers).items()}
    else:
        json_data['separated by symmetry'] = False
    if zak:
        for k in subbands:
            print('symmetry eigenvalue : {0} \n Traces are : '.format(k))
            subbands[k].write_characters(degen_thresh=0.001, symmetries=symmetries)
            print('symmetry eigenvalue : {0} \n Zak phases are : '.format(k))
            zak = subbands[k].zakphase()
            for n, (z, gw, gc, lgw) in enumerate(zip(*zak)):
                print('   {n:4d}    {z:8.5f} pi gapwidth = {gap:8.4f} gapcenter = {cent:8.3f} localgap= {lg:8.4f}'.format(n=n + 1, z=z / np.pi, gap=gw, cent=gc, lg=lgw))
            exit()
    if wcc:
        for k in subbands:
            print('symmetry eigenvalue {0}'.format(k))
            wcc = subbands[k].wcc()
            print('symmetry eigenvalue : {0} \n  WCC are : {1} \n sumWCC={2}'.format(k, wcc, np.sum(wcc) % 1))
        exit()
    bandstr.write_trace(degen_thresh=degenthresh, symmetries=symmetries)
    json_data['characters_and_irreps'] = []
    for k, sub in subbands.items():
        if isymsep is not None:
            print('\n\n\n\n ################################################ \n\n\n next subspace:  ', ' , '.join(('{0}:{1}'.format(s, short(ev)) for s, ev in zip(isymsep, k))))
        plotfile = None
        characters = sub.write_characters(degen_thresh=degenthresh, symmetries=symmetries, kpnames=kpnames, preline=preline, plotFile=plotfile)
        json_data['characters_and_irreps'].append({'symmetry_eigenvalues': k, 'subspace': characters})
    if plotbands:
        json_data['characters_and_irreps'] = {}
        print('plotbands = True --> writing bands')
        for k, sub in subbands.items():
            if isymsep is not None:
                print('\n\n\n\n ################################################ \n\n\n next subspace:  ', ' , '.join(('{0}:{1}'.format(s, short(ev)) for s, ev in zip(isymsep, k))))
                fname = 'bands-' + suffix + '-' + '-'.join(('{0}:{1}'.format(s, short(ev)) for s, ev in zip(isymsep, k))) + '.dat'
                fname1 = 'bands-sym-' + suffix + '-' + '-'.join(('{0}:{1}'.format(s, short(ev)) for s, ev in zip(isymsep, k))) + '.dat'
            else:
                fname = 'bands-{0}.dat'.format(suffix)
                fname1 = 'bands-sym-{0}.dat'.format(suffix)
            with open(fname, 'w') as f:
                f.write(sub.write_bands())
            sub.write_trace_all(degenthresh, fname=fname1)
    dumpfn(json_data, 'irrep-output.json', indent=4)