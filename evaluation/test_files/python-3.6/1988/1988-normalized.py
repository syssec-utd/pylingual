def scrape_cloudsize_from_stdout(self, nodes_per_cloud):
    """
        Look at the stdout log and wait until the cluster of proper size is formed.
        This call is blocking.
        Exit if this fails.

        :param nodes_per_cloud:
        :return none
        """
    retries = 60
    while retries > 0:
        if self.terminated:
            return
        f = open(self.output_file_name, 'r')
        s = f.readline()
        while len(s) > 0:
            if self.terminated:
                return
            match_groups = re.search('Cloud of size (\\d+) formed', s)
            if match_groups is not None:
                size = match_groups.group(1)
                if size is not None:
                    size = int(size)
                    if size == nodes_per_cloud:
                        f.close()
                        return
            s = f.readline()
        f.close()
        retries -= 1
        if self.terminated:
            return
        time.sleep(1)
    print('')
    print('ERROR: Too many retries starting cloud.')
    print('')
    sys.exit(1)