def keystone(*arg):
    """
    Swift annotation for adding function to process keystone notification.

    if event_type include wildcard, will put {pattern: function} into process_wildcard dict
    else will put {event_type: function} into process dict

    :param arg: event_type of notification
    """
    check_event_type(Openstack.Keystone, *arg)
    event_type = arg[0]

    def decorator(func):
        if event_type.find('*') != -1:
            event_type_pattern = pre_compile(event_type)
            keystone_customer_process_wildcard[event_type_pattern] = func
        else:
            keystone_customer_process[event_type] = func
        log.info('add function {0} to process event_type:{1}'.format(func.__name__, event_type))

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        return wrapper
    return decorator