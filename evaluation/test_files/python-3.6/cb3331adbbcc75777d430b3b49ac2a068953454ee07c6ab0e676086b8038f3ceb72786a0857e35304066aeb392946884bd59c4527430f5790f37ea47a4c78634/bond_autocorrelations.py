"""
Created on Fri Nov 25 19:59:20 2022

@author: Mikhail Glagolev
"""
import MDAnalysis as mda
from MDAnalysis import transformations
import numpy as np
import json
A_GUESS = 1.0
P_GUESS = 3.0
BETA_GUESS = 0.0
B_GUESS = 0.0
FIT_PLOT_DENSITY = 10

def bond_autocorrelations(u: mda.Universe, k_max, selection=None, different_molecules: bool=False):
    """
    
    Calculate the autocorrelation function of the polymer bonds.
    The formula is presented in https://doi.org/10.1134/S0965545X10070102
    Application to all-atom simulations: https://doi.org/10.3390/polym11122056

    Parameters
    ----------
    u : mda.Universe
        Input data for analysis as MDAnalysis Universe.
    k_max : integer
        The maximum value of the distance between the bonds along the backbone
    different_molecules : bool
        Take into account the bonds where the particles have different
        residue ids. The default value is False.

    Returns
    -------
    {description: "Bond vectors autocorrelation function, for k in 
                   [0,...,k_max] the vectors belonging to different
                   molecules are (not) taken into account",
     data: {ts1: [c(0), c(1), c(2), ..., c(k_max)],
            ts2: [c(0), c(1), c(2), ..., c(k_max)],
            ....
           }
    }

    """
    description = 'Bond vectors autocorrelation function, for k in [0,...,'
    description += str(k_max)
    if different_molecules:
        description += '], the vectors belonging to different molecules' + 'are taken into account'
    else:
        description += '], the vectors belonging to different molecules' + 'are not taken into account'
    unwrap = transformations.unwrap(u.atoms)
    u.trajectory.add_transformations(unwrap)
    if selection is not None:
        atoms = u.select_atoms(selection)
    else:
        atoms = u.atoms
    data = {}
    for ts in u.trajectory:
        ck = []
        nbonds = len(atoms.bonds)
        bond_resids = atoms.bonds.atom1.resids
        b = atoms.bonds.atom2.positions - atoms.bonds.atom1.positions
        for k in range(0, k_max + 1):
            b1 = np.pad(b, ((0, k), (0, 0)), constant_values=1.0)
            b2 = np.pad(b, ((k, 0), (0, 0)), constant_values=1.0)
            valid1 = np.concatenate((np.full((nbonds,), True), np.full((k,), False)))
            valid2 = np.concatenate((np.full((k,), False), np.full((nbonds,), True)))
            valid = np.logical_and(valid1, valid2)
            if not different_molecules:
                resid1 = np.pad(bond_resids, (0, k), constant_values=0)
                resid2 = np.pad(bond_resids, (k, 0), constant_values=0)
                valid = np.logical_and(valid, np.equal(resid1, resid2))
            mask = np.logical_not(valid)
            c = np.sum(np.multiply(b1, b2), axis=1) / np.linalg.norm(b1, axis=1) / np.linalg.norm(b2, axis=1)
            c_masked = np.ma.masked_array(c, mask=mask)
            c_average = np.ma.average(c_masked)
            ck.append(c_average)
        data[str(ts)] = {'ck': ck}
    return {'description': description, 'data': data}

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Calculate the autocorrelation function of the \n        polymer bonds. The formula is presented in \n        https://doi.org/10.1134/S0965545X10070102 Application to\n        all-atom simulations: https://doi.org/10.3390/polym11122056')
    parser.add_argument('input', metavar='INPUT', action='store', nargs='+', help='input file(s), the format will be guessed by MDAnalysis \n        based on file extension')
    parser.add_argument('--k_max', metavar='k_max', type=int, nargs='?', default=0, help='maximum distance between the bonds along the backbone')
    parser.add_argument('--selection', metavar='QUERY', type=str, nargs='?', help='Consider only selected atoms, use MDAnalysis selection language')
    parser.add_argument('--different-molecules', action='store_true', help='Calculate correlations based on particle index number,            even if the bonds belong to different molecules')
    parser.add_argument('--plot', action='store_true', help='Plot the averaged results')
    parser.add_argument('--fit', action='store_true', help='Fit the averaged results with a modulated exponential function')
    parser.add_argument('--p_guess', metavar='NUMBER', type=float, nargs='?', default=3.5, help='Initial guess for the number of monomer units per turn')
    args = parser.parse_args()
    u = mda.Universe(*args.input)
    result = bond_autocorrelations(u, k_max=args.k_max, selection=args.selection, different_molecules=args.different_molecules)
    if args.plot or args.fit:
        summed_data = np.ndarray((args.k_max + 1,))
        for ts in result['data']:
            summed_data += np.asarray(result['data'][ts])
        averaged_data = summed_data / len(result['data'])
    if args.fit:
        from scipy.optimize import curve_fit

        def fitting_function(x, a, p, beta, b):
            return a * (np.cos(2.0 * np.pi * x / p) + b) * np.exp(x * beta)
        initial_guess = [A_GUESS, args.p_guess, BETA_GUESS, B_GUESS]
        (params, covariance) = curve_fit(fitting_function, list(range(1, args.k_max + 1)), averaged_data[1:], p0=initial_guess)
    if args.plot:
        import matplotlib.pyplot as plt
        plt.plot(range(args.k_max + 1), averaged_data)
        if args.fit:
            fitting_x = np.asarray(list(range(args.k_max * FIT_PLOT_DENSITY + 1)))
            fitting_x = fitting_x / float(FIT_PLOT_DENSITY)
            vectorized_fitting_function = np.vectorize(fitting_function, excluded=[1, 2, 3, 4])
            fitting_y = vectorized_fitting_function(fitting_x, params[0], params[1], params[2], params[3])
            plt.plot(fitting_x, fitting_y, label='p=%.2f' % params[1] + '\nbeta=%.2f' % params[2] + '\nb=%.2f' % params[3])
        plt.xlabel('k', fontsize=18)
        plt.ylabel('C(k)', fontsize=18)
        plt.legend(shadow=False, fontsize=18)
        plt.show()
    print(json.dumps(result, indent=2))
if __name__ == '__main__':
    main()