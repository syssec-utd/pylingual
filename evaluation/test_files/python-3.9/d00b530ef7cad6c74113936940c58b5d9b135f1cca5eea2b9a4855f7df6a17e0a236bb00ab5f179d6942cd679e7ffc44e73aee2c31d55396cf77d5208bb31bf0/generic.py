import numpy as np
from pyiron_atomistics.atomistics.job.atomistic import AtomisticGenericJob, MapFunctions as AtomisticMapFunctions
from pyiron_atomistics.dft.waves.electronic import ElectronicStructure
import warnings
__author__ = 'Jan Janssen'
__copyright__ = 'Copyright 2021, Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department'
__version__ = '1.0'
__maintainer__ = 'Jan Janssen'
__email__ = 'janssen@mpie.de'
__status__ = 'production'
__date__ = 'Sep 1, 2017'

class GenericDFTJob(AtomisticGenericJob):

    def __init__(self, project, job_name):
        super(GenericDFTJob, self).__init__(project, job_name)
        self._generic_input['fix_symmetry'] = True
        self.map_functions = MapFunctions()
        self._generic_input['k_mesh_spacing'] = None
        self._generic_input['k_mesh_center_shift'] = None
        self._generic_input['reduce_kpoint_symmetry'] = True

    @property
    def encut(self):
        return self.plane_wave_cutoff

    @encut.setter
    def encut(self, val):
        self.plane_wave_cutoff = val

    @property
    def kpoint_mesh(self):
        return self.get_kpoints()

    @kpoint_mesh.setter
    def kpoint_mesh(self, val):
        self.set_kpoints(mesh=val)

    @property
    def xc(self):
        return self.exchange_correlation_functional

    @xc.setter
    def xc(self, val):
        self.exchange_correlation_functional = val

    @property
    def plane_wave_cutoff(self):
        raise NotImplementedError('The encut property is not implemented for this code.')

    @plane_wave_cutoff.setter
    def plane_wave_cutoff(self, val):
        raise NotImplementedError('The encut property is not implemented for this code.')

    @property
    def spin_constraints(self):
        raise NotImplementedError('The spin_constraints property is not implemented for this code.')

    @spin_constraints.setter
    def spin_constraints(self, val):
        raise NotImplementedError('The spin_constraints property is not implemented for this code.')

    @property
    def exchange_correlation_functional(self):
        raise NotImplementedError('The exchange property is not implemented for this code.')

    @exchange_correlation_functional.setter
    def exchange_correlation_functional(self, val):
        raise NotImplementedError('The exchange property is not implemented for this code.')

    @property
    def k_mesh_spacing(self):
        """
        Number of unreduced k-points per Angstrom of the lattice vector

        Returns:
            float: Number of k-points per Angstrom
        """
        return self._generic_input['k_mesh_spacing']

    @k_mesh_spacing.setter
    def k_mesh_spacing(self, val):
        self._generic_input['k_mesh_spacing'] = val

    @property
    def k_mesh_center_shift(self):
        """
        Number of unreduced k-points per Angstrom of the lattice vector

        Returns:
            float: Number of k-points per Angstrom
        """
        return self._generic_input['k_mesh_center_shift']

    @k_mesh_center_shift.setter
    def k_mesh_center_shift(self, val):
        self._generic_input['k_mesh_center_shift'] = val

    @property
    def reduce_kpoint_symmetry(self):
        """
        Number of unreduced k-points per Angstrom of the lattice vector

        Returns:
            float: Number of k-points per Angstrom
        """
        return self._generic_input['reduce_kpoint_symmetry']

    @reduce_kpoint_symmetry.setter
    def reduce_kpoint_symmetry(self, boolean):
        self._generic_input['reduce_kpoint_symmetry'] = boolean

    @property
    def fix_spin_constraint(self):
        return self._generic_input['fix_spin_constraint']

    @fix_spin_constraint.setter
    def fix_spin_constraint(self, boolean):
        if not isinstance(boolean, bool):
            raise AssertionError()
        self._generic_input['fix_spin_constraint'] = boolean

    @property
    def fix_symmetry(self):
        return self._generic_input['fix_symmetry']

    @fix_symmetry.setter
    def fix_symmetry(self, boolean):
        if not isinstance(boolean, bool):
            raise AssertionError()
        self._generic_input['fix_symmetry'] = boolean

    def _get_structure(self, frame=-1, wrap_atoms=True):
        snapshot = super(GenericDFTJob, self)._get_structure(frame=frame, wrap_atoms=wrap_atoms)
        spins = self.get_magnetic_moments(iteration_step=frame)
        if spins is not None:
            snapshot.set_initial_magnetic_moments(spins)
        return snapshot

    def set_mixing_parameters(self, method=None, n_pulay_steps=None, density_mixing_parameter=None, spin_mixing_parameter=None, density_residual_scaling=None, spin_residual_scaling=None):
        """
        Args:
            method (str): mixing method 'PULAY' or 'KERKER' (default: PULAY)
            n_pulay_steps (int): number of previous densities to use for the Pulay mixing
                (default: 7)
            density_mixing_parameter (float): mixing ratio of rho_opt to rho_in
            spin_mixing_parameter (float): linear mixing parameter for spin densities
            density_residual_scaling (float): scaling for the residual contribution of the Kerker
                mixing. 1 means it takes as much rho_in (input density) as residual (where Kerker
                preconditioning applies). The lower the value, the smaller the residual
                contribution becomes.
            spin_residual_scaling (float): scaling for the spin residual
                (cf. density_residual_scaling)

            Mixing ratio m is given by:

                rho^n = (m-1)*rho_in+m*preconditioner*rho_opt


        A low value of density mixing parameter may lead to a more stable convergence, but will slow
        down the calculation if set too low. In systems with bands around the Fermi energy (i.e.
        metals, e.g. Fe, Mn), the mixing parameters should be small. In insulators (e.g. Al, Si) the
        mixing parameter should be high.

        """
        raise NotImplementedError('set_mixing_parameters is not implemented for this code.')

    def restart_for_band_structure_calculations(self, job_name=None):
        """
        Restart a new job created from an existing calculation by reading the charge density
        for band structure calculations.

        Args:
            job_name (str/None): Job name

        Returns:
            new_ham (pyiron_atomistics.dft.job.generic.GenericDFTJob): New job
        """
        raise NotImplementedError('restart_for_band_structure_calculations is not implemented for this code.')

    def get_magnetic_moments(self, iteration_step=-1):
        """
        Gives the magnetic moments of a calculation for each iteration step.

        Args:
            iteration_step (int): Step for which the structure is requested

        Returns:
            numpy.ndarray/None: array of final magmetic moments or None if no magnetic moment is given
        """
        spins = self.get('output/generic/dft/atom_spins')
        if spins is not None:
            return spins[iteration_step]
        else:
            return None

    def get_kpoints(self):
        raise NotImplementedError('The get_kpoints() function is not implemented for this code.')

    def get_valence_and_total_charge_density(self):
        raise NotImplementedError('The get_valence_and_total_charge_density() function is not implemented for this code.')

    def get_k_mesh_by_cell(self, k_mesh_spacing, cell=None):
        """
        Get k-mesh density according to the box size.

        Args:
            k_mesh_spacing (float): K-point spacing in units of 2 * pi reciprocal Angstrom.
                                (smaller values result in a denser mesh for a given structure).
            cell (numpy.ndarray/list): The cell shape

        Returns:
            list/numpy.ndarray: Mesh size

        """
        if cell is None:
            if self.structure is None:
                raise ValueError("Can't generate k-points without structure being set and if cell is not specified")
            cell = self.structure.cell
        return get_k_mesh_by_density(cell=cell, k_mesh_spacing=k_mesh_spacing)

    def set_kpoints(self, mesh=None, scheme='MP', center_shift=None, symmetry_reduction=True, manual_kpoints=None, weights=None, reciprocal=True, k_mesh_spacing=None, n_path=None, path_name=None):
        """
        Function to setup the k-points

        Args:
            mesh (list/numpy.ndarray): Size of the mesh (ignored if scheme is not set to 'MP' or kpoints_per_reciprocal_
            angstrom is set)
            scheme (str): Type of k-point generation scheme (MP/GP(gamma point)/Manual/Line)
            center_shift (list/numpy.ndarray/None): Shifts the center of the mesh from the gamma point by the given vector in relative coordinates
            symmetry_reduction (boolean): Tells if the symmetry reduction is to be applied to the k-points
            manual_kpoints (list/numpy.ndarray): Manual list of k-points
            weights(list/numpy.ndarray): Manually supplied weights to each k-point in case of the manual mode
            reciprocal (bool): Tells if the supplied values are in reciprocal (direct) or cartesian coordinates (in
            reciprocal space)
            k_mesh_spacing (float): K-point spacing in units of 2 * pi reciprocal Angstrom.
                                (smaller values result in a denser mesh for a given structure).
            n_path (int): Number of points per trace part for line mode
            path_name (str): Name of high symmetry path used for band structure calculations.
        """
        if k_mesh_spacing is not None:
            if mesh is not None:
                warnings.warn('mesh value is overwritten by k_mesh_spacing')
            mesh = self.get_k_mesh_by_cell(k_mesh_spacing=k_mesh_spacing)
        self.k_mesh_spacing = k_mesh_spacing
        self.k_mesh_center_shift = center_shift
        self.reduce_kpoint_symmetry = symmetry_reduction
        if mesh is not None:
            if np.min(mesh) <= 0:
                raise ValueError('mesh values must be larger than 0')
        if center_shift is not None:
            if np.min(center_shift) < 0 or np.max(center_shift) > 1:
                warnings.warn('center_shift is given in relative coordinates')
        self._set_kpoints(mesh=mesh, scheme=scheme, center_shift=center_shift, symmetry_reduction=symmetry_reduction, manual_kpoints=manual_kpoints, weights=weights, reciprocal=reciprocal, n_path=n_path, path_name=path_name)

    def calc_static(self, electronic_steps=100, algorithm=None, retain_charge_density=False, retain_electrostatic_potential=False):
        self._generic_input['fix_symmetry'] = True
        super(GenericDFTJob, self).calc_static()

    def calc_minimize(self, electronic_steps=60, ionic_steps=100, max_iter=None, pressure=None, algorithm=None, retain_charge_density=False, retain_electrostatic_potential=False, ionic_energy_tolerance=None, ionic_force_tolerance=None, ionic_energy=None, ionic_forces=None, volume_only=False):
        self._generic_input['fix_symmetry'] = True
        super(GenericDFTJob, self).calc_minimize(max_iter=max_iter, pressure=pressure)

    def calc_md(self, temperature=None, n_ionic_steps=1000, n_print=1, time_step=1.0, retain_charge_density=False, retain_electrostatic_potential=False, **kwargs):
        self._generic_input['fix_symmetry'] = False
        super(GenericDFTJob, self).calc_md(temperature=temperature, n_ionic_steps=n_ionic_steps, n_print=n_print, time_step=time_step)

    def nbands_convergence_check(self):
        """
        Function to check if there are a sufficient number of empty bands in the calculation to ensure electronic convergence.

        Returns:

            bool : True if the highest band is unoccupied, False if the highest band is occupied
        """
        return np.all(np.isclose(self['output/electronic_structure/occ_matrix'][:, :, -1], 0))

    def get_encut(self):
        return self.encut

    def set_encut(self, encut):
        """
        Sets the plane-wave energy cutoff
        Args:
            encut (float): The energy cutoff in eV
        """
        self.plane_wave_cutoff = encut

    def set_exchange_correlation_functional(self, exchange_correlation_functional):
        self.exchange_correlation_functional = exchange_correlation_functional

    def set_empty_states(self, n_empty_states=None):
        raise NotImplementedError('The set_empty_states function is not implemented for this code.')

    def get_bader_charges(self):
        """
        Returns the total charge on every atom determined by the Bader charge partitioning scheme.

        Returns:
            numpy.ndarray: The Bader charges for each atom

        """
        return self['output/generic/dft/bader_charges']

    def get_bader_volumes(self):
        """
        Returns the integration volume around every atom from the Bader charge partitioning scheme.

        Returns:
            numpy.ndarray: The Bader charges for each atom

        """
        return self['output/generic/dft/bader_volumes']

    def _set_kpoints(self, mesh=None, scheme='MP', center_shift=None, symmetry_reduction=True, manual_kpoints=None, weights=None, reciprocal=True, n_path=None, path_name=None):
        raise NotImplementedError('The set_kpoints function is not implemented for this code.')

    def get_electronic_structure(self):
        """
        Gets the electronic structure instance from the hdf5 file

        Returns:
                pyiron_atomistics.atomistics.waves.electronic.ElectronicStructure instance
        """
        if self.status not in ['finished', 'warning', 'not_converged']:
            return
        else:
            with self.project_hdf5.open('output') as ho:
                es_obj = ElectronicStructure()
                es_obj.from_hdf(ho)
            return es_obj

    def modify_kpoints(self):
        if self.k_mesh_spacing is not None:
            self.set_kpoints(center_shift=self.k_mesh_center_shift, k_mesh_spacing=self.k_mesh_spacing, symmetry_reduction=self.reduce_kpoint_symmetry)

    def save(self):
        self.modify_kpoints()
        super(GenericDFTJob, self).save()

    def get_density_of_states(self, sigma=0.1, shift_by_fermi_energy=True, grid=None):
        """
        Get density of states from a fully converged result. A Gaussian smeared histogram is
        returned

        Args:
            sigma (float): Gaussian smearing parameter in energy unit.
            shift_by_fermi_energy (bool): Shift the histogram by the Fermi energy value. Setting
                this to False will return code specific absolute values which have physically no
                meaning.
            grid (list/numpy.ndarray): Energy grid. If None, the interval between maximum and
                minimum eigenvalues plus 5 x sigma with a step length of sigma will be taken.

        Returns:
            (dict): grid and density of states (n_spin x energy_grid)
        """
        if sigma <= 0:
            raise ValueError('Sigma must be a positive float')
        k_weights = self['output/electronic_structure/k_weights']
        if k_weights is None:
            raise ValueError('k-point weighting not found')
        e_fermi = 0
        if shift_by_fermi_energy:
            e_fermi = self['output/electronic_structure/efermi']
        eigen_values = self['output/electronic_structure/eig_matrix']
        eigen_values = eigen_values - e_fermi
        if grid is None:
            grid = np.arange(eigen_values.min() - 5 * sigma, eigen_values.max() + 5 * sigma, sigma)
        hist = eigen_values[:, :, :, np.newaxis] - grid[np.newaxis, np.newaxis, np.newaxis, :]
        hist = np.exp(-hist ** 2 / (2 * sigma ** 2)) * k_weights[np.newaxis, :, np.newaxis, np.newaxis]
        hist = np.sum(hist, axis=(1, 2))
        hist *= 2 / len(eigen_values) / np.sqrt(2 * np.pi * sigma ** 2)
        return {'grid': grid, 'dos': hist}

def get_k_mesh_by_density(cell, k_mesh_spacing=0.5):
    """
    Get k-mesh density according to the box size.

    Args:
        cell (numpy.ndarray/list): The cell shape
        k_mesh_spacing (float): K-point spacing in units of 2 * pi reciprocal Angstrom.
                                (smaller values result in a denser mesh for a given structure).

    Returns:
        list/numpy.ndarray: Mesh size

    """
    omega = np.linalg.det(cell)
    (l1, l2, l3) = cell
    g1 = 2 * np.pi / omega * np.cross(l2, l3)
    g2 = 2 * np.pi / omega * np.cross(l3, l1)
    g3 = 2 * np.pi / omega * np.cross(l1, l2)
    kmesh = np.rint(np.array([np.linalg.norm(g) for g in [g1, g2, g3]]) / k_mesh_spacing)
    kmesh[kmesh < 1] = 1
    return [int(k) for k in kmesh]

def set_encut(job, parameter):
    job.set_encut(parameter)
    return job

def set_kpoints(job, parameter):
    job.set_kpoints(parameter)
    return job

class MapFunctions(AtomisticMapFunctions):

    def __init__(self):
        super().__init__()
        self.set_encut = set_encut
        self.set_kpoints = set_kpoints