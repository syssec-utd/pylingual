import sys
from typing import List, Set, Tuple
import re
import decimal
import logging
import operator
import inspect
from urllib.parse import unquote, urlsplit
from html.parser import HTMLParser
import otree.constants
from otree import settings
from otree.currency import Currency
from otree.models import Participant, Session
from otree import common
from otree.common import get_dotted_name, get_admin_secret_code, get_models_module
from otree.database import db, session_scope
from otree.live import call_live_method_compat
ADMIN_SECRET_CODE = get_admin_secret_code()
logger = logging.getLogger('otree.bots')
INTERNAL_FORM_FIELDS = {'csrfmiddlewaretoken', 'must_fail', 'timeout_happened', 'admin_secret_code', 'error_fields'}
DISABLE_CHECK_HTML_INSTRUCTIONS = '\nChecking the HTML may not find all form fields and buttons\n(e.g. those added with JavaScript),\nso you can disable this check by yielding a Submission\nwith check_html=False, e.g.:\n\nyield Submission(pages.PageName, {{...}}, check_html=False)\n'
HTML_MISSING_BUTTON_WARNING = ("\nBot is trying to submit page {page_name},\nbut no button was found in the HTML of the page.\n(searched for <input> with type='submit' or <button> with type != 'button').\n" + DISABLE_CHECK_HTML_INSTRUCTIONS).replace('\n', ' ').strip()
HTML_MISSING_FIELD_WARNING = ('\nBot is trying to submit page {page_name} with fields: "{fields}",\nbut these form fields were not found in the HTML of the page\n(searched for tags {tags} with name= attribute matching the field name).\n' + DISABLE_CHECK_HTML_INSTRUCTIONS).replace('\n', ' ').strip()

class BOTS_CHECK_HTML:
    pass

class Submission:

    def __init__(self, PageClass, post_data=None, *, check_html=BOTS_CHECK_HTML, timeout_happened=False):
        post_data = post_data or {}
        post_data = post_data.copy()
        if check_html == BOTS_CHECK_HTML:
            check_html = settings.BOTS_CHECK_HTML
        if timeout_happened:
            post_data[otree.constants.timeout_happened] = True
            post_data[otree.constants.admin_secret_code] = ADMIN_SECRET_CODE
        if hasattr(PageClass, 'wait_for_all_groups'):
            msg = "Your bot yielded '{}', which is a wait page. You should delete this line, because bots handle wait pages automatically.".format(PageClass)
            raise AssertionError(msg)
        for key in post_data:
            if isinstance(post_data[key], Currency):
                post_data[key] = str(decimal.Decimal(post_data[key]))
        self.page_class = PageClass
        self.page_class_dotted: str = get_dotted_name(PageClass)
        self.post_data: dict = post_data
        self.check_html = check_html

class SubmissionMustFail(Submission):
    """lets you intentionally submit with invalid
    input to ensure it's correctly rejected"""

    def __init__(self, PageClass, post_data=None, *, check_html=BOTS_CHECK_HTML, error_fields=None):
        post_data = post_data or {}
        super().__init__(PageClass, post_data, check_html=check_html)
        self.post_data['must_fail'] = True
        if error_fields:
            self.post_data['error_fields'] = error_fields

class ExpectError(AssertionError):
    pass

def expect(*args):
    if len(args) == 2:
        (lhs, rhs) = args
        op = '=='
    elif len(args) == 3:
        (lhs, op, rhs) = args
    else:
        msg = f'expect() takes 2 or 3 arguments'
        raise ValueError(msg)
    operators = {'==': operator.eq, '!=': operator.ne, '>': operator.gt, '<': operator.lt, '>=': operator.ge, '<=': operator.le, 'in': lambda a, b: a in b, 'not in': lambda a, b: a not in b}
    if op not in operators:
        msg = f'"{op}" not allowed in expect()'
        raise ValueError(msg)
    res = operators[op](lhs, rhs)
    if not res:
        error_messages = {'==': f'Expected {rhs!r}, actual value is {lhs!r}', 'in': f'{lhs!r} was not found', 'not in': f'{lhs!r} was not expected but was found anyway'}
        default_msg = f'Assertion failed: {lhs!r} {op} {rhs!r}'
        msg = error_messages.get(op, default_msg)
        raise ExpectError(msg)

class ParticipantBot:

    def __init__(self, participant_or_code, *, player_bots, executed_live_methods=None):
        if isinstance(participant_or_code, str):
            participant = Participant.objects_get(code=participant_or_code)
        else:
            participant = participant_or_code
        self.participant_code = participant.code
        self.session_code = participant._session_code
        self._client = None
        self.url = None
        self._response = None
        self._html = None
        self.path = None
        self.submits = None
        if executed_live_methods is None:
            executed_live_methods = set()
        self.executed_live_methods = executed_live_methods
        for b in player_bots:
            b.participant_bot = self
        self.player_bots: List[PlayerBot] = player_bots
        self.submits_generator = self.get_submits()

    @property
    def client(self):
        if not self._client:
            self.load_client()
        return self._client

    def load_client(self):
        try:
            import requests
        except ModuleNotFoundError:
            sys.exit('You need to install requests to run bots ("pip3 install requests")')
        from starlette.testclient import TestClient
        from otree.asgi import app
        self._client: TestClient = TestClient(app)

    def open_start_url(self):
        start_url = common.participant_start_url(self.participant_code)
        self.response = self.client.get(start_url, allow_redirects=True)

    def get_next_submit(self):
        return next(self.submits_generator)

    def get_submits(self):
        for player_bot in self.player_bots:
            generator = player_bot.play_round()
            if generator is None:
                continue
            for submission in generator:
                if not isinstance(submission, Submission):
                    submission = BareYieldToSubmission(submission)
                self.assert_correct_page(submission, player_bot.player)
                self.assert_html_ok(submission)
                self.live_method_stuff(player_bot, submission)
                yield submission

    def live_method_stuff(self, player_bot, submission):
        PageClass = submission.page_class
        live_method = PageClass.live_method
        if live_method:
            record = (player_bot.player.group_id, PageClass)
            if record not in self.executed_live_methods:
                bots_module = inspect.getmodule(player_bot)
                method_calls_fn = getattr(bots_module, 'call_live_method', None)
                if method_calls_fn:
                    players = {p.id_in_group: p for p in player_bot.group.get_players()}

                    def method(id_in_group, data):
                        return call_live_method_compat(live_method, players[id_in_group], data)
                    method_calls_fn(method=method, case=player_bot.case, round_number=player_bot.round_number, page_class=PageClass, group=player_bot.group)
                    db.commit()
                self.executed_live_methods.add(record)

    def _play_individually(self):
        """convenience method for testing"""
        self.open_start_url()
        try:
            while True:
                submission = self.get_next_submit()
                self.submit(submission)
        except StopIteration:
            return

    def assert_html_ok(self, submission: Submission):
        if submission.check_html:
            fields_to_check = [f for f in submission.post_data if f not in INTERNAL_FORM_FIELDS]
            checker = PageHtmlChecker(fields_to_check)
            missing_fields = checker.get_missing_fields(self.html)
            if missing_fields:
                page_name = submission.page_class.url_name()
                raise MissingHtmlFormFieldError(HTML_MISSING_FIELD_WARNING.format(page_name=page_name, fields=', '.join(missing_fields), tags=', '.join(('<{}>'.format(tag) for tag in checker.field_tags))))
            if not checker.submit_button_found:
                page_name = submission.page_class.url_name()
                raise MissingHtmlButtonError(HTML_MISSING_BUTTON_WARNING.format(page_name=page_name))

    def assert_correct_page(self, submission, player):
        ClassName = submission.page_class.__name__
        if not f'/{ClassName}/' in self.path:
            from otree.lookup import get_page_lookup
            idx = int(self.path.rsplit('/', maxsplit=1)[-1])
            lookup = get_page_lookup(self.session_code, idx)
            expected = dict(app=type(player).__module__, round_number=player.round_number, page=ClassName)
            actual = dict(app=lookup.app_name, round_number=lookup.round_number, page=lookup.page_class.__name__)
            msg = f'Discrepancy between bot code and app code. Bot is trying to submit this page:\n{expected}\nBut the participant is actually here:\n{actual}\n'
            raise AssertionError(msg)

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, response):
        self.url = unquote(response.url)
        self.path = urlsplit(self.url).path
        self._response = response
        self.html = response.content.decode('utf-8')

    @property
    def html(self):
        return self._html

    @html.setter
    def html(self, html):
        self._html = HtmlString(normalize_html_whitespace(html))

    def on_wait_page(self):
        if not is_wait_page(self.response):
            return False
        self.response = self.client.get(self.url, allow_redirects=True)
        return is_wait_page(self.response)

    def submit(self, submission: Submission):
        post_data = submission.post_data
        pretty_post_data = bot_prettify_post_data(post_data)
        log_string = 'Submit ' + self.path
        if pretty_post_data:
            log_string += ', {}'.format(pretty_post_data)
        if post_data.get('must_fail'):
            log_string += ', SubmissionMustFail'
        if post_data.get('timeout_happened'):
            log_string += ', timeout_happened'
        logger.info(log_string)
        self.response = self.client.post(self.url, post_data, allow_redirects=True)

class PlayerBot:
    cases = []

    def __init__(self, case_number: int, app_name, player_pk: int, subsession_pk: int, session_pk, participant_code):
        models_module = get_models_module(app_name)
        self.PlayerClass = models_module.Player
        self.GroupClass = models_module.Group
        self.SubsessionClass = models_module.Subsession
        self._player_pk = player_pk
        self._subsession_pk = subsession_pk
        self._session_pk = session_pk
        self._participant_code = participant_code
        if case_number == None:
            case_number = 0
        cases = self.cases
        if len(cases) >= 1:
            self.case = cases[case_number % len(cases)]
        else:
            self.case = None

    def play_round(self):
        pass

    @property
    def player(self):
        return self.PlayerClass.objects_get(id=self._player_pk)

    @property
    def group(self):
        """can't cache self._group_pk because group can change"""
        return self.player.group

    @property
    def subsession(self):
        return self.SubsessionClass.objects_get(id=self._subsession_pk)

    @property
    def round_number(self):
        return self.player.round_number

    @property
    def participant(self):
        return Participant.objects_get(code=self._participant_code)

    @property
    def session(self):
        return Session.objects_get(id=self._session_pk)

    @property
    def html(self):
        return self.participant_bot.html

class MissingHtmlButtonError(AssertionError):
    pass

class MissingHtmlFormFieldError(AssertionError):
    pass

def BareYieldToSubmission(yielded_value):
    post_data = {}
    if isinstance(yielded_value, (list, tuple)):
        PageClass = yielded_value[0]
        if len(yielded_value) == 2:
            post_data = yielded_value[1]
    else:
        PageClass = yielded_value
    return Submission(PageClass, post_data)

def normalize_html_whitespace(html):
    html = html.replace('\n', ' ').replace('\r', ' ')
    html = re.sub('\\s+', ' ', html)
    return html

class HtmlString(str):

    def truncated(self):
        """
        Make output more readable by truncating everything before the
         {% content %} block. I also considered indenting the HTML,
         but minidom had a parse error, and BS4 modifies a lot of tags,
         didn't seem optimal.
        """
        div_str = '<div class="_otree-content">'
        i = self.index(div_str) + len(div_str)
        return '...' + self[i:]

    def __str__(self):
        return self.truncated()

    def __repr__(self):
        return self.truncated()

class PageHtmlChecker(HTMLParser, object):

    def __init__(self, fields_to_check):
        super().__init__()
        self.missing_fields = set(fields_to_check)
        self.field_tags = {'input', 'button', 'select', 'textarea'}
        self.submit_button_found = False

    def get_missing_fields(self, html):
        self.feed(html)
        return self.missing_fields

    def check_if_field(self, tag, attrs):
        if tag in self.field_tags:
            for (attr_name, attr_value) in attrs:
                if attr_name == 'name':
                    self.missing_fields.discard(attr_value)

    def check_if_button(self, tag, attrs):
        if not self.submit_button_found:
            if tag == 'button':
                for (attr_name, attr_value) in attrs:
                    if attr_name == 'type' and attr_value == 'button':
                        return
                self.submit_button_found = True
            if tag == 'input':
                for (attr_name, attr_value) in attrs:
                    if attr_name == 'type' and attr_value == 'submit':
                        self.submit_button_found = True

    def handle_starttag(self, tag, attrs):
        self.check_if_field(tag, attrs)
        self.check_if_button(tag, attrs)

def is_wait_page(response):
    return response.headers.get(otree.constants.wait_page_http_header) == otree.constants.get_param_truth_value

def bot_prettify_post_data(post_data):
    if hasattr(post_data, 'dict'):
        post_data = post_data.dict()
    return {k: v for (k, v) in post_data.items() if k not in INTERNAL_FORM_FIELDS}