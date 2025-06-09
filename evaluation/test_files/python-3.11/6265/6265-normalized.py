def get_libraries(self, database=''):
    """return active enrichr library name.Offical API """
    lib_url = 'http://amp.pharm.mssm.edu/%sEnrichr/datasetStatistics' % database
    libs_json = json.loads(requests.get(lib_url).text)
    libs = [lib['libraryName'] for lib in libs_json['statistics']]
    return sorted(libs)