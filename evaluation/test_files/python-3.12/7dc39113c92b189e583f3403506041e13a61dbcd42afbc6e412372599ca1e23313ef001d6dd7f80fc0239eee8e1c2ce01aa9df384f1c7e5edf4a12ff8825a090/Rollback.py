class Rollback(object):

    def __init__(self, value=None, label=None):
        """
        :param value: (Optional) 回滚策略ID
        :param label: (Optional) 回滚策略名称
        """
        self.value = value
        self.label = label