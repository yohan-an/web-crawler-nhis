import time

import cv2
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import requests
from io import BytesIO

from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def main():
    # Service 객체로 ChromeDriver 경로를 설정
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # 필요한 작업 수행
    driver.get("https://www.nhis.or.kr/nhis/index.do")

    nextUrl = 'https://www.nhis.or.kr/nhis/etc/personalLoginPage.do'

    driver.get(nextUrl)

    time.sleep(2)

    # login
    login(driver)

    # 인증서 선택
    certificateSelect(driver)

    # 인증 확인하기 (사용자 완료시까지 대기)
    certificateComplate(driver)

    # 결과
    retrieveHealthinCheckUpTargetResult(driver)

    time.sleep(10)
    # 브라우저 닫기
    driver.quit()


def login(driver):
    try:
        from selenium.webdriver.support import expected_conditions as EC
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "button.button.large.red.simpleDemo"))
        )

        # 버튼 찾기 (클래스 이름으로)
        login_button = driver.find_element(By.CSS_SELECTOR, "button.button.large.red.simpleDemo")
        login_button.click()
        print("로그인 버튼을 클릭했습니다.")


    except TimeoutException:
        print("페이지 로딩 대기 시간이 초과되었습니다.")
    except Exception as e:
        print("버튼을 찾을 수 없거나 클릭하는 중 오류가 발생했습니다:", e)


def certificateSelect(driver):
    try:
        from selenium.webdriver.support import expected_conditions as EC

        # 최대 10초 동안 span 클래스와 특정 텍스트가 로드될 때까지 대기
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "label-nm")))

        # span 요소가 로드된 후, 해당 요소의 텍스트가 "카카오톡"인지 확인
        # "카카오톡" 텍스트가 로드된 후, 해당 요소 찾기
        kakao_span = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='label-nm']/p[text()='카카오톡']")))

        if kakao_span:

            kakao_span.click()
            print('"카카오톡" 텍스트가 로드되었습니다.')
        else:
            print('텍스트가 일치하지 않습니다.')

        input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-id="oacx_name"]')))
        input_box.send_keys("안상길")
        input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-id="oacx_birth"]')))
        input_box.send_keys("19831015")
        input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-id="oacx_phone2"]')))
        input_box.send_keys('30211502')

        checkbox = wait.until(EC.presence_of_element_located((By.ID, "totalAgree")))
        if not checkbox.is_selected():
            checkbox.click()
            print('전체동의 클릭')

        requestButton = wait.until(EC.presence_of_element_located((By.ID, "oacx-request-btn-pc")))
        requestButton.click()

    except Exception as e:
        print("오류 발생:", e)


def certificateComplate(driver):
    # 인증 확인 완료

    from selenium.webdriver.support import expected_conditions as EC

    wait = WebDriverWait(driver, 10)
    certificate = False
    while not certificate:
        time.sleep(2)

        try:
            # 인증완료 버튼 버튼
            confirm_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.basic.sky.w70")))
            print("1")
            if confirm_button:
                confirm_button.click()
            else:
                print('break ! ')
                break

        except (TimeoutException, NoSuchElementException):
            print("no search confirm button  - 1")
            break

        try:
            # Alert 버튼 찾기
            alert_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.btnArea button.pop.sky.full")))
            print("2")
            if alert_button:
                alert_button.click()
            else:
                certificate = True
                print('break !! ')
                break

        except (TimeoutException, NoSuchElementException):
            print("no search alert button  - 2")
            break


def retrieveHealthinCheckUpTargetResult(driver):
    """
        개인정보 조회
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

    # 요소 캡처
    capture_element(driver, captcha_img, image_file_name)

    # CAPTCHA 이미지의 src 속성 가져오기
    captcha_url = captcha_img.get_attribute("src")

    # OCR을 통해 이미지에서 텍스트 추출
    captcha_text = opencv_captcha("./", image_file_name)

    print("CAPTCHA 텍스트:", captcha_text)
    return captcha_text


def opencv_captcha(image_path="", image_name=""):
    image_path = image_path + "/" + image_name
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # 대비 높이기 (Histogram Equalization)
    image = cv2.equalizeHist(image)

    # 블러링을 통해 잡음 제거
    image = cv2.GaussianBlur(image, (5, 5), 0)

    # 임계처리를 통해 바이너리 이미지로 변환
    _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 전처리된 이미지 확인 (디버그용)
    cv2.imshow('Processed Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Tesseract로 텍스트 추출
    text = pytesseract.image_to_string(image, config='--psm 6')
    print("추출된 텍스트:", text)


def image_stream_download(captcha_url, filename="processed_captcha.png"):
    """
        스트림 이미지 다운로드
    """

    # 이미지 다운로드
    response = requests.get(captcha_url)
    img = Image.open(BytesIO(response.content))
    img.save(filename)

    return img


def capture_element(driver, element, save_path="element_screenshot.png"):
    """
        이미지 캡처
    """
    # 특정 요소 캡처해서 이미지 파일로 저장
    element.screenshot(save_path)
    print(f"요소 캡처 완료: {save_path}")


def preprocess_image(img):
    """
        이미지 전처리 (노이즈제거)
    :param img:
    :return:
    """
    # 이미지 그레이스케일로 변환
    img = img.convert("L")

    # 그레이스케일 후 대비 조정 (enhance 값은 1.5로 적당히 낮춤)
    img = ImageEnhance.Contrast(img).enhance(1.5)

    # 이미지의 노이즈 제거
    img = img.filter(ImageFilter.MedianFilter(3))  # 커널 사이즈 3으로 설정하여 좀 더 부드럽게 처리

    # 이미지 밝기 조정 (필요 시)
    img = ImageEnhance.Brightness(img).enhance(1.2)

    return img


if __name__ == "__main__":
    main()
