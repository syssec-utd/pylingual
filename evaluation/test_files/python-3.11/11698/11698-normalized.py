def parse_conservations(variant):
    """Parse the conservation predictors

        Args:
            variant(dict): A variant dictionary

        Returns:
            conservations(dict): A dictionary with the conservations
    """
    conservations = {}
    conservations['gerp'] = parse_conservation(variant, 'dbNSFP_GERP___RS')
    conservations['phast'] = parse_conservation(variant, 'dbNSFP_phastCons100way_vertebrate')
    conservations['phylop'] = parse_conservation(variant, 'dbNSFP_phyloP100way_vertebrate')
    return conservations