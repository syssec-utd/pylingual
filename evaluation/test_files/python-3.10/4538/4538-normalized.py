def _decode_agents_data(self, block):
    """
        decode agents jsons, count diffs
        """
    collect = []
    if block:
        for chunk in block.split('\n'):
            try:
                if chunk:
                    prepared_results = {}
                    jsn = json.loads(chunk)
                    for (ts, values) in jsn.iteritems():
                        for (key, value) in values.iteritems():
                            try:
                                (key_group, key_name) = (key.split('_')[0].split('-')[0], '_'.join(key.split('_')[1:]))
                            except:
                                (key_group, key_name) = (key.split('_')[0], '_'.join(key.split('_')[1:]))
                            if key_group in decoder.diff_metrics.keys():
                                if key_name in decoder.diff_metrics[key_group]:
                                    decoded_key = decoder.find_common_names(key)
                                    if self.prev_check:
                                        try:
                                            value = jsn[ts][key] - self.prev_check[key]
                                        except KeyError:
                                            logger.debug('There is no diff value for metric %s.\nTimestamp: %s. Is it initial data?', key, ts, exc_info=True)
                                            value = 0
                                        prepared_results[decoded_key] = value
                                else:
                                    decoded_key = decoder.find_common_names(key)
                                    prepared_results[decoded_key] = value
                            else:
                                decoded_key = decoder.find_common_names(key)
                                prepared_results[decoded_key] = value
                        self.prev_check = jsn[ts]
                        collect.append((ts, prepared_results))
            except ValueError:
                logger.error('Telegraf agent send trash to output: %s', chunk)
                logger.debug('Telegraf agent data block w/ trash: %s', exc_info=True)
                return []
            except BaseException:
                logger.error('Exception trying to parse agent data: %s', chunk, exc_info=True)
                return []
        if collect:
            return collect