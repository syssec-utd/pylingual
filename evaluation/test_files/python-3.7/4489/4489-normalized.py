def _read_data(self, lines):
    """
        Parse lines and return stats
        """
    results = []
    for line in lines:
        (timestamp, rps, instances) = line.split('\t')
        curr_ts = int(float(timestamp))
        if self.__last_ts < curr_ts:
            self.__last_ts = curr_ts
            results.append(self.stats_item(self.__last_ts, float(rps), float(instances)))
    return results