def find_bai_file(bam_file):
    """Find out BAI file by extension given the BAM file."""
    bai_file = bam_file.replace('.bam', '.bai')
    if not os.path.exists(bai_file):
        bai_file = '{}.bai'.format(bam_file)
    return bai_file