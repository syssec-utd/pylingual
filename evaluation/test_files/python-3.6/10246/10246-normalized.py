def stereo_parent(self, mol, skip_standardize=False):
    """Return the stereo parent of a given molecule.

        The stereo parent has all stereochemistry information removed from tetrahedral centers and double bonds.

        :param mol: The input molecule.
        :type mol: rdkit.Chem.rdchem.Mol
        :param bool skip_standardize: Set to True if mol has already been standardized.
        :returns: The stereo parent molecule.
        :rtype: rdkit.Chem.rdchem.Mol
        """
    if not skip_standardize:
        mol = self.standardize(mol)
    else:
        mol = copy.deepcopy(mol)
    Chem.RemoveStereochemistry(mol)
    return mol