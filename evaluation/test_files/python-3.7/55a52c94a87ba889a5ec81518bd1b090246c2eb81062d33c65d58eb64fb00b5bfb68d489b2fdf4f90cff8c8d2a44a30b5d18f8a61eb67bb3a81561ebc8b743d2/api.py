from selenium_recaptcha_solver.exceptions import RecaptchaException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from pydub import AudioSegment
import speech_recognition as sr
import requests
import tempfile
import os

class API:

    def __init__(self, driver: WebDriver, google_api_key: str=None):
        """
        :param driver: Selenium web driver where the Captcha will be solved on
        :param google_api_key: API key for Google's Speech API (A generic API key is already provided but it can
        be revoked by Google at any time, you can get an API key at https://cloud.google.com/speech-to-text)
        """
        self.__driver = driver
        self.__recognizer = sr.Recognizer()
        self.__google_api_key = google_api_key

    def click_recaptcha_v2(self, iframe: WebElement) -> None:
        """
        :param iframe: Iframe of Captcha to be solved
        """
        self.__driver.switch_to.frame(iframe)
        checkbox = self.__driver.find_element(by='id', value='recaptcha-anchor')
        self._js_click(checkbox)
        if checkbox.get_attribute('checked'):
            return
        self.__driver.switch_to.default_content()
        captcha_challenge = self._wait_for_element(tag='xpath', locator='//iframe[@title="recaptcha challenge expires in two minutes"]', timeout=5)
        self.solve_recaptcha_v2_challenge(iframe=captcha_challenge)

    def solve_recaptcha_v2_challenge(self, iframe: WebElement) -> None:
        """
        :param iframe: Iframe of Captcha to be solved
        """
        self.__driver.switch_to.frame(iframe)
        audio_button = self._wait_for_element(tag='id', locator='recaptcha-audio-button', timeout=10)
        self._js_click(audio_button)
        self._solve_audio_challenge()
        verify_button = self._wait_for_element(tag='id', locator='recaptcha-verify-button', timeout=5)
        self._js_click(verify_button)
        try:
            self._wait_for_element(tag='xpath', locator='//div[normalize-space()="Multiple correct solutions required - please solve more."]', timeout=1)
            self._solve_audio_challenge()
            second_verify_button = self._wait_for_element(tag='id', locator='recaptcha-verify-button', timeout=5)
            self._js_click(second_verify_button)
        except TimeoutException:
            pass
        self.__driver.switch_to.default_content()

    def _solve_audio_challenge(self) -> None:
        try:
            download_link = self._wait_for_element(tag='class name', locator='rc-audiochallenge-tdownload-link', timeout=10)
        except TimeoutException:
            raise RecaptchaException('Google has detected automated queries. Try again later.')
        tmp_dir = tempfile.gettempdir()
        (mp3_file, wav_file) = (os.path.join(tmp_dir, 'tmp.mp3'), os.path.join(tmp_dir, 'tmp.wav'))
        tmp_files = {mp3_file, wav_file}
        with open(mp3_file, 'wb') as f:
            link = download_link.get_attribute('href')
            audio_download = requests.get(url=link, allow_redirects=True)
            f.write(audio_download.content)
            f.close()
        AudioSegment.from_mp3(mp3_file).export(wav_file, format='wav')
        self.__recognizer.dynamic_energy_threshold = False
        self.__recognizer.energy_threshold = 400
        with sr.AudioFile(wav_file) as source:
            audio = self.__recognizer.listen(source)
            try:
                recognized_text = self.__recognizer.recognize_google(audio, key=self.__google_api_key)
            except sr.UnknownValueError:
                raise RecaptchaException('Speech recognition API could not understand audio, try again.')
        self._cleanup(tmp_files)
        self.__driver.find_element(by='id', value='audio-response').send_keys(recognized_text)

    def _js_click(self, element: WebElement) -> None:
        """
        :param element: Web element to perform click on via JavaScript
        """
        self.__driver.execute_script('arguments[0].click();', element)

    def _wait_for_element(self, tag: str, locator: str, timeout: int) -> any:
        """
        :param tag: Tag to get element by (id, class name, xpath, tag name, etc.)
        :param locator: Value of the tag (Example: tag -> id, locator -> button-id)
        :param timeout: Time to wait for element before raising TimeoutError
        :return: Web element specified by tag and locator
        :raises TimeoutException: If the element is not located within the desired time span
        """
        element_attributes = (tag, locator)
        WebDriverWait(self.__driver, timeout).until(ec.visibility_of_element_located(element_attributes))
        return self.__driver.find_element(by=tag, value=locator)

    @staticmethod
    def _cleanup(paths: set) -> None:
        """
        :param paths: Paths to validate existance of and delete
        """
        for path in paths:
            if os.path.exists(path):
                os.remove(path)