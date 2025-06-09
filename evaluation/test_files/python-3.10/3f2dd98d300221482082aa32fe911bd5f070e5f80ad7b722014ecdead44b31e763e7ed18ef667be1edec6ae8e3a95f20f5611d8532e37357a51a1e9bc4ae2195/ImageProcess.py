import base64
import requests
from pobaidu.lib import get_toml
from aip import AipImageProcess

class ImageProcess:

    def __init__(self):
        self.baidu_ai_cfg = get_toml()
        if self.baidu_ai_cfg['baidu-ai']['client_api'] and self.baidu_ai_cfg['baidu-ai']['client_secret'] and self.baidu_ai_cfg['baidu-ai']['client_id']:
            self.CLIENT_API = self.baidu_ai_cfg['baidu-ai']['client_api']
            self.CLIENT_SECRET = self.baidu_ai_cfg['baidu-ai']['client_secret']
            self.CLIENT_ID = self.baidu_ai_cfg['baidu-ai']['client_id']

    def selfie_anime(self, img_path):
        print('=' * 30)
        print('正在进行动漫头像的转换')
        print('本仓库的视频教程：http://t.cn/A6aAvu47')
        print('这个接口调用的是百度AI平台的免费试用接口（200次），如果代码报错，大概率是试用次数没有了')
        print('获取免费使用次数的教程，我整理在这个文档里了：https://python-office.com/office/image.html')
        print('=' * 30)
        url = 'https://aip.baidubce.com/rest/2.0/image-process/v1/selfie_anime'
        origin_im = open(img_path, 'rb')
        path = base64.b64encode(origin_im.read())
        origin_im.close()
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        params = {'access_token': self.get_access_token(self.CLIENT_API, self.CLIENT_SECRET), 'image': path}
        response = requests.post(url, data=params, headers=headers)
        if response:
            f = open('result.jpg', 'wb')
            try:
                anime = response.json()['image']
            except:
                raise Exception('你没有开通百度AI账号，错误原因以及【免费】开通方式，见：https://mp.weixin.qq.com/s/5Eyk2j20jzSaVcr1DTsfvw')
            anime = base64.b64decode(anime)
            f.write(anime)
            f.close()
        print('*' * 20 + '{}'.format('动漫头像名称：result.jpg') + '*' * 20)
        print('*' * 20 + '{}'.format('您的动漫头像转换完毕，请在本代码运行的文档里查看') + '*' * 20)

    def colourize(self, img_path, output_path):
        """
        给黑白图片上色 https://ai.baidu.com/ai-doc/IMAGEPROCESS/Bk3bclns3
        :param img_path: 黑白图片的位置
        :param output_path: 上色后图片的保存位置
        :return:
                {
                    "log_id": "6876747463538438254",
                    "image": "处理后图片的Base64编码"
                }
        """
        client = AipImageProcess(self.CLIENT_ID, self.CLIENT_API, self.CLIENT_SECRET)
        with open(img_path, 'rb') as fp:
            res_image = client.colourize(fp.read())
            imgdata = base64.b64decode(res_image['image'])
            with open(output_path, 'wb') as f:
                f.write(imgdata)
            return res_image