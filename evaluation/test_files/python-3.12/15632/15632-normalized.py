def call_adam(job, master_ip, arguments, memory=None, override_parameters=None, run_local=False, native_adam_path=None):
    """
    Invokes the ADAM container. Find ADAM at https://github.com/bigdatagenomics/adam.

    :param toil.Job.job job: The Toil Job calling this function
    :param masterIP: The Spark leader IP address.
    :param arguments: Arguments to pass to ADAM.
    :param memory: Gigabytes of memory to provision for Spark driver/worker.
    :param override_parameters: Parameters passed by the user, that override our defaults.
    :param native_adam_path: Path to ADAM executable. If not provided, Docker is used.
    :param run_local: If true, runs Spark with the --master local[*] setting, which uses
      all cores on the local machine. The master_ip will be disregarded.

    :type masterIP: MasterAddress
    :type arguments: list of string
    :type memory: int or None
    :type override_parameters: list of string or None
    :type native_adam_path: string or None
    :type run_local: boolean
    """
    if run_local:
        master = ['--master', 'local[*]']
    else:
        master = ['--master', 'spark://%s:%s' % (master_ip, SPARK_MASTER_PORT), '--conf', 'spark.hadoop.fs.default.name=hdfs://%s:%s' % (master_ip, HDFS_MASTER_PORT)]
    default_params = master + ['--conf', 'spark.driver.maxResultSize=0', '--conf', 'spark.storage.memoryFraction=0.3', '--conf', 'spark.storage.unrollFraction=0.1', '--conf', 'spark.network.timeout=300s']
    if native_adam_path is None:
        docker_parameters = ['--log-driver', 'none', master_ip.docker_parameters(['--net=host'])]
        dockerCall(job=job, tool='quay.io/ucsc_cgl/adam:962-ehf--6e7085f8cac4b9a927dc9fb06b48007957256b80', dockerParameters=docker_parameters, parameters=_make_parameters(master_ip, default_params, memory, arguments, override_parameters))
    else:
        check_call([os.path.join(native_adam_path, 'bin/adam-submit')] + default_params + arguments)