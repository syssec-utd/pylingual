class RecordRule(object):

    def __init__(self, userRoomId=None, mcuUsers=None, filePrefix=None):
        """
        :param userRoomId: (Optional) 业务接入方定义的且在JRTC系统内注册过的房间号
        :param mcuUsers: (Optional) 业务接入方用户体系定义的且在JRTC系统内注册过的userId,当前不支持混流，且只支持一个userId,不指定时，默认录制本房间内所有userId的单路音视频流
        :param filePrefix: (Optional) 录制文件前缀
        """
        self.userRoomId = userRoomId
        self.mcuUsers = mcuUsers
        self.filePrefix = filePrefix