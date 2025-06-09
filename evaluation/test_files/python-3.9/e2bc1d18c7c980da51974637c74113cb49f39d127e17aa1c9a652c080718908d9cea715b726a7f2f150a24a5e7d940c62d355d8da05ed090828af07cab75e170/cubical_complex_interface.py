import os
import numpy as np
from ..modules.gtda_cubical_complex import Cubical_complex_interface as Bitmap_cubical_complex_base_interface
from ..modules.gtda_persistent_cohomology import Persistent_cohomology_interface as Cubical_complex_persistence_interface

class CubicalComplex:
    """The CubicalComplex is an example of a structured complex useful in
    computational mathematics (specially rigorous numerics) and image
    analysis.
    """

    def __init__(self, dimensions=None, top_dimensional_cells=None, perseus_file=''):
        """CubicalComplex constructor from dimensions and
        top_dimensional_cells or from a Perseus-style file name.
        :param dimensions: A list of number of top dimensional cells.
        :type dimensions: list of int
        :param top_dimensional_cells: A list of cells filtration values.
        :type top_dimensional_cells: list of double
        Or
        :param perseus_file: A Perseus-style file name.
        :type perseus_file: string
        """
        self.thisptr = None
        self.pcohptr = None
        if dimensions is not None and top_dimensional_cells is not None and (perseus_file == ''):
            self.thisptr = Bitmap_cubical_complex_base_interface(dimensions, top_dimensional_cells)
        elif dimensions is None and top_dimensional_cells is None and (perseus_file != ''):
            if os.path.isfile(perseus_file):
                self.thisptr = Bitmap_cubical_complex_base_interface(str.encode(perseus_file))
            else:
                print('file ' + perseus_file + ' not found.')
        else:
            print('CubicalComplex can be constructed from dimensions and top_dimensional_cells or from a Perseus-style file name.')

    def __del__(self):
        if self.thisptr is not None:
            del self.thisptr
        if self.pcohptr is not None:
            del self.pcohptr

    def __is_defined(self):
        """Returns true if CubicalComplex pointer is not NULL.
         """
        if self.thisptr is not None:
            return True
        return False

    def __is_persistence_defined(self):
        """Returns true if Persistence pointer is not NULL.
         """
        if self.pcohptr is not None:
            return True
        return False

    def num_simplices(self):
        """This function returns the number of all cubes in the complex.
        :returns:  int -- the number of all cubes in the complex.
        """
        return self.thisptr.num_simplices()

    def dimension(self):
        """This function returns the dimension of the complex.
        :returns:  int -- the complex dimension.
        """
        return self.thisptr.dimension()

    def persistence(self, homology_coeff_field=11, min_persistence=0):
        """This function returns the persistence of the complex.
        :param homology_coeff_field: The homology coefficient field. Must be a
            prime number
        :type homology_coeff_field: int.
        :param min_persistence: The minimum persistence value to take into
            account (strictly greater than min_persistence). Default value is
            0.0.
            Sets min_persistence to -1.0 to see all values.
        :type min_persistence: float.
        :returns: list of pairs(dimension, pair(birth, death)) -- the
            persistence of the complex.
        """
        if self.pcohptr is not None:
            del self.pcohptr
        if self.thisptr is not None:
            pass
            self.pcohptr = Cubical_complex_persistence_interface(self.thisptr, True)
        persistence_result = []
        if self.pcohptr is not None:
            self.pcohptr.compute_persistence(homology_coeff_field, min_persistence)
            persistence_result = self.pcohptr.get_persistence()
        return persistence_result

    def betti_numbers(self):
        """This function returns the Betti numbers of the complex.
        :returns: list of int -- The Betti numbers ([B0, B1, ..., Bn]).
        :note: betti_numbers function requires persistence function to be
            launched first.
        :note: betti_numbers function always returns [1, 0, 0, ...] as infinity
            filtration cubes are not removed from the complex.
        """
        bn_result = []
        if self.pcohptr is not None:
            bn_result = self.pcohptr.betti_numbers()
        return bn_result

    def persistent_betti_numbers(self, from_value, to_value):
        """This function returns the persistent Betti numbers of the complex.
        :param from_value: The persistence birth limit to be added in the
            numbers (persistent birth <= from_value).
        :type from_value: float.
        :param to_value: The persistence death limit to be added in the
            numbers (persistent death > to_value).
        :type to_value: float.
        :returns: list of int -- The persistent Betti numbers ([B0, B1, ...,
            Bn]).
        :note: persistent_betti_numbers function requires persistence
            function to be launched first.
        """
        pbn_result = []
        if self.pcohptr is not None:
            pbn_result = self.pcohptr.persistent_betti_numbers(from_value, to_value)
        return pbn_result

    def persistence_intervals_in_dimension(self, dimension):
        """This function returns the persistence intervals of the complex in a
        specific dimension.
        :param dimension: The specific dimension.
        :type dimension: int.
        :returns: The persistence intervals.
        :rtype:  numpy array of dimension 2
        :note: intervals_in_dim function requires persistence function to be
            launched first.
        """
        intervals_result = [[]]
        if self.pcohptr is not None:
            intervals_result = self.pcohptr.intervals_in_dimension(dimension)
        else:
            print('intervals_in_dim function requires persistence function to be launched first.')
        return np.array(intervals_result)