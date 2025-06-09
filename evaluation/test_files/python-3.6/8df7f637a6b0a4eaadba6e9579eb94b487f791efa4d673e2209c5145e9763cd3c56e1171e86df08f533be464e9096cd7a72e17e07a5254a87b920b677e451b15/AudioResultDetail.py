class AudioResultDetail(object):

    def __init__(self, scene=None, label=None, score=None, suggestion=None, details=None):
        """
        :param scene: (Optional) 检测场景，和调用请求中的场景对应
        :param label: (Optional) 检测结果的分类，与具体的scene对应。取值范围参考scene和label说明
        :param score: (Optional) 结果为该分类的概率，取值范围为0.00-100.00。值越高，表示越有可能属于改该子分类
        :param suggestion: (Optional) 建议用户执行的操作，取值范围pass：图片正常，无需进行其余操作，或者未识别出目标对象review：检测结果不确定，需要进行人工审核，或识别出目标对象block：图片违规，建议执行进一步操作（如直接删除或做限制处理）
        :param details: (Optional) 语音对应的文本详情（每一句文本对应一个元素），包含一个或者多个元素，具体结构描述见detail。
        """
        self.scene = scene
        self.label = label
        self.score = score
        self.suggestion = suggestion
        self.details = details