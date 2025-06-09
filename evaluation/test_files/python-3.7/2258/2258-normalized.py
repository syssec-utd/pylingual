def save_dict():
    """
    Save the log scraping results into logs denoted by g_output_filename_failed_tests and
    g_output_filename_passed_tests.

    :return: none
    """
    global g_test_root_dir
    global g_output_filename_failed_tests
    global g_output_filename_passed_tests
    global g_output_pickle_filename
    global g_failed_test_info_dict
    if '2.build_id' not in g_failed_test_info_dict.keys():
        g_failed_test_info_dict['2.build_id'] = 'unknown'
    build_id = g_failed_test_info_dict['2.build_id']
    g_output_filename_failed_tests = g_output_filename_failed_tests + '_build_' + build_id + '_failed_tests.log'
    g_output_filename_passed_tests = g_output_filename_passed_tests + '_build_' + build_id + '_passed_tests.log'
    g_output_pickle_filename = g_output_pickle_filename + '_build_' + build_id + '.pickle'
    allKeys = sorted(g_failed_test_info_dict.keys())
    with open(g_output_pickle_filename, 'wb') as test_file:
        pickle.dump(g_failed_test_info_dict, test_file)
    text_file_failed_tests = open(g_output_filename_failed_tests, 'w')
    text_file_passed_tests = None
    allKeys = sorted(g_failed_test_info_dict.keys())
    write_passed_tests = False
    if 'passed_tests_info *********' in allKeys:
        text_file_passed_tests = open(g_output_filename_passed_tests, 'w')
        write_passed_tests = True
    for keyName in allKeys:
        val = g_failed_test_info_dict[keyName]
        if isinstance(val, list):
            if len(val) == 3:
                if keyName == 'failed_tests_info *********':
                    write_test_java_message(keyName, val, text_file_failed_tests)
                if keyName == 'passed_tests_info *********':
                    write_test_java_message(keyName, val, text_file_passed_tests)
            elif len(val) == 2:
                write_java_message(keyName, val, text_file_failed_tests)
                if write_passed_tests:
                    write_java_message(keyName, val, text_file_passed_tests)
        else:
            write_general_build_message(keyName, val, text_file_failed_tests)
            if write_passed_tests:
                write_general_build_message(keyName, val, text_file_passed_tests)
    text_file_failed_tests.close()
    if write_passed_tests:
        text_file_passed_tests.close()