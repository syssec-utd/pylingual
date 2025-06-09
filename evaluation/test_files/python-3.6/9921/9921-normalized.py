def has_code(state, text, pattern=True, not_typed_msg=None):
    """Test the student code.

    Tests if the student typed a (pattern of) text. It is advised to use ``has_equal_ast()`` instead of ``has_code()``,
    as it is more robust to small syntactical differences that don't change the code's behavior.

    Args:
        text (str): the text that is searched for
        pattern (bool): if True (the default), the text is treated as a pattern. If False, it is treated as plain text.
        not_typed_msg (str): feedback message to be displayed if the student did not type the text.

    :Example:

        Student code and solution code::

            y = 1 + 2 + 3

        SCT::

            # Verify that student code contains pattern (not robust!!):
            Ex().has_code(r"1\\s*\\+2\\s*\\+3")

    """
    if not not_typed_msg:
        if pattern:
            not_typed_msg = 'Could not find the correct pattern in your code.'
        else:
            not_typed_msg = 'Could not find the following text in your code: %r' % text
    student_code = state.student_code
    _msg = state.build_message(not_typed_msg)
    state.do_test(StringContainsTest(student_code, text, pattern, Feedback(_msg, state)))
    return state