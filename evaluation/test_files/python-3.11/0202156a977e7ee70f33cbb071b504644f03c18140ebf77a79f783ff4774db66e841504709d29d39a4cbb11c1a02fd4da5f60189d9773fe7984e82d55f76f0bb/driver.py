import os
import shutil
import subprocess
import time
import allure
import wda
from qrunner.core.ios.common import get_tcp_port, check_device
from qrunner.utils.exceptions import ScreenFailException
from qrunner.utils.log import logger
from qrunner.running.config import Qrunner

def _start_wda_xctest(udid: str, port, wda_bundle_id=None) -> bool:
    xctool_path = shutil.which('tidevice')
    logger.info(f'WDA is not running, exec: {xctool_path} -u {udid} wdaproxy --port {port} -B {wda_bundle_id}')
    args = []
    if udid:
        args.extend(['-u', udid])
    args.append('wdaproxy')
    args.extend(['--port', str(port)])
    if wda_bundle_id is not None:
        args.extend(['-B', wda_bundle_id])
    p = subprocess.Popen([xctool_path] + args)
    time.sleep(3)
    if p.poll() is not None:
        logger.warning('xctest launch failed')
        return False
    return True

class IosDriver(object):

    def __init__(self, device_id=None):
        self.device_id = check_device(device_id)
        self.pkg_name = None
        logger.info(f'启动 ios driver for {self.device_id}')
        port = get_tcp_port(self.device_id)
        self.d = wda.Client(f'http://localhost:{port}')
        if not self.d.is_ready():
            logger.info('wda未启动，开始启动wda')
            _start_wda_xctest(self.device_id, port=port)

    @property
    def device_info(self):
        """设备信息"""
        info = self.d.device_info()
        logger.info(f'设备信息: {info}')
        return info

    @property
    def page_content(self):
        """获取页面xml内容"""
        page_source = self.d.source(accessible=False)
        logger.info(f'获取页面内容: \n{page_source}')
        return page_source

    def install_app(self, ipa_url, new=True, pkg_name=None):
        """安装应用
        @param ipa_url: ipa链接
        @param new: 是否先卸载
        @param pkg_name: 应用包名
        @return:
        """
        if new is True:
            pkg_name = pkg_name if pkg_name else self.pkg_name
            self.uninstall_app(pkg_name)
        cmd = f'tidevice -u {self.device_id} install {ipa_url}'
        logger.info(f'安装应用: {ipa_url}')
        output = subprocess.getoutput(cmd)
        if 'Complete' in output.split()[-1]:
            logger.info(f'{self.device_id} 安装应用{ipa_url} 成功')
            return
        else:
            logger.info(f'{self.device_id} 安装应用{ipa_url}失败，因为{output}')

    def uninstall_app(self, pkg_name=None):
        """卸载应用"""
        pkg_name = pkg_name if pkg_name else self.pkg_name
        cmd = f'tidevice -u {self.device_id} uninstall {pkg_name}'
        logger.info(f'卸载应用: {pkg_name}')
        output = subprocess.getoutput(cmd)
        if 'Complete' in output.split()[-1]:
            logger.info(f'{self.device_id} 卸载应用{pkg_name} 成功')
            return
        else:
            logger.info(f'{self.device_id} 卸载应用{pkg_name}失败，因为{output}')

    def start_app(self, pkg_name=None, stop=True):
        """启动应用
        @param bundle_id: 应用包名
        @param stop: 是否先停止应用
        """
        if not pkg_name:
            pkg_name = self.pkg_name
        logger.info(f'启动应用: {pkg_name}')
        if stop is True:
            self.d.app_terminate(pkg_name)
        self.d.app_start(pkg_name)

    def stop_app(self, pkg_name=None):
        """停止应用"""
        if not pkg_name:
            pkg_name = self.pkg_name
        logger.info(f'停止应用: {pkg_name}')
        self.d.app_terminate(pkg_name)

    def back(self):
        """返回上一页"""
        logger.info('返回上一页')
        time.sleep(1)
        self.d.swipe(0, 100, 100, 100)

    def set_text(self, value):
        """输入内容"""
        logger.info(f'输入: {value}')
        self.d.send_keys(value)

    def screenshot(self, file_name):
        """截图"""
        if '.' in file_name:
            file_name = file_name.split('.')[0]
        img_dir = os.path.join(os.getcwd(), 'images')
        if os.path.exists(img_dir) is False:
            os.mkdir(img_dir)
        file_path = os.path.join(img_dir, f'{file_name}.png')
        logger.info(f'截图保存至: {file_path}')
        self.d.screenshot(file_path)
        return file_path

    def screenshot_with_time(self, file_name):
        """
        截图并保存到预定路径
        @param file_name: foo.png or fool
        @return:
        """
        logger.info(f'截图: {file_name}')
        try:
            if '.' in file_name:
                file_name = file_name.split('.')[0]
            img_dir = os.path.join(os.getcwd(), 'images')
            if os.path.exists(img_dir) is False:
                os.mkdir(img_dir)
            time_str = time.strftime('%Y年%m月%d日 %H时%M分%S秒')
            file_path = os.path.join(img_dir, f'{time_str}-{file_name}.png')
            self.d.screenshot(file_path)
            allure.attach.file(file_path, attachment_type=allure.attachment_type.PNG, name=f'{file_name}.png')
            return file_path
        except Exception as e:
            raise ScreenFailException(f'{file_name} 截图失败\n{str(e)}')

    def click(self, x, y):
        """点击坐标"""
        logger.info(f'点击坐标: ({x}, {y})')
        logger.info(f'{self.device_id} Tap point ({x}, {y})')
        self.d.appium_settings({'snapshotMaxDepth': 0})
        self.d.tap(x, y)
        self.d.appium_settings({'snapshotMaxDepth': 50})
        time.sleep(1)

    def click_alerts(self, alert_list: list):
        """点击弹窗"""
        try:
            self.d.alert.click(alert_list)
        except:
            pass

    def swipe(self, start_x, start_y, end_x, end_y, duration=0):
        """根据坐标滑动"""
        logger.info(f'从坐标({start_x}, {start_y})滑动到({end_x}, {end_y})')
        logger.info(f'{self.device_id} swipe from point ({start_x}, {start_y}) to ({end_x}, {end_y})')
        self.d.appium_settings({'snapshotMaxDepth': 2})
        self.d.swipe(int(start_x), int(start_y), int(end_x), int(end_y), duration)
        self.d.appium_settings({'snapshotMaxDepth': 50})
        time.sleep(2)

    def swipe_left(self, start_percent=1, end_percent=0.5):
        """往左滑动"""
        logger.info('往左边滑动')
        w, h = self.d.window_size()
        self.swipe(start_percent * (w - 1), h / 2, end_percent * w, h / 2)

    def swipe_right(self, start_percent=0.5, end_percent=1):
        """往右滑动"""
        logger.info('往右边滑动')
        w, h = self.d.window_size()
        self.swipe(start_percent * w, h / 2, end_percent * (w - 1), h / 2)

    def swipe_up(self, start_percent=0.8, end_percent=0.2):
        """往上滑动"""
        logger.info('往上边滑动')
        w, h = self.d.window_size()
        self.swipe(w / 2, start_percent * h, w / 2, end_percent * h)

    def swipe_down(self, start_percent=0.2, end_percent=0.8):
        """往下滑动"""
        logger.info('往下面滑动')
        w, h = self.d.window_size()
        self.swipe(w / 2, start_percent * h, w / 2, end_percent * h)

    def health_check(self):
        """检查设备连接状态"""
        logger.info('健康检查')
        self.d.healthcheck()

    def open_url(self, url):
        """
        打开schema
        @param: url，schema链接，taobao://m.taobao.com/index.htm
        @return:
        """
        logger.info(f'打开url: {url}')
        self.d.open_url(url)
if __name__ == '__main__':
    driver = IosDriver()
    driver.bundle_id = 'com.qizhidao.company'
    print(driver.page_content)