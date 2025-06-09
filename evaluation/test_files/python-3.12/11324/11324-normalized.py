def parse_ped(ped_stream, family_type='ped'):
    """Parse out minimal family information from a PED file.

    Args:
        ped_stream(iterable(str))
        family_type(str): Format of the pedigree information

    Returns:
        family_id(str), samples(list[dict])
    """
    pedigree = FamilyParser(ped_stream, family_type=family_type)
    if len(pedigree.families) != 1:
        raise PedigreeError('Only one case per ped file is allowed')
    family_id = list(pedigree.families.keys())[0]
    family = pedigree.families[family_id]
    samples = [{'sample_id': ind_id, 'father': individual.father, 'mother': individual.mother, 'sex': SEX_MAP[individual.sex], 'phenotype': PHENOTYPE_MAP[int(individual.phenotype)]} for ind_id, individual in family.individuals.items()]
    return (family_id, samples)