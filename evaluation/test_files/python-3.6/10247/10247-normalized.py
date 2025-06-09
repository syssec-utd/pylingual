def isotope_parent(self, mol, skip_standardize=False):
    """Return the isotope parent of a given molecule.

        The isotope parent has all atoms replaced with the most abundant isotope for that element.

        :param mol: The input molecule.
        :type mol: rdkit.Chem.rdchem.Mol
        :param bool skip_standardize: Set to True if mol has already been standardized.
        :returns: The isotope parent molecule.
        :rtype: rdkit.Chem.rdchem.Mol
        """
    if not skip_standardize:
        mol = self.standardize(mol)
    else:
        mol = copy.deepcopy(mol)
    for atom in mol.GetAtoms():
        atom.SetIsotope(0)
    return mol