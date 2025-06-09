def get_library_name(database='Human'):
    """return enrichr active enrichr library name. 
    :param str database: Select one from { 'Human', 'Mouse', 'Yeast', 'Fly', 'Fish', 'Worm' } 
    
    """
    if database not in ['Human', 'Mouse', 'Yeast', 'Fly', 'Fish', 'Worm']:
        sys.stderr.write("No supported database. Please input one of these:\n                            'Human', 'Mouse', 'Yeast', 'Fly', 'Fish', 'Worm' ")
        return
    if database in ['Human', 'Mouse']:
        database = ''
    lib_url = 'http://amp.pharm.mssm.edu/%sEnrichr/datasetStatistics' % database
    libs_json = json.loads(requests.get(lib_url).text)
    libs = [lib['libraryName'] for lib in libs_json['statistics']]
    return sorted(libs)