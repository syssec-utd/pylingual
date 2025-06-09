def canonicalize_tautomer_smiles(smiles):
    """Return a standardized canonical tautomer SMILES string given a SMILES string.

    Note: This is a convenience function for quickly standardizing and finding the canonical tautomer for a single
    SMILES string. It is more efficient to use the :class:`~molvs.standardize.Standardizer` class directly when working
    with many molecules or when custom options are needed.

    :param string smiles: The SMILES for the molecule.
    :returns: The SMILES for the standardize canonical tautomer.
    :rtype: string.
    """
    mol = Chem.MolFromSmiles(smiles, sanitize=False)
    mol = Standardizer().standardize(mol)
    tautomer = TautomerCanonicalizer().canonicalize(mol)
    return Chem.MolToSmiles(tautomer, isomericSmiles=True)