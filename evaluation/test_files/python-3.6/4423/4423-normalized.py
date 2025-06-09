def get_info(self):
    """ get merged info about phantom conf """
    result = copy.copy(self.streams[0])
    result.stat_log = self.stat_log
    result.steps = []
    result.ammo_file = ''
    result.rps_schedule = None
    result.ammo_count = 0
    result.duration = 0
    result.instances = 0
    result.loadscheme = []
    result.loop_count = 0
    for stream in self.streams:
        sec_no = 0
        logger.debug('Steps: %s', stream.stepper_wrapper.steps)
        for item in stream.stepper_wrapper.steps:
            for x in range(0, item[1]):
                if len(result.steps) > sec_no:
                    result.steps[sec_no][0] += item[0]
                else:
                    result.steps.append([item[0], 1])
                sec_no += 1
        if result.rps_schedule:
            result.rps_schedule = []
        else:
            result.rps_schedule = stream.stepper_wrapper.loadscheme
        if result.loadscheme:
            result.loadscheme = ''
        else:
            result.loadscheme = ''
        if result.loop_count:
            result.loop_count = u'0'
        else:
            result.loop_count = stream.stepper_wrapper.loop_count
        result.ammo_file += '{} '.format(stream.stepper_wrapper.ammo_file)
        result.ammo_count += stream.stepper_wrapper.ammo_count
        result.duration = max(result.duration, stream.stepper_wrapper.duration)
        result.instances += stream.instances
    if not result.ammo_count:
        raise ValueError('Total ammo count cannot be zero')
    return result