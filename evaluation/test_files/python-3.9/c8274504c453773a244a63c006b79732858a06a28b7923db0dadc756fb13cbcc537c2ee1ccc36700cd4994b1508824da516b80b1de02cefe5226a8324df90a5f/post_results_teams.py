from junitparser import JUnitXml, TestSuite, TestCase
from collections import defaultdict
import requests
import os
import logging
'\n-------------------------------------------------------------------\nRead the junit xml file and post into Teams channel\n-------------------------------------------------------------------\n'
class_set = set()
project_name = None

def post_reports_to_teams(build_url, webhook_url):
    global class_set
    result_dict = defaultdict(list)
    xml = get_xml_report()
    if xml.tests > 0:
        for suite in xml:
            for case in suite:
                if case.classname and 'tests' in case.classname:
                    class_set.add(case.classname)
                    result_dict[get_feature_name(case.classname)].append(translate_result(case.result))
        create_payload(generate_result(result_dict), xml, build_url, webhook_url)

def translate_result(result):
    result_list = ['failure', 'skipped', 'error']
    if len(result) > 0:
        test = str(result).split(' ')[1].replace("'", '')
        if test in result_list:
            return 'SKIPPED' if test in 'error' else test.upper()
    else:
        return 'PASSED'

def get_provider(provider):
    sorted_class = sorted(class_set)
    for class_name in sorted_class:
        if provider in class_name:
            return class_name.split('.')[1]

def generate_result(result):
    payload_data = ''
    global project_name
    for (key, values) in result.items():
        project_name = get_provider(key)
        res_dict = {}
        for value in values:
            if res_dict.get(value):
                res_dict[value] = res_dict.get(value) + 1
            else:
                res_dict[value] = 1
        final_data = project_name.upper() + ' - ' + key.replace('_', ' ').title() + ' - ' + 'Passed: ' + integer(res_dict.get('PASSED')) + ' ' + 'Failed: ' + integer(res_dict.get('FAILURE')) + ' ' + 'Skipped: ' + integer(res_dict.get('SKIPPED'))
        payload_data += final_data + '<br>'
    return payload_data

def create_payload(final_payload, xml, build_url, webhook_url):
    total_tests = int(xml.tests)
    failed_error_skipped = xml.failures + xml.skipped + xml.errors
    failed_tests = xml.failures
    passed_tests = xml.tests - failed_error_skipped
    if passed_tests > 0 or failed_tests > 0:
        pass_percent = round(float(passed_tests * 100 / total_tests), 2)
        payload = f"**UI Automation Test Results:** <br><br>**Project:** {project_name.upper()}<br>**Environment:** {build_url}<br>**Build:** {build_url}<br><br>**Total TestCases Executed:** {total_tests}<br>**Passed:** {passed_tests}<br>**Failed:** {xml.failures}<br>**Skipped:** {xml.skipped + xml.errors}<br>**Pass Percentage:** {pass_percent}{'%'}<br><br>**Feature-wise Summary:**<br> " + '<br>'
        payload += final_payload
    else:
        payload = f'**UI Automation Test Results:** <br>**Project:** {project_name.upper()}<br>**Environment:** https://{build_url}<br>**Build:** {build_url}<br><br>All the test cases are skipped please look into it'
    post_request(payload, webhook_url)
    print(payload)

def post_request(payload, webhook_url):
    headers = {'Content-Type': 'application/json'}
    team_response = requests.post(url=webhook_url, json={'text': payload}, headers=headers)
    if team_response.status_code == 200:
        logging.info('<br> Successfully posted UI test execution pytest report on Teams channel')
    else:
        logging.info('<br> Something went wrong. Unable to post ui test execution pytest report on Teams channel.<br>Response:')

def get_xml_report():
    test_report_file = os.getcwd() + '//junitresults.xml'
    xml = JUnitXml.fromfile(test_report_file)
    return xml

def get_feature_name(class_name):
    feature_name = class_name.split('_')
    del feature_name[0:1]
    return '_'.join(feature_name)

def integer(value):
    return str(0) if value is None else str(value)

def main(args):
    if args.teams_report_flag.lower() == 'yes':
        post_reports_to_teams(args.build)
    pass
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--teams', dest='teams_report_flag', default='no', help='Post the test report on teams channel: Y or N')
    parser.add_argument('--build', required=False, help='Jenkins Pipeline url')
    main(parser.parse_args())
    exit(main(parser.parse_args()))