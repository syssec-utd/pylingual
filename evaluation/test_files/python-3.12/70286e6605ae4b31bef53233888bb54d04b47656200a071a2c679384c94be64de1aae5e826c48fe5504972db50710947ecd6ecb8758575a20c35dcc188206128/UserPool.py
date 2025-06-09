from volworld_common.util.id_util import new_rand_test_user_name
from volworld_aws_api_common.test.aws.request.post__signup import act__signup
from volworld_aws_api_common.test.aws.request.post__login import act__login
from volworld_aws_api_common.api.AA import AA
from volworld_common.test.behave.BehaveUtil import BehaveUtil
from volworld_aws_api_common.test.behave.ACotA import ACotA

class UserInfo:

    def __init__(self, name: str, password: str=None):
        self.name = name
        self.used_name = f'{self.name}xxxxxx{new_rand_test_user_name()}'
        self.password = password
        self.token = None
        self.login_info = None

    def signup(self):
        login = act__signup(self.used_name, self.password)
        assert login[AA.Name] == self.used_name
        self.password = login[AA.Password]

    def login(self, forced=False):
        if not forced and self.login_info is not None:
            return
        self.login_info = act__login(self.used_name, self.password)
        self.token = self.login_info[AA.Token]
        return self.login_info

class UserPool:

    def __init__(self):
        self.users = dict()

    def get_user(self, name: str) -> UserInfo:
        name = BehaveUtil.clear_string(name)
        if name not in self.users:
            return None
        return self.users[name]

    def get_login_user(self, name: str) -> UserInfo:
        user = self.get_user(name)
        user.login()
        return user

    def add_user(self, name: str, password: str=None) -> UserInfo:
        name = BehaveUtil.clear_string(name)
        assert name not in self.users
        self.users[name] = UserInfo(name, password)
        return self.users[name]

    def add_signup_user(self, name: str, password: str=None) -> UserInfo:
        name = BehaveUtil.clear_string(name)
        assert name not in self.users
        inf = UserInfo(name, password)
        self.users[name] = inf
        inf.signup()
        return inf

    def login(self, context, name):
        name = BehaveUtil.clear_string(name)
        user: UserInfo = self.users[name]
        assert user is not None
        if hasattr(context, 'curr_login_user'):
            if getattr(context, ACotA.LoginUser) == user:
                return
        curr_login_name = 'None'
        if hasattr(context, ACotA.LoginUser):
            curr_login_name = getattr(context, ACotA.LoginUser).name
        print(f'Need to login [{name}], current login is [{curr_login_name}]')
        user.login()
        setattr(context, ACotA.LoginUser, user)
        return user