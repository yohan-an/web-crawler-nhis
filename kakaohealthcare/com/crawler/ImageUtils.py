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


class ImageUtils(object):
    def __init__(self):
        pass;


    def preprocess_image(self,  captcha_element):
        """
            테서렉트에 대한 기본 - 이미지 전처리 (노이즈제거)
        :param img:
        :return:
        """

        # CAPTCHA 이미지의 src 속성 가져오기
        captcha_url = captcha_element.get_attribute("src")

        # 이미지 다운로드
        response = requests.get(captcha_url)
        img = Image.open(BytesIO(response.content))

        # 전처리 이전 이미지
        img.save("prior_preprocessing.png")

        # 이미지 그레이스케일로 변환
        img = img.convert("L")

        # 그레이스케일 후 대비 조정 (enhance 값은 1.5로 적당히 낮춤)
        img = ImageEnhance.Contrast(img).enhance(1.5)

        # 이미지의 노이즈 제거
        img = img.filter(ImageFilter.MedianFilter(3))  # 커널 사이즈 3으로 설정하여 좀 더 부드럽게 처리

        # 이미지 밝기 조정 (필요 시)
        img = ImageEnhance.Brightness(img).enhance(1.2)

        return img