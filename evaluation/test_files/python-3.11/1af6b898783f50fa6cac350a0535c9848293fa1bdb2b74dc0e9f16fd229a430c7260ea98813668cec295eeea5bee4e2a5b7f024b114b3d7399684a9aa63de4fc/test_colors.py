def test_colors_get_printed(pytester):
    pytester.copy_example('examples/test_example.py')
    pytester.makepyfile(__init__='')
    result = pytester.runpytest('-s')
    result.assert_outcomes(passed=1)
    bold, reset = ('\x1b[1m', '\x1b[0m')
    result.stdout.fnmatch_lines([f'*{bold}\x1b[31mtest_colors: this should be red{reset}', f'*{bold}\x1b[32mtest_colors: this should be green{reset}', f'*{bold}\x1b[33mtest_colors: this should be yellow{reset}', f'*{bold}\x1b[34mtest_colors: this should be blue{reset}', f'*{bold}\x1b[35mtest_colors: this should be magenta{reset}', f'*{bold}\x1b[36mtest_colors: this should be cyan{reset}'])