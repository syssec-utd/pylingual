def case(context, vcf, vcf_sv, vcf_cancer, vcf_str, owner, ped, update, config, no_variants, peddy_ped, peddy_sex, peddy_check):
    """Load a case into the database.

    A case can be loaded without specifying vcf files and/or bam files
    """
    adapter = context.obj['adapter']
    if config is None and ped is None:
        LOG.warning('Please provide either scout config or ped file')
        context.abort()
    config_raw = yaml.load(config) if config else {}
    try:
        config_data = parse_case_data(config=config_raw, ped=ped, owner=owner, vcf_snv=vcf, vcf_sv=vcf_sv, vcf_str=vcf_str, vcf_cancer=vcf_cancer, peddy_ped=peddy_ped, peddy_sex=peddy_sex, peddy_check=peddy_check)
    except SyntaxError as err:
        LOG.warning(err)
        context.abort()
    LOG.info('Use family %s' % config_data['family'])
    try:
        case_obj = adapter.load_case(config_data, update)
    except Exception as err:
        LOG.error('Something went wrong during loading')
        LOG.warning(err)
        context.abort()