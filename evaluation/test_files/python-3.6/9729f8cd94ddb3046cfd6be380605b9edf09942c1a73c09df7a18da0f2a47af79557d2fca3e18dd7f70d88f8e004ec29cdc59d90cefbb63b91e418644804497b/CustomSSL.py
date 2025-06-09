class CustomSSL(object):

    def __init__(self, priority=None, keyless_server=None, expires_on=None, hosts=None, zone_id=None, status=None, geo_restrictions=None, modified_on=None, signature=None, issuer=None, id=None, uploaded_on=None, bundle_method=None):
        """
        :param priority: (Optional) 在请求中使用证书的顺序/优先级。

        :param keyless_server: (Optional) 
        :param expires_on: (Optional) 来自授权机构的证书过期时间
        :param hosts: (Optional) 
        :param zone_id: (Optional) 域标识符标签
        :param status: (Optional) 域的自定义SSL的状态
        :param geo_restrictions: (Optional) 
        :param modified_on: (Optional) 上次修改证书的时间
        :param signature: (Optional) 用于证书的哈希类型
        :param issuer: (Optional) 颁发证书的证书颁发机构
        :param id: (Optional) 自定义证书标识符标签
        :param uploaded_on: (Optional) 证书上载到星盾的时间
        :param bundle_method: (Optional) SSL泛捆绑在各处有着最高的概率被验证，甚至能被使用过时的或不寻常的信任存储的客户端验证。
最佳捆绑使用最短的认证链和最新的中间证书。
而强制捆绑会验证证书链，但不以其他方式修改证书链。

        """
        self.priority = priority
        self.keyless_server = keyless_server
        self.expires_on = expires_on
        self.hosts = hosts
        self.zone_id = zone_id
        self.status = status
        self.geo_restrictions = geo_restrictions
        self.modified_on = modified_on
        self.signature = signature
        self.issuer = issuer
        self.id = id
        self.uploaded_on = uploaded_on
        self.bundle_method = bundle_method