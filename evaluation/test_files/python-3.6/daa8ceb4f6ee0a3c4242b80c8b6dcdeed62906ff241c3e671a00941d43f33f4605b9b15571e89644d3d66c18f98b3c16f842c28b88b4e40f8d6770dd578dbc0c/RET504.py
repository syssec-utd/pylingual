def x():
    a = 1
    return a

def get_bar_if_exists(obj):
    result = ''
    if hasattr(obj, 'bar'):
        result = str(obj.bar)
    return result

def x():
    formatted = _USER_AGENT_FORMATTER.format(format_string, **values)
    formatted = formatted.replace('()', '').replace('  ', ' ').strip()
    return formatted

def user_agent_username(username=None):
    if not username:
        return ''
    username = username.replace(' ', '_')
    try:
        username.encode('ascii')
    except UnicodeEncodeError:
        username = quote(username.encode('utf-8'))
    else:
        if '%' in username:
            username = quote(username)
    return username

def x(y):
    a = 1
    print(a)
    return a

def x():
    a = 1
    if y:
        return a
    a = a + 2
    print(a)
    return a

def x():
    a = {}
    a['b'] = 2
    return a

def x():
    a = []
    a.append(2)
    return a

def x():
    a = lambda x: x
    a()
    return a

def x():
    (b, a) = [1, 2]
    return a

def x():
    val = ''
    for i in range(5):
        val = val + str(i)
    return val

def x():
    val = ''
    i = 5
    while i:
        val = val + str(i)
        i = i - x
    return val

def x():
    a = 1
    print(f'a={a}')
    return a

def x():
    (b, a) = (1, 2)
    print(b)
    return a

def x():
    a = 1
    print()
    return a

class X:

    def x(self):
        a = self.property
        self.property = None
        return a

def resolve_from_url(self, url: str) -> dict:
    local_match = self.local_scope_re.match(url)
    if local_match:
        schema = get_schema(name=local_match.group(1))
        self.store[url] = schema
        return schema
    raise NotImplementedError(...)
my_dict = {}

def my_func():
    foo = calculate_foo()
    my_dict['foo_result'] = foo
    return foo

def no_exception_loop():
    success = False
    for _ in range(10):
        try:
            success = True
        except Exception:
            print('exception')
    return success

def no_exception():
    success = False
    try:
        success = True
    except Exception:
        print('exception')
    return success

def exception():
    success = True
    try:
        print('raising')
        raise Exception
    except Exception:
        success = False
    return success

def close(self):
    any_failed = False
    for task in self.tasks:
        try:
            task()
        except BaseException:
            any_failed = True
            report(traceback.format_exc())
    return any_failed

def global_assignment():
    global X
    X = 1
    return X

def nonlocal_assignment():
    X = 1

    def inner():
        nonlocal X
        X = 1
        return X

def decorator() -> Flask:
    app = Flask(__name__)

    @app.route('/hello')
    def hello() -> str:
        """Hello endpoint."""
        return 'Hello, World!'
    return app

def default():
    y = 1

    def f(x=y) -> X:
        return x
    return y

def get_queryset(option_1, option_2):
    queryset: Any = None
    queryset = queryset.filter(a=1)
    if option_1:
        queryset = queryset.annotate(b=Value(2))
    if option_2:
        queryset = queryset.filter(c=3)
    return queryset

def get_queryset():
    queryset = Model.filter(a=1)
    queryset = queryset.filter(c=3)
    return queryset

def get_queryset():
    queryset = Model.filter(a=1)
    return queryset

def str_to_bool(val):
    if isinstance(val, bool):
        return val
    val = val.strip().lower()
    if val in ('1', 'true', 'yes'):
        return True
    return False

def str_to_bool(val):
    if isinstance(val, bool):
        return val
    val = 1
    return val

def str_to_bool(val):
    if isinstance(val, bool):
        return some_obj
    return val