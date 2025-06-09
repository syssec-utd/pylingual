def send_to_output(master_dict, mash_output, sample_id, assembly_file):
    """Send dictionary to output json file
    This function sends master_dict dictionary to a json file if master_dict is
    populated with entries, otherwise it won't create the file

    Parameters
    ----------
    master_dict: dict
        dictionary that stores all entries for a specific query sequence
        in multi-fasta given to mash dist as input against patlas database
    last_seq: str
        string that stores the last sequence that was parsed before writing to
        file and therefore after the change of query sequence between different
        rows on the input file
    mash_output: str
        the name/path of input file to main function, i.e., the name/path of
        the mash dist output txt file.
    sample_id: str
        The name of the sample being parse to .report.json file

    Returns
    -------

    """
    plot_dict = {}
    if master_dict:
        out_file = open('{}.json'.format(''.join(mash_output.split('.')[0])), 'w')
        out_file.write(json.dumps(master_dict))
        out_file.close()
        for k, v in master_dict.items():
            if not v[2] in plot_dict:
                plot_dict[v[2]] = [k]
            else:
                plot_dict[v[2]].append(k)
        number_hits = len(master_dict)
    else:
        number_hits = 0
    json_dic = {'tableRow': [{'sample': sample_id, 'data': [{'header': 'Mash Dist', 'table': 'plasmids', 'patlas_mashdist': master_dict, 'value': number_hits}]}], 'plotData': [{'sample': sample_id, 'data': {'patlasMashDistXrange': plot_dict}, 'assemblyFile': assembly_file}]}
    with open('.report.json', 'w') as json_report:
        json_report.write(json.dumps(json_dic, separators=(',', ':')))