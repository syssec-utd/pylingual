class SkipActionCfg(object):

    def __init__(self, passAll, cc, waf, deny, rateLimit, bot, risk):
        """
        :param passAll:  是否跳过所有阶段，1表示是，0表示否
        :param cc:  是否执行cc防护，1表示是，0表示否
        :param waf:  是否执行waf防护，1表示是，0表示否
        :param deny:  是否执行deny防护，1表示是，0表示否
        :param rateLimit:  是否执行限速，1表示是，0表示否
        :param bot:  是否执行bot，1表示是，0表示否
        :param risk:  是否执行风控，1表示是，0表示否
        """
        self.passAll = passAll
        self.cc = cc
        self.waf = waf
        self.deny = deny
        self.rateLimit = rateLimit
        self.bot = bot
        self.risk = risk