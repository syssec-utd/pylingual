def _apply_transform(self, mol, rule):
    """Repeatedly apply normalization transform to molecule until no changes occur.

        It is possible for multiple products to be produced when a rule is applied. The rule is applied repeatedly to
        each of the products, until no further changes occur or after 20 attempts. If there are multiple unique products
        after the final application, the first product (sorted alphabetically by SMILES) is chosen.
        """
    mols = [mol]
    for n in six.moves.range(20):
        products = {}
        for mol in mols:
            for product in [x[0] for x in rule.RunReactants((mol,))]:
                if Chem.SanitizeMol(product, catchErrors=True) == 0:
                    products[Chem.MolToSmiles(product, isomericSmiles=True)] = product
        if products:
            mols = [products[s] for s in sorted(products)]
        else:
            return mols[0] if n > 0 else None