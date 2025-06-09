from b_lambda_layer_common.ssm.ssm_parameter import SSMParameter
from .dummy_ssm_client import DummySsmClient

def test_FUNC_refresh_AND_value_WITH_multiple_calls_EXPECT_values_refreshed():
    """
    Test whether the parameter can fetch and refreshed from SSM.

    :return: No return.
    """
    dummy_client = DummySsmClient()
    assert dummy_client.get_parameters_function_calls == 0
    parameter = SSMParameter(param_name='TestParameter', ssm_client=dummy_client)
    assert dummy_client.get_parameters_function_calls == 0
    value1 = parameter.value
    assert dummy_client.get_parameters_function_calls == 1
    value2 = parameter.value
    assert dummy_client.get_parameters_function_calls == 1
    assert value1 == value2
    parameter.refresh()
    assert dummy_client.get_parameters_function_calls == 2
    value3 = parameter.value
    assert dummy_client.get_parameters_function_calls == 2
    assert value1 == value2 and value2 != value3

def test_FUNC_refresh_on_error_WITH_multiple_decorators_EXPECT_values_refreshed():
    """
    Test whether the decorators work.

    :return: No return.
    """
    dummy_client = DummySsmClient()
    parameter = SSMParameter(param_name='TestParameter', ssm_client=dummy_client)
    outer_decorator_callbacks = 0
    inner_decorator_callbacks = 0

    def callback_function_outer():
        nonlocal outer_decorator_callbacks
        outer_decorator_callbacks += 1

    def callback_function_inner():
        nonlocal inner_decorator_callbacks
        inner_decorator_callbacks += 1

    @parameter.refresh_on_error(error_callback=callback_function_outer)
    @parameter.refresh_on_error(error_callback=callback_function_inner)
    def decorated_function():
        nonlocal inner_decorator_callbacks
        nonlocal outer_decorator_callbacks
        print(parameter.value)
        if inner_decorator_callbacks == 0 or outer_decorator_callbacks == 0:
            raise Exception('Lets raise some exceptions!')
    decorated_function()
    assert outer_decorator_callbacks == 1
    assert inner_decorator_callbacks == 1
    assert dummy_client.get_parameters_function_calls == 3