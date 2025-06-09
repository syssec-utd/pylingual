def _check_required_files(self):
    """Checks whetner the trace and log files are available
        """
    if not os.path.exists(self.trace_file):
        raise eh.InspectionError('The provided trace file could not be opened: {}'.format(self.trace_file))
    if not os.path.exists(self.log_file):
        raise eh.InspectionError('The .nextflow.log files could not be opened. Are you sure you are in a nextflow project directory?')