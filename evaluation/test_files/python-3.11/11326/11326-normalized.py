def mt_report(context, case_id, test, outpath=None):
    """Export all mitochondrial variants for each sample of a case
       and write them to an excel file

        Args:
            adapter(MongoAdapter)
            case_id(str)
            test(bool): True if the function is called for testing purposes
            outpath(str): path to output file

        Returns:
            written_files(int): number of written or simulated files
    """
    LOG.info('exporting mitochondrial variants for case "{}"'.format(case_id))
    adapter = context.obj['adapter']
    query = {'chrom': 'MT'}
    case_obj = adapter.case(case_id=case_id)
    if not case_obj:
        LOG.warning('Could not find a scout case with id "{}". No report was created.'.format(case_id))
        context.abort()
    samples = case_obj.get('individuals')
    mt_variants = list(adapter.variants(case_id=case_id, query=query, nr_of_variants=-1, sort_key='position'))
    if not mt_variants:
        LOG.warning('There are no MT variants associated to case {} in database!'.format(case_id))
        context.abort()
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    if not outpath:
        outpath = str(os.getcwd())
    written_files = 0
    for sample in samples:
        sample_id = sample['individual_id']
        sample_lines = export_mt_variants(variants=mt_variants, sample_id=sample_id)
        document_name = '.'.join([case_obj['display_name'], sample_id, today]) + '.xlsx'
        workbook = Workbook(os.path.join(outpath, document_name))
        Report_Sheet = workbook.add_worksheet()
        if test and sample_lines and workbook:
            written_files += 1
            continue
        row = 0
        for col, field in enumerate(MT_EXPORT_HEADER):
            Report_Sheet.write(row, col, field)
        for row, line in enumerate(sample_lines, 1):
            for col, field in enumerate(line):
                Report_Sheet.write(row, col, field)
        workbook.close()
        if os.path.exists(os.path.join(outpath, document_name)):
            written_files += 1
    if test:
        LOG.info('Number of excel files that can be written to folder {0}: {1}'.format(outpath, written_files))
    else:
        LOG.info('Number of excel files written to folder {0}: {1}'.format(outpath, written_files))
    return written_files