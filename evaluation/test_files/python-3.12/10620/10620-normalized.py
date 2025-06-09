def write_configs(self, project_root):
    """Wrapper method that writes all configuration files to the pipeline
        directory
        """
    with open(join(project_root, 'resources.config'), 'w') as fh:
        fh.write(self.resources)
    with open(join(project_root, 'containers.config'), 'w') as fh:
        fh.write(self.containers)
    with open(join(project_root, 'params.config'), 'w') as fh:
        fh.write(self.params)
    with open(join(project_root, 'manifest.config'), 'w') as fh:
        fh.write(self.manifest)
    if not exists(join(project_root, 'user.config')):
        with open(join(project_root, 'user.config'), 'w') as fh:
            fh.write(self.user_config)
    lib_dir = join(project_root, 'lib')
    if not exists(lib_dir):
        os.makedirs(lib_dir)
    with open(join(lib_dir, 'Helper.groovy'), 'w') as fh:
        fh.write(self.help)
    pipeline_to_json = self.render_pipeline()
    with open(splitext(self.nf_file)[0] + '.html', 'w') as fh:
        fh.write(pipeline_to_json)