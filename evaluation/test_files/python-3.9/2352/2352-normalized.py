def extractPrintSaveIntermittens():
    """
    This function will print out the intermittents onto the screen for casual viewing.  It will also print out
    where the giant summary dictionary is going to be stored.

    :return: None
    """
    global g_summary_dict_intermittents
    localtz = time.tzname[0]
    for ind in range(len(g_summary_dict_all['TestName'])):
        if g_summary_dict_all['TestInfo'][ind]['FailureCount'] >= g_threshold_failure:
            addFailedTests(g_summary_dict_intermittents, g_summary_dict_all, ind)
    if len(g_summary_dict_intermittents['TestName']) > 0:
        json.dump(g_summary_dict_intermittents, open(g_summary_dict_name, 'w'))
        with open(g_summary_csv_filename, 'w') as summaryFile:
            for ind in range(len(g_summary_dict_intermittents['TestName'])):
                testName = g_summary_dict_intermittents['TestName'][ind]
                numberFailure = g_summary_dict_intermittents['TestInfo'][ind]['FailureCount']
                firstFailedTS = parser.parse(time.ctime(min(g_summary_dict_intermittents['TestInfo'][ind]['Timestamp'])) + ' ' + localtz)
                firstFailedStr = firstFailedTS.strftime('%a %b %d %H:%M:%S %Y %Z')
                recentFail = parser.parse(time.ctime(max(g_summary_dict_intermittents['TestInfo'][ind]['Timestamp'])) + ' ' + localtz)
                recentFailStr = recentFail.strftime('%a %b %d %H:%M:%S %Y %Z')
                eachTest = '{0}, {1}, {2}, {3}\n'.format(testName, recentFailStr, numberFailure, g_summary_dict_intermittents['TestInfo'][ind]['TestCategory'][0])
                summaryFile.write(eachTest)
                print('Intermittent: {0}, Last failed: {1}, Failed {2} times since {3}'.format(testName, recentFailStr, numberFailure, firstFailedStr))