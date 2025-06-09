def picard_mark_duplicates(job, bam, bai, validation_stringency='LENIENT'):
    """
    Runs Picard MarkDuplicates on a BAM file. Requires that the BAM file be coordinate sorted.

    :param JobFunctionWrappingJob job: passed automatically by Toil
    :param str bam: FileStoreID for BAM file
    :param str bai: FileStoreID for BAM index file
    :param str validation_stringency: BAM file validation stringency, default is LENIENT
    :return: FileStoreIDs for BAM and BAI files
    :rtype: tuple
    """
    work_dir = job.fileStore.getLocalTempDir()
    job.fileStore.readGlobalFile(bam, os.path.join(work_dir, 'sorted.bam'))
    job.fileStore.readGlobalFile(bai, os.path.join(work_dir, 'sorted.bai'))
    command = ['MarkDuplicates', 'INPUT=sorted.bam', 'OUTPUT=mkdups.bam', 'METRICS_FILE=metrics.txt', 'ASSUME_SORTED=true', 'CREATE_INDEX=true', 'VALIDATION_STRINGENCY=%s' % validation_stringency.upper()]
    docker_parameters = ['--rm', '--log-driver', 'none', '-e', 'JAVA_OPTIONS=-Djava.io.tmpdir=/data/ -Xmx{}'.format(job.memory), '-v', '{}:/data'.format(work_dir)]
    start_time = time.time()
    dockerCall(job=job, workDir=work_dir, parameters=command, tool='quay.io/ucsc_cgl/picardtools:1.95--dd5ac549b95eb3e5d166a5e310417ef13651994e', dockerParameters=docker_parameters)
    end_time = time.time()
    _log_runtime(job, start_time, end_time, 'Picard MarkDuplicates')
    bam = job.fileStore.writeGlobalFile(os.path.join(work_dir, 'mkdups.bam'))
    bai = job.fileStore.writeGlobalFile(os.path.join(work_dir, 'mkdups.bai'))
    return (bam, bai)