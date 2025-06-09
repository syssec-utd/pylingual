def guard_entire(requirements, identity=None, throws=None, on_fail=None):
    """
    Used to protect an entire blueprint with a set of requirements. If a route
    handler inside the blueprint should be exempt, then it may be decorated
    with the :func:`~flask_allows.views.exempt_from_requirements` decorator.

    This function should be registered as a before_request handler on the
    blueprint and provided with the requirements to guard the blueprint with::

        my_bp = Blueprint(__name__, 'namespace')
        my_bp.before_request(guard_entire(MustBeLoggedIn()))

    ``identity``, ``on_fail`` and ``throws`` may also be provided but are optional.
    If on_fails returns a non-None result, that will be considered the return
    value of the routing::


        from flask import flash, redirect

        def flash_and_redirect(message, level, endpoint):
            def _(*a, **k):
                flash(message, level)
                return redirect(endpoint)
            return _

        bp = Blueprint(__name__, 'namespace')
        bp.before_request(
            guard_entire(
                [MustBeLoggedIn()],
                on_fail=flash_and_redirect(
                    "Please login in first",
                    "warning",
                    "login"
                )
            )
        )

    ``on_fail`` will also receive anything found in
    ``flask.request.view_args`` as keyword arguments.

    If needed, this guard may be applied multiple times. This may be useful
    if different conditions should result in different `on_fail` mechanisms
    being invoked::

        bp = Blueprint(__name__, "admin_panel")
        bp.before_request(
            guard_entire(
                [MustBeLoggedIn()],
                on_fail=flash_and_redirect(
                    "Please login in first",
                    "warning",
                    "login"
                )
            )
        )
        bp.before_request(
            guard_entire(
                [MustBeAdmin()],
                on_fail=flash_and_redirect(
                    "You are not an admin.",
                    "danger",
                    "index"
                )
            )
        )

    :param requirements: An iterable of requirements to apply to every request
        routed to the blueprint.
    :param identity: Optional. The identity that should be used for fulfilling
        requirements on the blueprint level.
    :param throws: Optional. Exception or exception type to be thrown if
        authorization fails.
    :param on_fail: Optional. Value or function to use if authorization fails.

    .. versionadded: 0.7.0
    """

    def guarder():
        if _should_run_requirements():
            return allows.run(requirements, identity=identity, on_fail=on_fail, throws=throws, f_kwargs=request.view_args)
        return None
    return guarder