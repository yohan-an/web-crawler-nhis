from io import BytesIO

import cv2
import pytesseract
import requests
from PIL import Image
from matplotlib import pyplot as plt
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from kakaohealthcare.com.conf.Const import Const
from kakaohealthcare.com.crawler.ImageUtils import ImageUtils


class Captcha(object):
    def __init__(self):
        pass

    def opencv_captcha(self, image_path="${home}", image_name="default_imagename.png"):
        image_path = image_path + "/" + image_name
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # 히스토그램 그리기 (전처리 전)
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        plt.hist(image.ravel(), 256, [0, 256])
        plt.title("Histogram - Before Equalization")
        plt.savefig(Const.WORKSPACE +"/histogram-before.jpg")
        # plt.close()
        # 대비 높이기 (Histogram Equalization)
        image = cv2.equalizeHist(image)

        # 히스토그램 그리기 (전처리 후)
        plt.subplot(1, 2, 2)
        plt.hist(image.ravel(), 256, [0, 256])
        plt.title("Histogram - After Equalization")
        plt.savefig(Const.WORKSPACE +"/histogram-after.jpg")


        plt.show()
        plt.close()


        # 블러링을 통해 잡음 제거
        image = cv2.GaussianBlur(image, (5, 5), 0)

        # 임계처리를 통해 바이너리 이미지로 변환
        _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 전처리된 이미지 확인 (디버그용)
        # cv2.imshow('Processed Image', image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        cv2.imwrite(Const.WORKSPACE+"/threshold_image.jpg", image)



        # Tesseract로 텍스트 추출
        text = pytesseract.image_to_string(image, config='--psm 6')
        print(f"text : {text}")
        return text


    def captcha_processing(self, driver):
        """
            이미지 캡처
        """

        image_file_name = "captcha_screenshot.png"

        driver.get('https://www.nhis.or.kr/nhis/healthin/retrieveHealthinCheckUpTargetResultPerson.do')
        wait = WebDriverWait(driver, 10)
        from selenium.webdriver.support import expected_conditions as EC
        captcha_area = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "captcha-area"))
        )

        # CAPTCHA 이미지가 로드될 때까지 대기
        captcha_img = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "captchaImg"))
        )

        image_utils = ImageUtils()
        first_correction = image_utils.preprocess_image(captcha_img)
        first_correction.save("first_correction.png")

        # 요소 캡처
        self.capture_element(driver, captcha_img, image_file_name)

        # CAPTCHA 이미지의 src 속성 가져오기
        captcha_url = captcha_img.get_attribute("src")

        # OCR을 통해 이미지에서 텍스트 추출



        captcha = Captcha()
        captcha_text = captcha.opencv_captcha("./", image_file_name)
        print("CAPTCHA 텍스트:", captcha_text)

        return captcha_text

    def capture_element(self, driver, element, save_path="element_screenshot.png"):
        """
            이미지 캡처
        """
        # 특정 요소 캡처해서 이미지 파일로 저장
        element.screenshot(save_path)
        #print(f"요소 캡처 완료: {save_path}")


    def captcha_processing_loop(self, driver):
        max_retry = 200
        from selenium.webdriver.support import expected_conditions as EC

        index = 0
        while max_retry > 0:

            print(".", end="", flush=True)
            captcha = Captcha()

            captcha_text = captcha.captcha_processing(driver)
            captcha_confirm_button = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.button.large.red"))
            )

            captcha_input = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.ID, "captcha"))
            )

            captcha_input.send_keys(captcha_text)

            try:
                if captcha_confirm_button:
                    captcha_confirm_button.click()
                else:
                    break
            except Exception:
                print("no search confirm button - captcha")

            # URL이 변경되었는지 확인하여 성공 시 종료
            try:
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "검진결과 한눈에 보기"))
                )
                print("\nCAPTCHA 성공! 페이지가 이동되었습니다.")
                break
            except:
                print("\n요소를 찾지 못했습니다. 다시 시도합니다.")

            # 재시도 횟수 감소
            max_retry -= 1
            index += 1

    def image_stream_download(self, captcha_url, filename="processed_captcha.png"):
        """
            스트림 이미지 다운로드
        """

        # 이미지 다운로드
        response = requests.get(captcha_url)
        img = Image.open(BytesIO(response.content))
        img.save(filename)

        return img

