class BindVpcReq(object):

    def __init__(self, regionId, vpcId):
        """
        :param regionId:  vpc所在区域id
        :param vpcId:  vpc id
        """
        self.regionId = regionId
        self.vpcId = vpcId