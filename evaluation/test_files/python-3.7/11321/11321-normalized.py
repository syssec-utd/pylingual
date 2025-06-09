def parse_individual(sample):
    """Parse individual information

        Args:
            sample (dict)

        Returns:
            {
                'individual_id': str,
                'father': str,
                'mother': str,
                'display_name': str,
                'sex': str,
                'phenotype': str,
                'bam_file': str,
                'vcf2cytosure': str,
                'analysis_type': str,
                'capture_kits': list(str),
            }

    """
    ind_info = {}
    if 'sample_id' not in sample:
        raise PedigreeError("One sample is missing 'sample_id'")
    sample_id = sample['sample_id']
    if 'sex' not in sample:
        raise PedigreeError("Sample %s is missing 'sex'" % sample_id)
    sex = sample['sex']
    if sex not in REV_SEX_MAP:
        log.warning("'sex' is only allowed to have values from {}".format(', '.join(list(REV_SEX_MAP.keys()))))
        raise PedigreeError('Individual %s has wrong formated sex' % sample_id)
    if 'phenotype' not in sample:
        raise PedigreeError("Sample %s is missing 'phenotype'" % sample_id)
    phenotype = sample['phenotype']
    if phenotype not in REV_PHENOTYPE_MAP:
        log.warning("'phenotype' is only allowed to have values from {}".format(', '.join(list(REV_PHENOTYPE_MAP.keys()))))
        raise PedigreeError('Individual %s has wrong formated phenotype' % sample_id)
    ind_info['individual_id'] = sample_id
    ind_info['display_name'] = sample.get('sample_name', sample['sample_id'])
    ind_info['sex'] = sex
    ind_info['phenotype'] = phenotype
    ind_info['father'] = sample.get('father')
    ind_info['mother'] = sample.get('mother')
    ind_info['confirmed_parent'] = sample.get('confirmed_parent')
    ind_info['confirmed_sex'] = sample.get('confirmed_sex')
    ind_info['predicted_ancestry'] = sample.get('predicted_ancestry')
    bam_file = sample.get('bam_path')
    if bam_file:
        ind_info['bam_file'] = bam_file
    mt_bam = sample.get('mt_bam')
    if mt_bam:
        ind_info['mt_bam'] = mt_bam
    analysis_type = sample.get('analysis_type')
    if analysis_type:
        ind_info['analysis_type'] = analysis_type
    ind_info['capture_kits'] = [sample.get('capture_kit')] if 'capture_kit' in sample else []
    vcf2cytosure = sample.get('vcf2cytosure')
    if vcf2cytosure:
        ind_info['vcf2cytosure'] = vcf2cytosure
    tumor_type = sample.get('tumor_type')
    if tumor_type:
        ind_info['tumor_type'] = tumor_type
    tumor_mutational_burden = sample.get('tmb')
    if tumor_mutational_burden:
        ind_info['tmb'] = tumor_mutational_burden
    msi = sample.get('msi')
    if msi:
        ind_info['msi'] = msi
    tumor_purity = sample.get('tumor_purity')
    if tumor_purity:
        ind_info['tumor_purity'] = tumor_purity
    return ind_info