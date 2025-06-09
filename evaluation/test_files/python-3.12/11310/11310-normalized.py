def institute(context, institute_id, sanger_recipient, coverage_cutoff, frequency_cutoff, display_name, remove_sanger):
    """
    Update an institute
    """
    adapter = context.obj['adapter']
    LOG.info('Running scout update institute')
    try:
        adapter.update_institute(internal_id=institute_id, sanger_recipient=sanger_recipient, coverage_cutoff=coverage_cutoff, frequency_cutoff=frequency_cutoff, display_name=display_name, remove_sanger=remove_sanger)
    except Exception as err:
        LOG.warning(err)
        context.abort()