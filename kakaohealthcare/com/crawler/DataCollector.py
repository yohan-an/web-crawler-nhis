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
from kakaohealthcare.com.crawler.ImageUtils import ImageUtils
from kakaohealthcare.com.crawler.Login import Login

class DataCollector:
    def __init__(self):
        pass

    def dataConvert(self):
        """
            수집된 데이터에 대한 데이터 파서
        """
        pass

    def health_result_download(self, driver):

        # 검진결과보기 이동
        driver.get("https://www.nhis.or.kr/nhis/healthin/retrieveHealthinCheckUpTargetResultAllPerson.do")

        wait = WebDriverWait(driver, 10)

        from selenium.webdriver.support import expected_conditions as EC
        xml_download_button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.button.medium.border[rel='modal:open']"))
        )
        xml_download_button.click()

        # 기본 URL 설정
        base_url = "https://www.nhis.or.kr"
        download_url = f"{base_url}/nhis/healthin/retrieveCrryy10Dnlod.do"

        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        sessionPcookies = dict_from_cookiejar(session.cookies)
        print("sessionPcookies :", sessionPcookies)

        # 파일 다운로드
        response = session.get(download_url)

        # 요청이 성공하면 파일로 저장
        if response.status_code == 200:
            with open("downloaded_file.xml", "wb") as file:
                file.write(response.content)
            print("파일이 성공적으로 다운로드되어 저장되었습니다.")
        else:
            print(f"파일 다운로드 실패. 상태 코드: {response.status_code}")


