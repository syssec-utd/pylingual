from yescaptcha.task.base import BaseTaskProxyless

class RecaptchaV3EnterpriseTask(BaseTaskProxyless):
    type = 'RecaptchaV3EnterpriseTask'

    def __init__(self, website_url, website_key, page_action, *args, **kwargs):
        self.page_action = page_action
        super(RecaptchaV3EnterpriseTask, self).__init__(website_url, website_key, *args, **kwargs)

    def serialize(self):
        return {**super().serialize(), 'pageAction': self.page_action}