class LiveStreamRecordConfig(object):

    def __init__(self, publishDomain=None, appName=None, streamName=None, watermarkConfig=None):
        """
        :param publishDomain: (Optional) 推流域名
        :param appName: (Optional) 应用名称
        :param streamName: (Optional) 流名称
        :param watermarkConfig: (Optional) 水印模板集合
        """
        self.publishDomain = publishDomain
        self.appName = appName
        self.streamName = streamName
        self.watermarkConfig = watermarkConfig