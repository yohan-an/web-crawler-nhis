import time

import cv2
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import requests
from io import BytesIO

from matplotlib import pyplot as plt
from requests.utils import dict_from_cookiejar
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from kakaohealthcare.com.crawler.Captcha import Captcha
from kakaohealthcare.com.crawler.DataCollector import DataCollector
from kakaohealthcare.com.crawler.ImageUtils import ImageUtils
from kakaohealthcare.com.crawler.Login import Login


def main():
    # Service 객체로 ChromeDriver 경로를 설정
    driver = driver_init()

    # 필요한 작업 수행
    driver.get("https://www.nhis.or.kr/nhis/index.do")
    next_url = 'https://www.nhis.or.kr/nhis/etc/personalLoginPage.do'
    driver.get(next_url)

    time.sleep(0.5)

    login = Login()
    # login
    login.login(driver)

    # 인증서 선택
    login.certificateSelect(driver)

    # 인증 확인하기 (사용자 완료시까지 대기)
    login.certificateComplate(driver)

    # 결과
    retrieve_healthin_checkUp_target_result(driver)

    # 결과 다운로드
    collector = DataCollector()
    collector.health_result_download(driver)

    # 브라우저 닫기
    # driver.quit()


def driver_init():
    # Service 객체로 ChromeDriver 경로를 설정
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    return driver


def retrieve_healthin_checkUp_target_result(driver):
    """
        개인정보 조회 ->
    """
    captcha = Captcha()
    captcha.captcha_processing_loop(driver)



if __name__ == "__main__":
    main()
