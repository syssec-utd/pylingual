class AttackLog(object):

    def __init__(self, ip=None, resourceType=None, attackLogId=None, startTime=None, endTime=None, cause=None, status=None, blackHole=None, peak=None, unit=None, attackType=None):
        """
        :param ip: (Optional) 公网 IP 地址
        :param resourceType: (Optional) 公网 IP 类型或绑定资源类型.
<br>- 0: 未知类型
<br>- 1: 弹性公网 IP(IP 为弹性公网 IP, 绑定资源类型未知)
<br>- 10: 弹性公网 IP(IP 为弹性公网 IP, 但未绑定资源)
<br>- 11: 云主机
<br>- 12: 负载均衡
<br>- 13: 原生容器实例
<br>- 14: 原生容器 Pod
<br>- 2: 云物理服务器
<br>- 3: Web应用防火墙 IP
<br>- 4: 托管区公网 IP

        :param attackLogId: (Optional) 攻击记录 ID
        :param startTime: (Optional) 攻击开始时间, UTC 时间, 格式: yyyy-MM-dd'T'HH:mm:ssZ
        :param endTime: (Optional) 攻击结束时间, UTC 时间, 格式: yyyy-MM-dd'T'HH:mm:ssZ
        :param cause: (Optional) 触发原因.<br>- 0: 未知,<br>- 1: 四层,<br>- 2: 七层,<br>- 3: 四层和七层
        :param status: (Optional) 状态. <br>- 0: 清洗完成<br>- 1: 清洗中<br>- 2: 黑洞中
        :param blackHole: (Optional) 是否黑洞
        :param peak: (Optional) 攻击流量峰值
        :param unit: (Optional) 攻击流量峰值单位
        :param attackType: (Optional) 攻击类型
        """
        self.ip = ip
        self.resourceType = resourceType
        self.attackLogId = attackLogId
        self.startTime = startTime
        self.endTime = endTime
        self.cause = cause
        self.status = status
        self.blackHole = blackHole
        self.peak = peak
        self.unit = unit
        self.attackType = attackType