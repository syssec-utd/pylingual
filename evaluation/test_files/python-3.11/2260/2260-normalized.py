def update_summary_file():
    """
    Concatecate all log file into a summary text file to be sent to users
    at the end of a daily log scraping.

    :return: none
    """
    global g_summary_text_filename
    global g_output_filename_failed_tests
    global g_output_filename_passed_tests
    with open(g_summary_text_filename, 'a') as tempfile:
        write_file_content(tempfile, g_output_filename_failed_tests)
        write_file_content(tempfile, g_output_filename_passed_tests)