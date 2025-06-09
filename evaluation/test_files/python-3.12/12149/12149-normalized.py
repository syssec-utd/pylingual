def check():
    """
    Tested under EPlus 8.1.0 on Windows (Geoffroy).
    """
    epw_path = os.path.join(CONF.eplus_base_dir_path, 'WeatherData', 'USA_VA_Sterling-Washington.Dulles.Intl.AP.724030_TMY3.epw')
    idf_dir_path = os.path.join(CONF.eplus_base_dir_path, 'ExampleFiles')
    test_num = 0
    for file_num, file_name in enumerate(os.listdir(idf_dir_path)):
        if file_num < START_FILE_NUM:
            continue
        base, ext = os.path.splitext(file_name)
        if ext == '.idf':
            with tempfile.TemporaryDirectory() as simulation_dir_path:
                s = simulate(os.path.join(idf_dir_path, file_name), epw_path, simulation_dir_path if DEBUG_SIMUL_DIR_PATH is None else DEBUG_SIMUL_DIR_PATH)
                if s.exists('eio'):
                    eio = Eio(s.get_file_path('eio'))
                    test_num += 1
        if test_num == MAX_TESTS_NB:
            break