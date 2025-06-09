from typing import Optional, Callable, Any, List
from cinnaroll_internal import constants, io_formats, model, rollout_config, utils

class ConfigParameterUndefinedError(Exception):
    ...

class ProjectIDError(Exception):
    ...

class InferFunctionNotImplementedError(Exception):
    ...

class UnknownFrameworkError(Exception):
    ...

def find_project_id_error(project_id: str) -> Optional[Exception]:
    return None

def find_infer_func_not_implemented_error(infer_func: Callable[[Any, Any], Any]) -> Optional[Exception]:
    if not utils.is_function_implemented(infer_func):
        return InferFunctionNotImplementedError('Infer function is not implemented. Implement it.')
    return None

def find_config_none_value_errors(config: rollout_config.RolloutConfig) -> List[Exception]:
    errors: List[Exception] = []
    config_parameters = {'project_id': config.project_id, 'model_object': config.model_object, 'infer_func_input_format': config.infer_func_input_format, 'infer_func_output_format': config.infer_func_output_format, 'model_input_sample': config.model_input_sample, 'infer_func_input_sample': config.infer_func_input_sample}
    for (name, value) in config_parameters.items():
        if value is None:
            errors.append(ConfigParameterUndefinedError(f'Required config parameter {name} is undefined (its value is None).'))
    return errors

def find_unknown_model_framework_error(model_object: Any) -> Optional[Exception]:
    if model.infer_framework(model_object) == constants.UNKNOWN_FRAMEWORK:
        return UnknownFrameworkError(f'Unknown machine learning framework used. Currently only {constants.VALID_FRAMEWORKS} are supported.')
    return None

def find_config_pre_training_errors(config: rollout_config.RolloutConfig) -> List[Exception]:
    errors: List[Exception] = []
    errors += find_config_none_value_errors(config)
    utils.append_if_not_none(errors, find_project_id_error(config.project_id))
    errors += io_formats.find_disallowed_io_format_errors(config.infer_func_input_format, config.infer_func_output_format)
    utils.append_if_not_none(errors, io_formats.find_infer_func_input_format_mismatch_error(config.infer_func_input_sample, config.infer_func_input_format))
    utils.append_if_not_none(errors, find_infer_func_not_implemented_error(config.infer))
    if config.model_object:
        utils.append_if_not_none(errors, find_unknown_model_framework_error(config.model_object))
    return errors