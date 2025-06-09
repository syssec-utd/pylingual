"""
:Author: wang kui
:Date: 2020-03-24 16:32:52
:LastEditTime: 2023-04-28 13:55:49
:LastEditors: HuangJingCan
:Description: power 用户权限相关接口
"""
from seven_studio.handlers.studio_base import *
from seven_studio.utils.dict import *
from seven_studio.models.db_models.product.product_info_model import *
from seven_studio.models.db_models.product.product_user_model import *
from seven_studio.models.db_models.role.role_power_model_ex import *
from seven_studio.models.db_models.role.role_user_model import *
from seven_studio.models.db_models.role.role_info_model import *
from seven_studio.models.db_models.user.user_info_model_ex import *
from seven_studio.models.seven_model import InvokeResult
from seven_studio.models.power_model import *

class GetUserInfoHandler(StudioBaseHandler):
    """
    :description: 获取当前用户信息
    """

    @login_filter(True)
    def get_async(self):
        """
        :description: 获取当前用户信息
        :param {type} 
        :return: 
        :last_editors: HuangJingCan
        """
        user_info = self.get_curr_user_info()
        curr_info = {}
        if user_info:
            curr_info['Account'] = user_info.Account
            curr_info['IsSuper'] = user_info.IsSuper
            curr_info['UserName'] = user_info.UserName
            curr_info['NickName'] = user_info.NickName
            curr_info['JobNo'] = user_info.JobNo
            curr_info['Avatar'] = user_info.Avatar
            curr_info['Phone'] = user_info.Phone
            curr_info['Email'] = user_info.Email
            curr_info['PersonalitySignature'] = user_info.PersonalitySignature
        return self.response_json_success(curr_info)

class GetUserProductListHandler(StudioBaseHandler):
    """
    :description: 获取用户产品列表
    """

    @login_filter(True)
    def get_async(self):
        """
        :description: 获取用户产品列表
        :param {type} 
        :return: 
        :last_editors: HuangJingCan
        """
        user_id = self.request_user_id()
        product_id = self.request_product_id()
        base_manage_context_key = config.get_value('base_manage_context_key', 'db_sevenstudio')
        product_info_model = ProductInfoModel(base_manage_context_key)
        product_user_model = ProductUserModel(base_manage_context_key)
        product_data = []
        product_infos = []
        home_info = {'Title': '平台管理', 'ImageUrl': '', 'ManageUrl': '', 'WebUrl': '', 'ProductID': 0}
        is_super = self.get_is_super()
        if is_super:
            product_infos = product_info_model.get_list('IsRelease=1')
            if product_id > 0 and self.__has_home_platform_power(self.get_curr_user_info()).ResultCode == '0':
                product_data.append(home_info)
        else:
            if self.__has_home_platform_power(self.get_curr_user_info()).ResultCode == '0':
                product_data.append(home_info)
            product_user_list = product_user_model.get_list('UserID=%s', params=user_id)
            if product_user_list:
                list_str = str([i.ProductID for i in product_user_list if i.ProductID > 0 or product_id == 0]).strip('[').strip(']')
                condition = f'IsRelease=1 AND ProductID IN({list_str})'
                product_infos = product_info_model.get_list(condition)
            elif not product_data:
                return self.response_common('NoData', '没有其他平台权限')
        for product_info in product_infos:
            product_data.append(self.__to_user_product_data(user_id, product_info, is_super))
        return self.response_json_success(product_data)

    def __to_user_product_data(self, user_id, product_info, is_super):
        """
        :description: 判断该用户是否有用户管理和角色管理权限
        :param user_id: 用户id
        :param product_info: 产品信息
        :param is_super: 是否超管
        :return: 
        :last_editors: HuangJingCan
        """
        has_user_manage = False
        has_role_manage = False
        if is_super:
            has_user_manage = True
            has_role_manage = True
        else:
            role_user_list = RoleUserModel(product_info.ManageContextKey).get_list('UserID=%s', params=user_id)
            role_power_list = RolePowerModelEx(product_info.ManageContextKey).get_role_power_list([i.RoleID for i in role_user_list])
            if [i for i in role_power_list if i.MenuID == config.get_value('menu_id_user', '80ce2364-368f-47ac-98c8-819fcb521bab')]:
                has_user_manage = True
            if [i for i in role_power_list if i.MenuID == config.get_value('menu_id_role', '47a90fe3-012b-49b6-af27-5293124ce827')]:
                has_role_manage = True
        return {'Title': product_info.ProductName, 'SubTitle': product_info.ProductSubName, 'ImageUrl': product_info.ImageUrl, 'ManageUrl': product_info.ManageUrl, 'PowerUrl': product_info.PowerUrl, 'ProductID': product_info.ProductID, 'HasUserManage': has_user_manage, 'HasRoleManage': has_role_manage, 'IsBrank': product_info.IsBrank}

    def __has_home_platform_power(self, user_info):
        """
        :description: 获取该账号是否有平台管理权限
        :param user_info：用户信息
        :return: 
        :last_editors: HuangJingCan
        """
        invoke_result = InvokeResult()
        invoke_result.ResultCode = 'AccountLock'
        invoke_result.ResultMessage = '对不起该账号没有平台管理权限'
        context_key = config.get_value('base_manage_context_key', 'db_sevenstudio')
        user_info_model_ex = UserInfoModel(context_key)
        base_user_info = user_info_model_ex.get_entity_by_id(user_info.UserID)
        if not base_user_info:
            return invoke_result
        if base_user_info.IsSuper == 1:
            return InvokeResult()
        role_user_list = RoleUserModel(context_key).get_list('UserID=%s', params=self.request_user_id())
        if not role_user_list:
            return invoke_result
        role_power_list = RolePowerModelEx(context_key).get_role_power_list([i.RoleID for i in role_user_list])
        role_power_info = [i for i in role_power_list if i.MenuID == config.get_value('menu_id_platform', '03E5D2A0-DB59-47F6-8F10-1ACDEFE9BDDD')]
        return InvokeResult() if role_power_info else invoke_result

class FocusPasswordHandler(StudioBaseHandler):
    """
    :description: 强制修改密码弹窗
    """

    @login_filter(True)
    def get_async(self):
        """
        :description: 强制修改密码弹窗
        :param {type} 
        :return: 
        :last_editors: HuangJingCan
        """
        invoke_result = InvokeResult()
        is_force_password = UserInfoModelEx().is_force_password(self.get_curr_user_info())
        if not is_force_password:
            invoke_result.ResultCode = 'Has Change Password'
            invoke_result.ResultMessage = '密码已修改过'
        return self.response_custom(invoke_result)

class FocusChangeUserPwHandler(StudioBaseHandler):
    """
    :description: 强制修改密码
    """

    @login_filter(True)
    def post_async(self):
        """
        :description: 强制修改密码
        :param {type} 
        :return: 
        :last_editors: HuangJingCan
        """
        password = self.get_param('password')
        invoke_result = InvokeResult()
        user_info_model_ex = UserInfoModel(config.get_value('base_manage_context_key', 'db_sevenstudio'))
        user_info_ex = UserInfoModelEx()
        base_user_info = self.get_base_user_info()
        user_id = base_user_info.UserID if base_user_info else ''
        is_force_password = user_info_ex.is_force_password(base_user_info)
        if not is_force_password:
            return self.response_common('Error', '无需强制更改密码')
        sign_password = user_info_ex.sign_password(password, user_id)
        user_info_model_ex.update_table('Password=%s', 'UserID=%s', [sign_password, user_id])
        self.logout(user_id)
        return self.response_custom(invoke_result)

class ChangeCurrUserPwHandler(StudioBaseHandler):
    """
    :description: 修改密码
    """

    @login_filter(True)
    def post_async(self):
        """
        :description: 修改密码
        :param {type} 
        :return: 
        :last_editors: HuangJingCan
        """
        password = self.get_param('Password')
        new_password = self.get_param('NewPassword')
        invoke_result = InvokeResult()
        user_info_model_ex = UserInfoModelEx(config.get_value('base_manage_context_key', 'db_sevenstudio'))
        base_user_info = self.get_base_user_info()
        user_id = base_user_info.UserID if base_user_info else ''
        if not user_info_model_ex.verify_password(password, base_user_info.Password, user_id):
            return self.response_common('ErrorPassword', '旧密码错误，请重新输入')
        sign_password = user_info_model_ex.sign_password(new_password, user_id)
        user_info_model_ex.update_table('Password=%s', 'UserID=%s', [sign_password, user_id])
        self.logout(user_id)
        return self.response_custom(invoke_result)

class GetRoleListHandler(StudioBaseHandler):
    """
    :description: 角色列表
    """

    @login_filter(True)
    def get_async(self):
        """
        :description: 角色列表
        :param {type} 
        :return: 
        :last_editors: HuangJingCan
        """
        manage_context_key = self.get_manage_context_key()
        user_id = self.request_user_id()
        is_super = self.get_is_super()
        condition = '' if is_super else f"ChiefUserID='{user_id}'"
        role_dict_list = RoleInfoModel(manage_context_key).get_dict_list(condition, field='RoleID,RoleName')
        return self.response_json_success(role_dict_list)

class GetRoleUserListHandler(StudioBaseHandler):
    """
    :description: 角色用户列表
    """

    @login_filter(True)
    @power_filter(True)
    def post_async(self):
        """
        :description: 角色用户列表
        :param {type} 
        :return: 
        :last_editors: HuangJingCan
        """
        manage_context_key = self.get_manage_context_key()
        user_id = self.request_user_id()
        is_super = self.get_is_super()
        page_index = self.get_page_index()
        page_size = self.get_page_size()
        (condition, order) = self.get_condition_by_body()
        page_data = PageInfo()
        role_user_dto_list = []
        role_info_model = RoleInfoModel(manage_context_key)
        if not is_super:
            if condition:
                condition += ' AND '
            condition += f"ChiefUserID='{user_id}'"
        (page_list, total) = role_info_model.get_page_list('*', page_index, page_size, condition, '', order)
        if not page_list:
            return self.response_json_success(page_data)
        user_ids_list = [i.ModifyUserID for i in page_list]
        user_ids_str = str(user_ids_list).strip('[').strip(']')
        user_info_list = UserInfoModel(manage_context_key).get_list(f'UserID IN({user_ids_str})')
        role_ids_list = [i.RoleID for i in page_list]
        role_ids_str = str(role_ids_list).strip('[').strip(']')
        role_info_list = RoleUserModel(manage_context_key).get_list(f'RoleID IN({role_ids_str})')
        role_power_list = RolePowerModel(manage_context_key).get_list(f'RoleID IN({role_ids_str})')
        role_power_list = RolePowerEx().get_list_by_role_power_list(role_power_list)
        for curr_role_info in page_list:
            curr_role_user_dto = DictUtil.auto_mapper(RoleUserDto(), curr_role_info.__dict__)
            curr_user_info = [i for i in user_info_list if curr_role_info.ModifyUserID != '' and i.UserID == curr_role_info.ModifyUserID]
            curr_role_user_dto.ModifyUser = curr_user_info[0].UserName if curr_user_info else ''
            curr_role_user_dto.RoleUserIds = [i.UserID for i in role_info_list if i.RoleID == curr_role_info.RoleID]
            curr_role_user_dto.RoleMenuIds = [i.MenuCoteID for i in role_power_list if i.RoleID == curr_role_info.RoleID]
            if curr_role_info.ModifyDate == '1900-01-01 00:00:00':
                curr_role_user_dto.ModifyDate = ''
            role_user_dto_list.append(curr_role_user_dto.__dict__)
        page_data.Data = role_user_dto_list
        page_data.RecordCount = total
        page_data.PageSize = page_size
        page_data.PageIndex = page_index
        return self.response_json_success(page_data)

class GetUserRoleListHandler(StudioBaseHandler):
    """
    :description: 用户角色列表
    """

    @login_filter(True)
    def post_async(self):
        """
        :description: 用户角色列表
        :param {type} 
        :return: 
        :last_editors: HuangJingCan
        """
        manage_context_key = self.get_manage_context_key()
        user_id = self.request_user_id()
        is_super = self.get_is_super()
        page_index = self.get_page_index()
        page_size = self.get_page_size()
        (condition, order) = self.get_condition_by_body()
        product_id = config.get_value('product_id')
        page_data = PageInfo()
        user_role_dto_list = []
        user_info_model = UserInfoModel(manage_context_key)
        if not is_super:
            if condition:
                condition += ' AND '
            condition += f"ChiefUserID='{user_id}'"
        (page_list, total) = user_info_model.get_page_list('*', page_index, page_size, condition, '', order)
        if not page_list:
            return self.response_json_success(page_data)
        chief_user_ids_list = [i.ChiefUserID for i in page_list]
        chief_user_ids_str = str(chief_user_ids_list).strip('[').strip(']')
        chief_user_info_list = user_info_model.get_list(f'UserID IN({chief_user_ids_str})')
        user_ids_list = [i.UserID for i in page_list]
        user_ids_str = str(user_ids_list).strip('[').strip(']')
        role_user_list = RoleUserModel(manage_context_key).get_list(f'UserID IN({user_ids_str})')
        product_user_list = []
        if product_id == 0:
            product_user_list = ProductUserModel(config.get_value('base_manage_context_key', 'db_sevenstudio')).get_list(f'UserID IN({user_ids_str})')
        for curr_user_info in page_list:
            curr_user_role_dto = DictUtil.auto_mapper(UserRoleDto(), curr_user_info.__dict__)
            curr_user_role_dto.UserRoleIds = [i.RoleID for i in role_user_list if i.UserID == curr_user_info.UserID]
            if product_id == 0:
                curr_user_role_dto.UserProductIds = [i.ProductID for i in product_user_list if i.UserID == curr_user_info.UserID]
            chief_user_info = [i for i in chief_user_info_list if curr_user_info.ChiefUserID and i.UserID == curr_user_info.ChiefUserID]
            curr_user_role_dto.ChiefUserName = chief_user_info[0].UserName if chief_user_info else ''
            if curr_user_role_dto.LoginDate == '1900-01-01 00:00:00':
                curr_user_role_dto.LoginDate = ''
            user_role_dto_list.append(curr_user_role_dto.__dict__)
        page_data.Data = user_role_dto_list
        page_data.RecordCount = total
        page_data.PageSize = page_size
        page_data.PageIndex = page_index
        return self.response_json_success(page_data)

class SaveUserHandler(StudioBaseHandler):
    """
    :description: 保存用户
    """

    @login_filter(True)
    def post_async(self):
        """
        :description: 保存用户
        :param {type} 
        :return: 
        :last_editors: HuangJingCan
        """
        user_id = self.get_param('UserID')
        account = self.get_param('Account')
        password = self.get_param('Password')
        email = self.get_param('Email')
        user_name = self.get_param('UserName')
        nick_name = self.get_param('NickName')
        job_no = self.get_param('JobNo')
        phone = self.get_param('Phone')
        avatar = self.get_param('Avatar')
        user_role_id_str = self.get_param('UserRoleIdStr')
        user_product_id_str = self.get_param('UserProductIdStr')
        change_pw = bool(self.get_param('ChangePw', False))
        manage_context_key = self.get_manage_context_key()
        is_super = self.get_is_super()
        curr_user_id = self.request_user_id()
        product_id = self.request_product_id()
        if account == '':
            return self.response_common('AccountEmpty', '账号为空')
        user_info_model = UserInfoModel(self.get_manage_context_key())
        user_info = UserInfo()
        if user_id != '':
            user_info = user_info_model.get_entity_by_id(user_id)
            if not user_info:
                return self.response_common('NoExit', '用户不存在')
            user_info_c = user_info_model.get_entity('Account=%s AND UserID!=%s', params=[account, user_id])
        else:
            user_info_c = user_info_model.get_entity('Account=%s', params=account)
        if user_info_c:
            return self.response_common('Exit', '账号已存在')
        user_info.Account = account
        user_info.Email = email
        user_info.UserName = user_name
        user_info.NickName = nick_name
        user_info.JobNo = job_no
        user_info.Phone = phone
        user_info.Avatar = avatar
        if not self.get_is_super():
            user_info.ChiefUserID = self.request_user_id()
        power_model = PowerModel(manage_context_key, is_super, curr_user_id, product_id)
        is_add = user_id == ''
        result = power_model.set_user(user_info, user_role_id_str.split(','), user_product_id_str.split(','), password, change_pw, is_add)
        return self.response_json_success(result)

class SaveCurrUserHandler(StudioBaseHandler):
    """
    :description: 保存用户
    """

    @login_filter(True)
    def post_async(self):
        """
        :description: 保存用户
        :param {type} 
        :return: 
        :last_editors: HuangJingCan
        """
        user_id = self.request_user_id()
        email = self.get_param('Email')
        nick_name = self.get_param('NickName')
        phone = self.get_param('Phone')
        avatar = self.get_param('Avatar')
        personality_signature = self.get_param('PersonalitySignature')
        user_info_model = UserInfoModel(self.get_manage_context_key())
        user_info = user_info_model.get_entity_by_id(user_id)
        if user_id == '' or not user_info:
            return self.response_common('Exit', '账号不存在')
        user_info.Email = email
        user_info.NickName = nick_name
        user_info.Phone = phone
        user_info.Avatar = avatar
        user_info.PersonalitySignature = personality_signature
        user_info_model.update_entity(user_info, field_list=['Email', 'NickName', 'Phone', 'Avatar', 'PersonalitySignature'])
        return self.response_json_success(user_info)

class GetUserListHandler(StudioBaseHandler):
    """
    :description: 用户列表
    """

    @login_filter(True)
    def get_async(self):
        """
        :description: 用户列表
        :param {type} 
        :return: 
        :last_editors: HuangJingCan
        """
        manage_context_key = self.get_manage_context_key()
        user_id = self.request_user_id()
        is_super = self.get_is_super()
        condition = '' if is_super else f"ChiefUserID='{user_id}'"
        user_dict_list = UserInfoModel(manage_context_key).get_dict_list(condition, field='UserID,Account,UserName')
        return self.response_json_success(user_dict_list)

class SaveRoleHandler(StudioBaseHandler):
    """
    :description: 修改角色
    """

    @login_filter(True)
    @power_filter(True)
    def post_async(self):
        """
        :description: 修改角色
        :param {type} 
        :return: 
        :last_editors: HuangJingCan
        """
        role_id = self.get_param('RoleID')
        role_name = self.get_param('RoleName')
        summary = self.get_param('Summary')
        role_user_id_str = self.get_param('RoleUserIdStr')
        role_menu_id_str = self.get_param('RoleMenuIdStr')
        manage_context_key = self.get_manage_context_key()
        is_super = self.get_is_super()
        curr_user_id = self.request_user_id()
        product_id = self.request_product_id()
        if role_name == '':
            return self.response_common('RoleNameEmpty', '角色名为空')
        role_info_model = RoleInfoModel(self.get_manage_context_key())
        role_info = RoleInfo()
        if role_id != '':
            role_info = role_info_model.get_entity_by_id(role_id)
            if not role_info:
                return self.response_common('NoExit', '角色不存在')
            role_info_c = role_info_model.get_entity('RoleName=%s and RoleID!=%s', params=[role_name, role_id])
            if role_info_c:
                return self.response_common('NoExit', '角色名已存在')
        else:
            role_info_c = role_info_model.get_entity('RoleName=%s', params=role_name)
            if role_info_c:
                return self.response_common('NoExit', '角色名已存在')
            role_info.RoleID = UUIDHelper.get_uuid()
        if not self.get_is_super():
            role_info.ChiefUserID = curr_user_id
        role_info.RoleName = role_name
        role_info.Summary = summary
        role_info.ModifyDate = TimeHelper.get_now_format_time()
        role_info.ModifyUserID = self.request_user_id()
        power_model = PowerModel(manage_context_key, is_super, curr_user_id, product_id)
        is_add = role_id == ''
        result = power_model.set_role(role_info, role_user_id_str.split(','), role_menu_id_str.split(','), is_add)
        result.ModifyUser = self.get_curr_user_info().UserName
        return self.response_json_success(result.__dict__)

class RemoveRoleUserHandler(StudioBaseHandler):
    """
    :description: 删除用户角色
    """

    @login_filter(True)
    @power_filter(True)
    def get_async(self):
        """
        :description: 删除用户角色
        :param {type} 
        :return: 
        :last_editors: HuangJingCan
        """
        manage_context_key = self.get_manage_context_key()
        is_super = self.get_is_super()
        curr_user_id = self.request_user_id()
        product_id = self.request_product_id()
        role_id = self.get_param('roleID')
        user_id = self.get_param('userID')
        if role_id == '':
            return self.response_common('EmptyRoleID', '角色ID为空')
        if user_id == '':
            return self.response_common('EmptyUserID', '用户ID为空')
        power_model = PowerModel(manage_context_key, is_super, curr_user_id, product_id)
        power_model.remove_role_user(role_id, user_id)
        return self.response_json_success()

class DeleteRoleHandler(StudioBaseHandler):
    """
    :description: 删除角色
    """

    @login_filter(True)
    @power_filter(True)
    def get_async(self):
        """
        :description: 删除用户角色
        :param {type} 
        :return: 
        :last_editors: HuangJingCan
        """
        role_id = self.get_param('RoleID')
        if role_id == '':
            return self.response_common('EmptyRoleID', '角色ID为空')
        manage_context_key = self.get_manage_context_key()
        RoleUserModel(manage_context_key).del_entity('RoleID=%s', role_id)
        RolePowerModel(manage_context_key).del_entity('RoleID=%s', role_id)
        RoleInfoModel(manage_context_key).del_entity('RoleID=%s', role_id)
        return self.response_json_success()

class DeleteUserHandler(StudioBaseHandler):
    """
    :description: 删除用户
    """

    @login_filter(True)
    @power_filter(True)
    @filter_check_params('UserID')
    def get_async(self):
        """
        :description: 删除用户
        :param {type} 
        :return: 
        :last_editors: HuangJingCan
        """
        user_id = self.get_param('UserID')
        manage_context_key = self.get_manage_context_key()
        curr_user_id = self.request_user_id()
        product_id = self.request_product_id()
        is_super = self.get_is_super()
        if user_id == '':
            return self.response_common('EmptyUserID', '用户ID为空')
        if user_id == self.request_user_id():
            return self.response_common('RemoveLimit', '当前账号不能删除')
        power_model = PowerModel(manage_context_key, is_super, curr_user_id, product_id)
        power_model.remove_user(curr_user_id, user_id)
        self.logout(user_id)
        return self.response_json_success()

class ModifyUserStatusHandler(StudioBaseHandler):
    """
    :description: 更新用户状态
    """

    @login_filter(True)
    @power_filter(True)
    @filter_check_params('UserID,IsLock')
    def get_async(self):
        """
        :description: 更新用户状态
        :param {type} 
        :return: 
        :last_editors: HuangJingCan
        """
        user_id = self.get_param('UserID')
        is_lock = int(self.get_param('IsLock', -1))
        manage_context_key = self.get_manage_context_key()
        curr_user_id = self.request_user_id()
        is_super = self.get_is_super()
        if user_id == '':
            return self.response_json_error_params()
        if is_lock not in [0, 1]:
            return self.response_json_error_params()
        user_info_model = UserInfoModel(manage_context_key)
        user_info = UserInfoModel(manage_context_key).get_entity_by_id(user_id)
        if not user_info:
            return self.response_common('NoExit', '用户不存在')
        if not is_super and user_info.ChiefUserID != curr_user_id:
            return self.response_common('NoExit', '用户不存在')
        user_info_model.update_table('IsLock=%s', 'UserID=%s', [is_lock, user_id])
        return self.response_json_success()

class ResetUserPasswordHandler(StudioBaseHandler):
    """
    :description: 重置密码
    """

    @login_filter(True)
    @power_filter(True)
    @filter_check_params('UserID')
    def get_async(self):
        """
        :description: 重置密码
        :param {type} 
        :return: 
        :last_editors: HuangJingCan
        """
        user_id = self.get_param('UserID')
        base_manage_context_key = config.get_value('base_manage_context_key', 'db_sevenstudio')
        curr_user_id = self.request_user_id()
        is_super = self.get_is_super()
        user_info_model = UserInfoModel(base_manage_context_key)
        user_info = UserInfoModel(base_manage_context_key).get_entity_by_id(user_id)
        if not user_info:
            return self.response_common('NoExit', '用户不存在')
        if not is_super and user_info.ChiefUserID != curr_user_id:
            return self.response_common('NoExit', '用户不存在')
        sign_password = UserInfoModelEx().sign_password('', user_id)
        user_info_model.update_table('FaildLoginCount=0,Password=%s', 'UserID=%s', [sign_password, user_id])
        self.logout(user_id)
        return self.response_json_success()

class ResetUserFaildLoginCountHandler(StudioBaseHandler):
    """
    :description: 登录失败重置
    """

    @login_filter(True)
    @power_filter(True)
    @filter_check_params('UserID')
    def get_async(self):
        """
        :description: 登录失败重置
        :param {type}
        :return:
        :last_editors: HuangJingCan
        """
        user_id = self.get_param('UserID')
        base_manage_context_key = config.get_value('base_manage_context_key', 'db_sevenstudio')
        curr_user_id = self.request_user_id()
        is_super = self.get_is_super()
        user_info_model = UserInfoModel(base_manage_context_key)
        user_info = UserInfoModel(base_manage_context_key).get_entity_by_id(user_id)
        if not user_info:
            return self.response_common('NoExit', '用户不存在')
        if not is_super and user_info.ChiefUserID != curr_user_id:
            return self.response_common('NoExit', '用户不存在')
        user_info_model.update_table('FaildLoginCount=0', 'UserID=%s', [user_id])
        return self.response_json_success()

class RemoveUserAllRoleHandler(StudioBaseHandler):
    """
    :description: 收回权限
    """

    @login_filter(True)
    @power_filter(True)
    @filter_check_params('UserID')
    def get_async(self):
        """
        :description: 收回权限
        :param {type}
        :return:
        :last_editors: HuangJingCan
        """
        user_id = self.get_param('UserID')
        manage_context_key = self.get_manage_context_key()
        curr_user_id = self.request_user_id()
        is_super = self.get_is_super()
        role_user_model = RoleUserModel(manage_context_key)
        if is_super:
            role_user_model.del_entity('UserID=%s', user_id)
        else:
            user_info = role_user_model.get_entity_by_id(user_id)
            if user_info and user_info.ChiefUserID != curr_user_id:
                role_user_model.del_entity('UserID=%s', user_id)
        return self.response_json_success()

class CopyUserRoleHandler(StudioBaseHandler):
    """
    :description: 复制权限
    """

    @login_filter(True)
    @power_filter(True)
    @filter_check_params('userID,copyUserID')
    def get_async(self):
        """
        :description: 复制权限
        :param {type}
        :return:
        :last_editors: HuangJingCan
        """
        copy_user_id = self.get_param('copyUserID')
        user_id = self.get_param('userID')
        manage_context_key = self.get_manage_context_key()
        curr_user_id = self.request_user_id()
        product_id = self.request_product_id()
        is_super = self.get_is_super()
        power_model = PowerModel(manage_context_key, is_super, curr_user_id, product_id)
        power_model.copy_user_role(copy_user_id, user_id)
        return self.response_json_success()