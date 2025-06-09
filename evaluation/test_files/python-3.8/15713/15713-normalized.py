def run_picard_sort(job, bam, sort_by_name=False):
    """
    Sorts BAM file using Picard SortSam

    :param JobFunctionWrappingJob job: passed automatically by Toil
    :param str bam: FileStoreID for BAM file
    :param boolean sort_by_name: If true, sorts by read name instead of coordinate.
    :return: FileStoreID for sorted BAM file
    :rtype: str
    """
    work_dir = job.fileStore.getLocalTempDir()
    job.fileStore.readGlobalFile(bam, os.path.join(work_dir, 'input.bam'))
    command = ['SortSam', 'O=/data/output.bam', 'I=/data/input.bam']
    docker_parameters = ['--rm', '--log-driver', 'none', '-e', 'JAVA_OPTIONS=-Djava.io.tmpdir=/data/ -Xmx{}'.format(job.memory), '-v', '{}:/data'.format(work_dir)]
    if sort_by_name:
        command.append('SO=queryname')
    else:
        command.append('SO=coordinate')
    start_time = time.time()
    dockerCall(job=job, workDir=work_dir, parameters=command, tool='quay.io/ucsc_cgl/picardtools:1.95--dd5ac549b95eb3e5d166a5e310417ef13651994e', dockerParameters=docker_parameters)
    end_time = time.time()
    _log_runtime(job, start_time, end_time, 'Picard SortSam')
    return job.fileStore.writeGlobalFile(os.path.join(work_dir, 'output.bam'))