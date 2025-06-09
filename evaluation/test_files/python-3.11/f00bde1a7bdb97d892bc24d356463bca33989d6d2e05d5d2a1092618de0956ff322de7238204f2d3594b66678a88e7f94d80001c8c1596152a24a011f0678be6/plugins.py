"""
The plugins module defines the components used by the rest of insights and
specializes their interfaces and execution model where required.

This module includes the following :class:`CompoentType` subclasses:

    - :class:`datasource`
    - :class:`parser`
    - :class:`combiner`
    - :class:`rule`
    - :class:`condition`
    - :class:`incident`
    - :class:`fact`

It also contains the following :class:`Response` subclasses that :class:`rules`
may return:

    - :class:`make_pass`
    - :class:`make_response` (alias for make_fail)
    - :class:`make_fail`
    - :class:`make_info`
    - :class:`make_metadata`
    - :class:`make_metadata_key`
    - :class:`make_fingerprint`

"""
from __future__ import print_function
import logging
import traceback
from pprint import pformat
from six import StringIO
from insights.core import dr
from insights.util.subproc import CalledProcessError
from insights import settings
log = logging.getLogger(__name__)

class ContentException(dr.SkipComponent):
    """ Raised whenever a :class:`datasource` fails to get data. """
    pass

class PluginType(dr.ComponentType):
    """
    PluginType is the base class of plugin types like datasource, rule, etc.
    It provides a default invoke method that catches exceptions we don't
    want bubbling to the top of the evaluation loop. These exceptions are
    commonly raised by datasource components but could be in the context of any
    component since most datasource runtime errors are lazy.

    It's possible for a datasource to "succeed" and return an object but for an
    exception to be raised when the parser tries to access the content of that
    object. For example, when a command datasource is evaluated, it only checks
    that the command exists and is executable. Invocation of the command itself
    is delayed until the parser asks for its value. This helps with performance
    and memory consumption.
    """

    def invoke(self, broker):
        try:
            return super(PluginType, self).invoke(broker)
        except ContentException as ce:
            log.debug(ce)
            broker.add_exception(self.component, ce, traceback.format_exc())
            raise dr.SkipComponent()
        except CalledProcessError as cpe:
            log.debug(cpe)
            broker.add_exception(self.component, cpe, traceback.format_exc())
            raise dr.SkipComponent()

class component(PluginType):
    pass

class datasource(PluginType):
    """
    Decorates a component that one or more :class:`insights.core.Parser`
    subclasses will consume.
    """
    multi_output = False
    raw = False
    filterable = False

    def invoke(self, broker):
        try:
            return self.component(broker)
        except ContentException as ce:
            log.debug(ce)
            broker.add_exception(self.component, ce, traceback.format_exc())
            raise dr.SkipComponent()
        except CalledProcessError as cpe:
            log.debug(cpe)
            broker.add_exception(self.component, cpe, traceback.format_exc())
            raise dr.SkipComponent()

class parser(PluginType):
    """
    Decorates a component responsible for parsing the output of a
    :class:`datasource`. ``@parser`` should accept multiple arguments, the first
    will ALWAYS be the datasource the parser component should handle.
    Any subsequent argument will be a ``component`` used to determine if
    the parser should fire.
    ``@parser`` should only decorate subclasses of :class:`insights.core.Parser`.

    .. warning::
        If a Parser component handles a datasource that returns a ``list``, a
        Parser instance will be created for each element of the list. Combiners
        or rules that depend on the Parser will be passed the list of instances
        and **not** a single parser instance. By default, if any parser in the
        list succeeds, those parsers are passed on to dependents, even if
        others fail. If all parsers should succeed or fail together, pass
        ``continue_on_error=False``.
    """

    def __init__(self, *args, **kwargs):
        group = kwargs.get('group', dr.GROUPS.single)
        self.continue_on_error = kwargs.get('continue_on_error', True)
        super(parser, self).__init__(*args, group=group)

    def invoke(self, broker):
        dep_value = broker[self.requires[0]]
        exception = False
        if not isinstance(dep_value, list):
            try:
                return self.component(dep_value)
            except ContentException as ce:
                log.debug(ce)
                broker.add_exception(self.component, ce, traceback.format_exc())
                exception = True
            except CalledProcessError as cpe:
                log.debug(cpe)
                broker.add_exception(self.component, cpe, traceback.format_exc())
                exception = True
        if exception:
            raise dr.SkipComponent()
        results = []
        for d in dep_value:
            try:
                r = self.component(d)
                if r is not None:
                    results.append(r)
            except dr.SkipComponent:
                pass
            except ContentException as ce:
                log.debug(ce)
                broker.add_exception(self.component, ce, traceback.format_exc())
                if not self.continue_on_error:
                    exception = True
                    break
            except CalledProcessError as cpe:
                log.debug(cpe)
                broker.add_exception(self.component, cpe, traceback.format_exc())
                if not self.continue_on_error:
                    exception = True
                    break
            except Exception as ex:
                tb = traceback.format_exc()
                log.warn(tb)
                broker.add_exception(self.component, ex, tb)
                if not self.continue_on_error:
                    exception = True
                    break
        if exception:
            raise dr.SkipComponent()
        if not results:
            log.debug('All failed: %s' % dr.get_name(self.component))
            raise dr.SkipComponent()
        return results

class metadata(parser):
    """
    Used for old cluster uber-archives.

    .. deprecated:: 1.x

    .. warning::
        Do not use this component type.
    """
    requires = ['metadata.json']

class combiner(PluginType):
    """
    A decorator for a component that composes or "combines" other components.

    A typical use case is hiding slight variations in related parser
    interfaces. Another use case is to combine several related parsers behind a
    single, cohesive, higher level interface.
    """
    pass

class remoteresource(PluginType):
    """ ComponentType for a component for remote web resources. """
    pass

class rule(PluginType):
    """
    Decorator for components that encapsulate some logic that depends on the
    data model of a system. Rules can depend on :class:`datasource` instances,
    :class:`parser` instances, :class:`combiner` instances, or anything else.

    For example:

    .. code-block:: python

       @rule(SshDConfig, InstalledRpms, [ChkConfig, UnitFiles], optional=[IPTables, IpAddr])
       def report(sshd_config, installed_rpms, chk_config, unit_files, ip_tables, ip_addr):
           # ...
           # ... some complicated logic
           # ...
           bash = installed_rpms.newest("bash")
           return make_pass("BASH", bash=bash)

    Notice that the arguments to ``report`` correspond to the dependencies in
    the ``@rule`` decorator and are in the same order.

    Parameters to the decorator have these forms:

    ============  ===============================  ==========================
    Criteria      Example Decorator Arguments      Description
    ============  ===============================  ==========================
    Required      ``SshDConfig, InstalledRpms``    Regular arguments
    At Least One  ``[ChkConfig, UnitFiles]``       An argument as a list
    Optional      ``optional=[IPTables, IpAddr]``  A list following optional=
    ============  ===============================  ==========================

    If a parameter is required, the value provided for it is guaranteed not to
    be ``None``. In the example above, ``sshd_config`` and ``installed_rpms``
    will not be ``None``.

    At least one of the arguments to parameters of an "at least one"
    list will not be ``None``. In the example, either or both of ``chk_config``
    and ``unit_files`` will not be ``None``.

    Any or all arguments for optional parameters may be ``None``.

    The following keyword arguments may be passed to the decorator:

    Keyword Args:
        requires (list) **deprecated**: a list of components that all
            components decorated with this type will require. Instead of using
            ``requires=[...]``, just pass dependencies as variable arguments
            to ``@rule`` as in the example above.
        optional (list): a list of components that all components decorated with
            this type will implicitly depend on optionally. Additional components
            passed as ``optional`` to the decorator will be appended to this list.
        metadata (dict): an arbitrary dictionary of information to associate
            with the component you're decorating. It can be retrieved with
            ``get_metadata``.
        tags (list): a list of strings that categorize the component. Useful for
            formatting output or sifting through results for components you care
            about.
        group: ``GROUPS.single`` or ``GROUPS.cluster``. Used to organize
            components into "groups" that run together with :func:`insights.core.dr.run`.
        cluster (bool): if ``True`` will put the component into the
            ``GROUPS.cluster`` group. Defaults to ``False``. Overrides ``group``
            if ``True``.
        content (string or dict): a jinja2 template or dictionary of jinja2
            templates. The :class:`Response` subclasses rules can return are
            dictionaries. :class:`make_pass`, :class:`make_fail`, and
            :class:`make_response` all accept first a key and then a list of
            arbitrary keyword arguments. If content is a dictionary, the key is
            used to look up the template that the rest of the keyword argments
            will be interpolated into. If content is a string, then it is used
            for all return values of the rule. If content isn't defined but a
            ``CONTENT`` variable is declared in the module, it will be used for
            every rule in the module and also can be a string or list of
            dictionaries
        links (dict): a dictionary with strings as keys and lists of urls as
            values. The keys categorize the urls, e.g. "kcs" for kcs urls and
            "bugzilla" for bugzilla urls.
    """
    content = None
    links = None

    def __init__(self, *args, **kwargs):
        super(rule, self).__init__(*args, **kwargs)
        self.content = kwargs.get('content')
        self.links = kwargs.get('links')

    def process(self, broker):
        """
        Ensures dependencies have been met before delegating to `self.invoke`.
        """
        if any((i in broker for i in dr.IGNORE.get(self.component, []))):
            raise dr.SkipComponent()
        missing = self.get_missing_dependencies(broker)
        if missing:
            return _make_skip(dr.get_name(self.component), missing)
        r = self.invoke(broker)
        if r is None:
            return make_none()
        if not isinstance(r, Response):
            raise Exception('rules must return Response objects.')
        return r

class condition(PluginType):
    """
    ComponentType used to encapsulate boolean logic you'd like to have analyzed
    by a rule analysis system. Conditions should return truthy values. ``None``
    is also a valid return type for conditions, so ``rules`` that depend on
    ``conditions`` that might return None should check their validity.
    """
    pass

class incident(PluginType):
    """
    ComponentType for a component used by rules that allows automated
    statistical analysis.
    """
    pass

class fact(PluginType):
    """
    ComponentType for a component that surfaces a dictionary or list of
    dictionaries that will be used later by cluster rules. The data from a fact
    is converted to a pandas Dataframe
    """
    pass

def is_type(component, _type):
    try:
        return issubclass(dr.get_component_type(component), _type)
    except:
        return False

def is_datasource(component):
    return is_type(component, datasource)

def is_parser(component):
    return is_type(component, parser)

def is_combiner(component):
    return is_type(component, combiner)

def is_rule(component):
    return is_type(component, rule)

def is_component(obj):
    return bool(dr.get_component_type(obj))

class ValidationException(Exception):

    def __init__(self, msg, r=None):
        if r:
            msg = '%s: %s' % (msg, r)
        super(ValidationException, self).__init__(msg)

class Response(dict):
    """
    Response is the base class of response types that can be returned from
    rules.

    Subclasses must call __init__ of this class via super() and must provide
    the response_type class attribute.

    The key_name class attribute is optional, but if one is specified, the
    first argument to __init__ must not be None. If key_name is None, then
    the first argument to __init__ should be None. It's best to override
    __init__ in subclasses so users aren't required to pass None explicitly.
    """
    response_type = None
    "\n    response_type is something like 'rule', 'metadata', 'fingerprint', etc. It\n    is how downstream systems identify the type of information returned by a\n    rule.\n    "
    key_name = None
    "\n    key_name is something like 'error_key', 'fingerprint_key', etc.  It is the\n    key downstream systems use to look up the exact response returned by a\n    rule.\n    "

    def __init__(self, key, **kwargs):
        self.validate_kwargs(kwargs)
        r = {'type': self.response_type}
        if self.key_name:
            self.validate_key(key)
            r[self.key_name] = key
        kwargs.update(r)
        kwargs = self.adjust_for_length(key, r, kwargs)
        super(Response, self).__init__(kwargs)

    def get_key(self):
        """
        Helper function that uses the response's key_name to look up the
        response identifier. For a rule, this is like
        response.get("error_key").
        """
        if self.key_name:
            return self.get(self.key_name)

    def validate_kwargs(self, kwargs):
        """
        Validates expected subclass attributes and constructor keyword
        arguments.
        """
        if not self.response_type:
            msg = 'response_type must be set on the Response subclass.'
            raise ValidationException(msg)
        if self.key_name and self.key_name in kwargs or 'type' in kwargs:
            name = self.__class__.__name__
            msg = '%s is an invalid argument for %s' % (self.key_name, name)
            raise ValidationException(msg)

    def validate_key(self, key):
        """ Called if the key_name class attribute is not None. """
        if not key:
            name = self.__class__.__name__
            msg = '%s response missing %s' % (name, self.key_name)
            raise ValidationException(msg, self)
        elif not isinstance(key, str):
            msg = 'Response contains invalid %s type' % self.key_name
            raise ValidationException(msg, type(key))

    def adjust_for_length(self, key, r, kwargs):
        """
        Converts the response to a string and compares its length to a max
        length specified in settings. If the response is too long, an error is
        logged, and an abbreviated response is returned instead.
        """
        length = len(str(kwargs))
        if length > settings.defaults['max_detail_length']:
            self._log_length_error(key, length)
            r['max_detail_length_error'] = length
            return r
        return kwargs

    def _log_length_error(self, key, length):
        """ Helper function for logging a response length error. """
        extra = {'max_detail_length': settings.defaults['max_detail_length'], 'len': length}
        if self.key_name:
            extra[self.key_name] = key
        msg = 'Length of data in %s is too long.' % self.__class__.__name__
        log.error(msg, extra=extra)

    def __str__(self):
        key_val = self.get_key()
        keys = sorted(self)
        if self.key_name in keys:
            keys.remove(self.key_name)
        if 'type' in keys:
            keys.remove('type')
        buf = StringIO()
        if not keys:
            print(key_val, file=buf)
            buf.seek(0)
            return buf.read()
        print('%s:' % key_val, file=buf)
        indent = len(max(keys, key=len)) + 6
        hang_indent = '\n' + ' ' * indent
        for k in keys:
            key = '    %s' % k + ' ' * (indent - len(k) - 6) + ': '
            buf.write(key)
            lines = pformat(self[k]).splitlines()
            num_lines = len(lines)
            if num_lines > 10:
                lines = lines[:10]
                lines.append('<...%s more lines...>' % (num_lines - 10))
            out = hang_indent.join(lines)
            buf.write(out)
            buf.write('\n')
        buf.seek(0)
        return buf.read()

class make_response(Response):
    """
    Returned by a rule to signal that its conditions have been met.

    Example:

    .. code-block:: python

        # completely made up package
        buggy = InstalledRpms.from_package("bash-3.4.23-1.el7")

        @rule(InstalledRpms)
        def report(installed_rpms):
           bash = installed_rpms.newest("bash")
           if bash == buggy:
               return make_response("BASH_BUG_123", bash=bash)
           return make_pass("BASH", bash=bash)

    .. deprecated::
        Use :class:`make_fail` instead.
    """
    response_type = 'rule'
    key_name = 'error_key'

class make_fail(make_response):
    """
    Returned by a rule to signal that its conditions have been met.

    Example:

    .. code-block:: python

        # completely made up package
        buggy = InstalledRpms.from_package("bash-3.4.23-1.el7")

        @rule(InstalledRpms)
        def report(installed_rpms):
           bash = installed_rpms.newest("bash")
           if bash == buggy:
               return make_fail("BASH_BUG_123", bash=bash)
           return make_pass("BASH", bash=bash)
    """
    pass

class make_pass(Response):
    """
    Returned by a rule to signal that its conditions explicitly have **not**
    been met. In other words, the rule has all of the information it needs to
    determine that the system it's analyzing is not in the state the rule was
    meant to catch.

    An example rule might check whether a system is vulnerable to a well
    defined exploit or has a bug in a specific version of a package. If it can
    say for sure "the system does not have this exploit" or "the system does
    not have the buggy version of the package installed", then it should return
    an instance of :class:`make_pass`.

    Example:

    .. code-block:: python

        # completely made up package
        buggy = InstalledRpms.from_package("bash-3.4.23-1.el7")

        @rule(InstalledRpms)
        def report(installed_rpms):
           bash = installed_rpms.newest("bash")
           if bash == buggy:
               return make_fail("BASH_BUG_123", bash=bash)
           return make_pass("BASH", bash=bash)

    """
    response_type = 'pass'
    key_name = 'pass_key'

class make_info(Response):
    """
    Returned by a rule to surface information about a system.

    Example:

    .. code-block:: python

        @rule(InstalledRpms)
        def report(rpms):
           bash = rpms.newest("bash")
           return make_info("BASH_VERSION", bash=bash.nvra)

    """
    response_type = 'info'
    key_name = 'info_key'

class make_fingerprint(Response):
    response_type = 'fingerprint'
    key_name = 'fingerprint_key'

class make_metadata_key(Response):
    response_type = 'metadata_key'
    key_name = 'key'

    def __init__(self, key, value):
        super(make_metadata_key, self).__init__(key, value=value)

    def adjust_for_length(self, key, r, kwargs):
        return kwargs

class make_metadata(Response):
    """
    Allows a rule to convey addtional metadata about a system to downstream
    systems. It doesn't convey success or failure but purely information that
    may be aggregated with other make_metadata responses. As such, it has no
    response key.
    """
    response_type = 'metadata'

    def __init__(self, **kwargs):
        super(make_metadata, self).__init__(None, **kwargs)

class _make_skip(Response):
    """
    Called automatically whenever a rule's dependencies aren't met. Likely to
    be deprecated or have its semantics changed. Do not call explicitly from
    rules.
    """
    response_type = 'skip'

    def __str__(self):
        required = self.missing[0]
        at_least_one = self.missing[1]
        buf = StringIO()
        print('Missing Dependencies:', file=buf)
        if required:
            print('    Requires:', file=buf)
            for d in required:
                print('        %s' % dr.get_name(d), file=buf)
        if at_least_one:
            for alo in at_least_one:
                print('    At Least One Of:', file=buf)
                for d in alo:
                    print('        %s' % dr.get_name(d), file=buf)
        buf.seek(0)
        return buf.read()

    def __init__(self, rule_fqdn, missing):
        self.missing = missing
        details = dr.stringify_requirements(missing)
        super(_make_skip, self).__init__(None, rule_fqdn=rule_fqdn, reason='MISSING_REQUIREMENTS', details=details)

class make_none(Response):
    """
    Used to create a response for a rule that returns None

    This is not intended to be used by plugins, only infrastructure
    but it not private so that we can easily add it to reporting.
    """
    response_type = 'none'
    key_name = 'none_key'

    def __init__(self):
        super(make_none, self).__init__(key='NONE_KEY')