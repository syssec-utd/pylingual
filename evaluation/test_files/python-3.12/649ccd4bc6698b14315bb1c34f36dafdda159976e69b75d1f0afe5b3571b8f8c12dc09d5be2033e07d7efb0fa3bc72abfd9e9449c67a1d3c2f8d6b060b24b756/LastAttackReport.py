class LastAttackReport(object):

    def __init__(self, lastAttackTime=None, attackCount=None):
        """
        :param lastAttackTime: (Optional) 最后攻击时间，时间戳
        :param attackCount: (Optional) 攻击个数
        """
        self.lastAttackTime = lastAttackTime
        self.attackCount = attackCount