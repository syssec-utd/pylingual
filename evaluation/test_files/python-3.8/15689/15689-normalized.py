def _get_mount_path(self):
    """
        Returns the path of the mount point of the current container. If this method is invoked
        outside of a Docker container a NotInsideContainerError is raised. Likewise if the docker
        daemon is unreachable from inside the container a UserError is raised. This method is
        idempotent.
        """
    if self._mount_path is None:
        name = current_docker_container_id()
        if dockerd_is_reachable():
            blob = json.loads(subprocess.check_output(['docker', 'inspect', name]))
            mounts = blob[0]['Mounts']
            sock_mnt = [x['Source'] == x['Destination'] for x in mounts if 'docker.sock' in x['Source']]
            require(len(sock_mnt) == 1, 'Missing socket mount. Requires the following: docker run -v /var/run/docker.sock:/var/run/docker.sock')
            if len(mounts) == 2:
                require(all((x['Source'] == x['Destination'] for x in mounts)), 'Docker Src/Dst mount points, invoked with the -v argument, must be the same if only using one mount point aside from the docker socket.')
                work_mount = [x['Source'] for x in mounts if 'docker.sock' not in x['Source']]
            else:
                mirror_mounts = [x['Source'] for x in mounts if x['Source'] == x['Destination']]
                work_mount = [x for x in mirror_mounts if 'docker.sock' not in x]
                require(len(work_mount) == 1, 'Wrong number of mirror mounts provided, see documentation.')
            self._mount_path = work_mount[0]
            log.info('The work mount is: %s', self._mount_path)
        else:
            raise UserError('Docker daemon is not reachable, ensure Docker is being run with: "-v /var/run/docker.sock:/var/run/docker.sock" as an argument.')
    return self._mount_path