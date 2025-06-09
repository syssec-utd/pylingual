def ask_yes_no(prompt, default=None):
    """Asks a question and returns a boolean (y/n) answer.

    If default is given (one of 'y','n'), it is used if the user input is
    empty. Otherwise the question is repeated until an answer is given.

    An EOF is treated as the default answer.  If there is no default, an
    exception is raised to prevent infinite loops.

    Valid answers are: y/yes/n/no (match is not case sensitive)."""
    answers = {'y': True, 'n': False, 'yes': True, 'no': False}
    ans = None
    while ans not in answers.keys():
        try:
            ans = raw_input(prompt + ' ').lower()
            if not ans:
                ans = default
        except KeyboardInterrupt:
            pass
        except EOFError:
            if default in answers.keys():
                ans = default
                print()
            else:
                raise
    return answers[ans]