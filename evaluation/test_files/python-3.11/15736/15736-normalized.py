def gatk_select_variants(job, mode, vcf_id, ref_fasta, ref_fai, ref_dict):
    """
    Isolates a particular variant type from a VCF file using GATK SelectVariants

    :param JobFunctionWrappingJob job: passed automatically by Toil
    :param str mode: variant type (i.e. SNP or INDEL)
    :param str vcf_id: FileStoreID for input VCF file
    :param str ref_fasta: FileStoreID for reference genome fasta
    :param str ref_fai: FileStoreID for reference genome index file
    :param str ref_dict: FileStoreID for reference genome sequence dictionary file
    :return: FileStoreID for filtered VCF
    :rtype: str
    """
    job.fileStore.logToMaster('Running GATK SelectVariants to select %ss' % mode)
    inputs = {'genome.fa': ref_fasta, 'genome.fa.fai': ref_fai, 'genome.dict': ref_dict, 'input.vcf': vcf_id}
    work_dir = job.fileStore.getLocalTempDir()
    for name, file_store_id in inputs.iteritems():
        job.fileStore.readGlobalFile(file_store_id, os.path.join(work_dir, name))
    command = ['-T', 'SelectVariants', '-R', 'genome.fa', '-V', 'input.vcf', '-o', 'output.vcf', '-selectType', mode]
    docker_parameters = ['--rm', 'log-driver', 'none', '-e', 'JAVA_OPTS=-Djava.io.tmpdir=/data/ -Xmx{}'.format(job.memory)]
    dockerCall(job=job, workDir=work_dir, parameters=command, tool='quay.io/ucsc_cgl/gatk:3.5--dba6dae49156168a909c43330350c6161dc7ecc2', dockerParameters=docker_parameters)
    return job.fileStore.writeGlobalFile(os.path.join(work_dir, 'output.vcf'))