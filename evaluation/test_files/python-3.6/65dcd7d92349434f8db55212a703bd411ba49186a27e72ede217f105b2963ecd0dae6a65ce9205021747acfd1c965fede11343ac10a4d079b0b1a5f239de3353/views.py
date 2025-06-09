"""Invenio module that adds userprofiles to the platform."""
from warnings import warn
from flask import Blueprint, current_app, flash, render_template, request
from flask_babelex import lazy_gettext as _
from flask_breadcrumbs import register_breadcrumb
from flask_login import current_user, login_required
from flask_menu import register_menu
from flask_security.confirmable import send_confirmation_instructions
from invenio_db import db
from invenio_theme.proxies import current_theme_icons
from speaklater import make_lazy_string
from .forms import EmailProfileForm, PreferencesForm, ProfileForm, VerificationForm, confirm_register_form_factory, register_form_factory
from .models import UserProfileProxy
blueprint = Blueprint('invenio_userprofiles', __name__, template_folder='templates')
blueprint_api_init = Blueprint('invenio_userprofiles_api_init', __name__, template_folder='templates')
blueprint_ui_init = Blueprint('invenio_userprofiles_ui_init', __name__)

def init_common(app):
    """Post initialization."""
    if app.config['USERPROFILES_EXTEND_SECURITY_FORMS']:
        security_ext = app.extensions['security']
        security_ext.confirm_register_form = confirm_register_form_factory(security_ext.confirm_register_form)
        security_ext.register_form = register_form_factory(security_ext.register_form)

@blueprint_ui_init.record_once
def init_ui(state):
    """Post initialization for UI application."""
    app = state.app
    init_common(app)
    app.register_blueprint(blueprint, url_prefix=app.config['USERPROFILES_PROFILE_URL'])

@blueprint_api_init.record_once
def init_api(state):
    """Post initialization for API application."""
    init_common(state.app)

@blueprint.app_template_filter()
def userprofile(value):
    """Retrieve user profile for a given user id."""
    warn('userprofile template filter is deprecated.', DeprecationWarning)
    return UserProfileProxy.get_by_userid(int(value))

@blueprint.route('/', methods=['GET', 'POST'])
@login_required
@register_menu(blueprint, 'settings.profile', _('%(icon)s Profile', icon=make_lazy_string(lambda : f'<i class="{current_theme_icons.user}"></i>')), order=0)
@register_breadcrumb(blueprint, 'breadcrumbs.settings.profile', _('Profile'))
def profile():
    """View for editing a profile."""
    verification_form = VerificationForm(formdata=None, prefix='verification')
    profile_form = profile_form_factory()
    preferences_form = PreferencesForm(formdata=None, obj=current_user, prefix='preferences')
    is_read_only = current_app.config.get('USERPROFILES_READ_ONLY', False)
    form = request.form.get('submit', None)
    if form == 'profile' and (not is_read_only):
        handle_profile_form(profile_form)
    elif form == 'verification':
        handle_verification_form(verification_form)
    elif form == 'preferences' and (not is_read_only):
        handle_preferences_form(preferences_form)
    return render_template(current_app.config['USERPROFILES_PROFILE_TEMPLATE'], profile_form=profile_form, verification_form=verification_form, preferences_form=preferences_form)

def profile_form_factory():
    """Create a profile form."""
    if current_app.config['USERPROFILES_EMAIL_ENABLED']:
        return EmailProfileForm(formdata=None, obj=current_user, prefix='profile')
    else:
        return ProfileForm(formdata=None, obj=current_user, prefix='profile')

def handle_verification_form(form):
    """Handle email sending verification form."""
    form.process(formdata=request.form)
    if form.validate_on_submit():
        send_confirmation_instructions(current_user)
        flash(_('Verification email sent.'), category='success')

def handle_profile_form(form):
    """Handle profile update form."""
    if current_app.config.get('USERPROFILES_READ_ONLY', False):
        return
    form.process(formdata=request.form)
    if form.validate_on_submit():
        email_changed = False
        datastore = current_app.extensions['security'].datastore
        with db.session.begin_nested():
            if current_app.config['USERPROFILES_EMAIL_ENABLED'] and form.email.data != current_user.email:
                email_changed = True
            form.populate_obj(current_user)
            db.session.add(current_user)
            datastore.mark_changed(id(db.session), uid=current_user.id)
        datastore.commit()
        if email_changed:
            send_confirmation_instructions(current_user)
            flash(_('Profile was updated. We have sent a verification email to %(email)s. Please check it.', email=current_user.email), category='success')
        else:
            flash(_('Profile was updated.'), category='success')

def handle_preferences_form(form):
    """Handle preferences form."""
    if current_app.config.get('USERPROFILES_READ_ONLY', False):
        return
    form.process(formdata=request.form)
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.add(current_user)
        current_app.extensions['security'].datastore.commit()
        flash(_('Preferences were updated.'), category='success')