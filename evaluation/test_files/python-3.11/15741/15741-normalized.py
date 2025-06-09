def bam_quickcheck(bam_path):
    """
    Perform a quick check on a BAM via `samtools quickcheck`.
    This will detect obvious BAM errors such as truncation.

    :param str bam_path: path to BAM file to checked

    :rtype: boolean
    :return: True if the BAM is valid, False is BAM is invalid or something related to the call went wrong
    """
    directory, bam_name = os.path.split(bam_path)
    exit_code = subprocess.call(['docker', 'run', '-v', directory + ':/data', 'quay.io/ucsc_cgl/samtools:1.3--256539928ea162949d8a65ca5c79a72ef557ce7c', 'quickcheck', '-vv', '/data/' + bam_name])
    if exit_code != 0:
        return False
    return True