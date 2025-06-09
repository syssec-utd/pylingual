def check_call(state, callstr, argstr=None, expand_msg=None):
    """When checking a function definition of lambda function,
    prepare has_equal_x for checking the call of a user-defined function.

    Args:
        callstr (str): call string that specifies how the function should be called, e.g. `f(1, a = 2)`.
           ``check_call()`` will replace ``f`` with the function/lambda you're targeting.
        argstr (str): If specified, this overrides the way the function call is refered to in the expand message.
        expand_msg (str): If specified, this overrides any messages that are prepended by previous SCT chains.
        state (State): state object that is chained from.

    :Example:

        Student and solution code::

            def my_power(x):
                print("calculating sqrt...")
                return(x * x)

        SCT::

            Ex().check_function_def('my_power').multi(
                check_call("f(3)").has_equal_value()
                check_call("f(3)").has_equal_output()
            )
    """
    state.assert_is(['function_defs', 'lambda_functions'], 'check_call', ['check_function_def', 'check_lambda_function'])
    if expand_msg is None:
        expand_msg = 'To verify it, we reran {{argstr}}. '
    stu_part, _argstr = build_call(callstr, state.student_parts['node'])
    sol_part, _ = build_call(callstr, state.solution_parts['node'])
    append_message = {'msg': expand_msg, 'kwargs': {'argstr': argstr or _argstr}}
    child = part_to_child(stu_part, sol_part, append_message, state)
    return child