def build_pipeline_string(self, forks):
    """Parses, filters and merge all possible pipeline forks into the
        final pipeline string

        This method checks for shared start and end sections between forks
        and merges them according to the shared processes::

            [[spades, ...], [skesa, ...], [...,[spades, skesa]]]
                -> [..., [[spades, ...], [skesa, ...]]]

        Then it defines the pipeline string by replacing the arrays levels
        to the flowcraft fork format::

            [..., [[spades, ...], [skesa, ...]]]
                -> ( ... ( spades ... | skesa ... ) )

        Parameters
        ----------
        forks : list
            List with all the possible pipeline forks.

        Returns
        -------
        str : String with the pipeline definition used as input for
        parse_pipeline
        """
    final_forks = []
    for i in range(0, len(forks)):
        needs_merge = [False, 0, 0, 0, 0, '']
        is_merged = False
        for i2 in range(0, len(forks[i])):
            for j in range(i, len(forks)):
                needs_merge[0] = False
                for j2 in range(0, len(forks[j])):
                    try:
                        j2_fork = forks[j][j2].split('|')
                    except AttributeError:
                        j2_fork = forks[j][j2]
                    if forks[i][i2] in j2_fork and (i2 == 0 or j2 == 0) and (i != j):
                        needs_merge[0] = True
                        needs_merge[1] = i
                        needs_merge[2] = i2
                        needs_merge[3] = j
                        needs_merge[4] = j2
                        needs_merge[5] = forks[i][i2]
                if needs_merge[0]:
                    index_merge_point = forks[needs_merge[3]][-1].index(needs_merge[5])
                    if needs_merge[2] == 0:
                        if len(forks[needs_merge[3]][-1]) < 2:
                            forks[needs_merge[3]] = forks[needs_merge[3]][:-1] + forks[needs_merge[1]][:]
                        else:
                            forks[needs_merge[3]][-1][index_merge_point] = forks[needs_merge[1]]
                    elif needs_merge[4] == 0:
                        if len(forks[needs_merge[3]][-1]) < 2:
                            forks[needs_merge[3]] = forks[needs_merge[3]][:-1] + forks[needs_merge[1]][:]
                        else:
                            forks[needs_merge[3]][-1][index_merge_point] = forks[needs_merge[1]]
                    is_merged = True
        if needs_merge[0] is not None and (not is_merged):
            if bool([nf for nf in forks[i] if '|' in nf]):
                continue
            final_forks.append(forks[i])
    if len(final_forks) == 1:
        final_forks = str(final_forks[0])
    pipeline_string = ' ' + str(final_forks).replace('[[', '( ').replace(']]', ' )').replace(']', ' |').replace(', [', ' ').replace("'", '').replace(',', '').replace('[', '')
    if pipeline_string[-1] == '|':
        pipeline_string = pipeline_string[:-1]
    to_search = ' {} '
    to_replace = ' {}={} '
    for key, val in self.process_to_id.items():
        pipeline_string = pipeline_string.replace(to_search.format(key), to_replace.format(key, val))
    return pipeline_string