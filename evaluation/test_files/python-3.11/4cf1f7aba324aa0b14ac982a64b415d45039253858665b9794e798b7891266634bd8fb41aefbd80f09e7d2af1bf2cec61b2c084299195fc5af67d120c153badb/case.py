import time
from qrunner.utils.log import logger
from qrunner.utils.config import conf
from qrunner.core.web.driver import WebDriver
from qrunner.core.web.element import WebElement

class WebTestCase(object):
    """
    测试用例基类，所有测试用例需要继承该类
    """

    def start_class(self):
        """
        Hook method for setup_class fixture
        :return:
        """
        pass

    def end_class(self):
        """
        Hook method for teardown_class fixture
        :return:
        """
        pass

    @classmethod
    def setup_class(cls):
        browser_name = conf.get_item('web', 'browser_name')
        cls.driver = WebDriver.get_instance(browser_name)
        cls().start_class()

    @classmethod
    def teardown_class(cls):
        cls().driver.quit()
        cls().end_class()

    def start(self):
        """
        Hook method for setup_method fixture
        :return:
        """
        pass

    def end(self):
        """
        Hook method for teardown_method fixture
        :return:
        """
        pass

    def setup_method(self):
        self.start_time = time.time()
        logger.debug(f"[start_time]: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.start()

    def teardown_method(self):
        self.end()
        self.screenshot('用例执行完成截图')
        logger.debug(f"[end_time]: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        take_time = time.time() - self.start_time
        logger.debug('[run_time]: {:.2f} s'.format(take_time))

    @staticmethod
    def sleep(n: int):
        logger.debug(f'等待: {n}s')
        time.sleep(n)

    def element(self, **kwargs):
        """
        定位元素
        :param kwargs: 元素定位方式
        :return: 根据平台返回对应的元素
        """
        return WebElement(**kwargs)

    def screenshot(self, file_name):
        file_path = self.driver.screenshot(file_name)
        logger.debug(f'[截图并上传报告] {file_path}')

    def click(self, **kwargs):
        """点击"""
        self.element(**kwargs).click()

    def click_exists(self, **kwargs):
        """存在才点击"""
        self.element(**kwargs).click_exists()

    def input(self, text, **kwargs):
        """输入"""
        self.element(**kwargs).set_text(text)

    def input_clear(self, **kwargs):
        """清除输入框"""
        self.element(**kwargs).clear_text()

    def get_text(self, **kwargs):
        """获取文本属性"""
        return self.element(**kwargs).text

    def assertText(self, expect_value, timeout=5):
        """断言页面包含文本"""
        for _ in range(timeout + 1):
            try:
                page_source = self.driver.page_content
                assert expect_value in page_source, f'页面内容不包含 {expect_value}'
                break
            except AssertionError:
                time.sleep(1)
        else:
            page_source = self.driver.page_content
            assert expect_value in page_source, f'页面内容不包含 {expect_value}'

    def assertNotText(self, expect_value, timeout=5):
        """断言页面不包含文本"""
        for _ in range(timeout + 1):
            try:
                page_source = self.driver.page_content
                assert expect_value not in page_source, f'页面内容不包含 {expect_value}'
                break
            except AssertionError:
                time.sleep(1)
        else:
            page_source = self.driver.page_content
            assert expect_value not in page_source, f'页面内容仍然包含 {expect_value}'

    def assertElement(self, timeout=5, **kwargs):
        """断言元素存在"""
        for _ in range(timeout + 1):
            try:
                element = self.element(**kwargs)
                assert element.exists(), f'元素 {kwargs} 不存在'
                break
            except AssertionError:
                time.sleep(1)
        else:
            assert self.element(**kwargs).exists(), f'元素 {kwargs} 不存在'

    def assertNotElement(self, timeout=5, **kwargs):
        """断言元素不存在"""
        for _ in range(timeout + 1):
            try:
                assert not self.element(**kwargs).exists(), f'元素 {kwargs} 仍然存在'
                break
            except AssertionError:
                time.sleep(1)
        else:
            assert not self.element(**kwargs).exists(), f'元素 {kwargs} 仍然存在'

    def open_url(self, url=None, login=True):
        """打开页面"""
        self.driver.open_url(url=url, login=login)

    def click_by_js(self, **kwargs):
        """通过js的方式点击"""
        self.driver.click(self.element(**kwargs))

    def accept_alert(self):
        """同意弹窗"""
        self.driver.accept_alert()

    def dismiss_alert(self):
        """拒绝弹窗"""
        self.driver.dismiss_alert()

    def assertTitle(self, expect_value=None, timeout=5):
        """断言页面标题等于"""
        for _ in range(timeout + 1):
            try:
                title = self.driver.get_title()
                assert expect_value == title, f'页面标题 {title} 不等于 {expect_value}'
                break
            except AssertionError:
                time.sleep(1)
        else:
            title = self.driver.get_title()
            assert expect_value == title, f'页面标题 {title} 不等于 {expect_value}'

    def assertInTitle(self, expect_value=None, timeout=5):
        """断言页面标题包含"""
        for _ in range(timeout + 1):
            try:
                title = self.driver.get_title()
                assert expect_value in title, f'页面标题 {title} 不包含 {expect_value}'
                break
            except AssertionError:
                time.sleep(1)
        else:
            title = self.driver.get_title()
            assert expect_value in title, f'页面标题 {title} 不包含 {expect_value}'

    def assertUrl(self, expect_value=None, timeout=5):
        """断言页面url等于"""
        for _ in range(timeout + 1):
            try:
                url = self.driver.get_url()
                assert expect_value == url, f'页面url {url} 不等于 {expect_value}'
                break
            except AssertionError:
                time.sleep(1)
        else:
            url = self.driver.get_url()
            assert expect_value == url, f'页面url {url} 不等于 {expect_value}'

    def assertInUrl(self, expect_value=None, timeout=5):
        """断言页面url包含"""
        for _ in range(timeout + 1):
            try:
                url = self.driver.get_url()
                assert expect_value in url, f'页面url {url} 不包含 {expect_value}'
                break
            except AssertionError:
                time.sleep(1)
        else:
            url = self.driver.get_url()
            assert expect_value in url, f'页面url {url} 不包含 {expect_value}'

    def assertAlertText(self, expect_value):
        """断言弹窗文本"""
        alert_text = self.driver.get_alert_text()
        assert expect_value == alert_text, f'弹窗文本 {alert_text} 等于 {expect_value}'