from unittest import TestCase

import main
from kakaohealthcare.com.conf.Const import Const
from kakaohealthcare.com.crawler.Captcha import Captcha


class TestCaptcha(TestCase):
    def test_captcha_processing(self):
        driver = main.driver_init()

        print(f'data = ', Const.WORKSPACE)
        captcha = Captcha()
        captcha.captcha_processing(driver)
        # self.assertTrue()


class TestCaptcha(TestCase):
    def test_opencv_captcha(self):
        captcha = Captcha()
        captcha.opencv_captcha(Const.WORKSPACE, "/captcha_screenshot.png")
        # self.fail()
