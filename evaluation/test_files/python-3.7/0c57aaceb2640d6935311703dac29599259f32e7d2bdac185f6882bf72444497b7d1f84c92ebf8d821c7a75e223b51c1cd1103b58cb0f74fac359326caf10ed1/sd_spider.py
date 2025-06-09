"""淘宝拼多多刷单爬虫模块"""
from time import sleep
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from pacc.mysql.retrieve import RetrieveSD
DOMAIN = 'http://sd.coco56.top/'
START_INDEX = 7
DEPARTING_STAFF = ['郭志勇']

class Spider:
    """爬虫类"""
    driver = webdriver.Chrome()

    @classmethod
    def open_url_in_new_window(cls, url=''):
        """在新窗口中打开URL

        :param url: 待打开的URL
        """
        cls.driver.execute_script(f"window.open('{url}')")

    @classmethod
    def main(cls):
        """淘宝拼多多刷单爬虫程序入口方法"""
        RetrieveSD.all_names = RetrieveSD.all_names[START_INDEX:]
        for (index, username) in enumerate(RetrieveSD.all_accounts[START_INDEX:]):
            cls.driver.get(DOMAIN)
            cls.driver.maximize_window()
            sleep(4)
            print(index + START_INDEX + 1, username, end=' ')
            password = 'k187397'
            cls.driver.find_element(By.ID, 'username').send_keys(username)
            cls.driver.find_element(By.ID, 'password').send_keys(password)
            cls.driver.find_element(By.XPATH, '//*[@class="ant-btn ant-btn-primary ant-btn-lg submit___Q43EO"]/span').click()
            sleep(3)
            cls.open_url_in_new_window(f'{DOMAIN}record/trades')
            cls.open_url_in_new_window(f'{DOMAIN}record/linked')
            cls.open_url_in_new_window(f'{DOMAIN}account/buyers')
            cls.open_url_in_new_window(f'{DOMAIN}account/wallet')
            cls.driver.switch_to.window(cls.driver.window_handles[1])
            sleep(5)
            while True:
                sleep(1)
                recorded_amount = cls.driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/section/div[2]/main/div/div[1]/div/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[1]/div/span[2]')
                recorded_amount = float(recorded_amount.text)
                to_be_recorded_amount = cls.driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/section/div[2]/main/div/div[1]/div/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[2]/div/span[2]')
                to_be_recorded_amount = float(to_be_recorded_amount.text)
                withdrawn_amount = cls.driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/section/div[2]/main/div/div[1]/div/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]/div/span[2]')
                withdrawn_amount = float(withdrawn_amount.text)
                if recorded_amount or to_be_recorded_amount or withdrawn_amount:
                    break
            cls.driver.find_element(By.XPATH, '//*[@class="ant-btn ant-btn-primary"]/span').click()
            cls.driver.find_element(By.ID, 'amount').send_keys('9999')
            cls.driver.find_element(By.ID, 'tradeWayNo').send_keys('18739776523@qq.com')
            value = cls.driver.find_element(By.ID, 'amount').get_attribute('value')
            print(RetrieveSD.all_names[index], value)
            cls.driver.find_element(By.ID, 'realName').send_keys('徐可可')
            cls.driver.find_element(By.ID, 'password').send_keys(password)
            pyperclip.copy(f'{RetrieveSD.all_names[index]}\t{value}')
            if float(value) >= 20 and RetrieveSD.all_names[index] not in DEPARTING_STAFF:
                cls.driver.find_element(By.XPATH, '//*[@class="ant-modal-footer"]//*[@class="ant-btn ant-btn-primary"]').click()
                sleep(3)
                cls.driver.refresh()
            else:
                print(f'已入账金额：{recorded_amount}，待入账金额：{to_be_recorded_amount}')
            input()
            cls.driver.quit()
            if not index == len(RetrieveSD.all_accounts) - 1:
                cls.driver = webdriver.Chrome()
if __name__ == '__main__':
    Spider.main()