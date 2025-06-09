def create_app(config_file=None, config=None):
    """Flask app factory function."""
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.jinja_env.add_extension('jinja2.ext.do')
    if config:
        app.config.update(config)
    if config_file:
        app.config.from_pyfile(config_file)
    app.mme_nodes = mme_nodes(app.config.get('MME_URL'), app.config.get('MME_TOKEN'))
    app.config['JSON_SORT_KEYS'] = False
    current_log_level = logger.getEffectiveLevel()
    coloredlogs.install(level='DEBUG' if app.debug else current_log_level)
    configure_extensions(app)
    register_blueprints(app)
    register_filters(app)
    if not (app.debug or app.testing) and app.config.get('MAIL_USERNAME'):
        configure_email_logging(app)

    @app.before_request
    def check_user():
        if not app.config.get('LOGIN_DISABLED') and request.endpoint:
            static_endpoint = 'static' in request.endpoint or 'report' in request.endpoint
            public_endpoint = getattr(app.view_functions[request.endpoint], 'is_public', False)
            relevant_endpoint = not (static_endpoint or public_endpoint)
            if relevant_endpoint and (not current_user.is_authenticated):
                next_url = '{}?{}'.format(request.path, request.query_string.decode())
                login_url = url_for('login.login', next=next_url)
                return redirect(login_url)
    return app