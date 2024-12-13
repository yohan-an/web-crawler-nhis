import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from kakaohealthcare.com.crawler.Captcha import Captcha
from kakaohealthcare.com.crawler.DataCollector import DataCollector
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
    #collector.health_result_download(driver)
    collector.health_result_download_pdf(driver)


    # 브라우저 닫기
    # driver.quit()


def driver_init():
    # Service 객체로 ChromeDriver 경로를 설정

    # PDF 저장을 위한 추가 설정
    # app_state = {
    #     "recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
    #     "selectedDestinationId": "Save as PDF",
    #     "version": 2,
    # }

    app_state = {
        "recentDestinations": [{"id": "PDF로 저장", "origin": "local", "account": ""}],  # 한글 환경에서 PDF 저장 옵션
        "selectedDestinationId": "PDF로 저장",  # 한글 환경에서 PDF 저장 옵션
        "version": 2,
    }

    # 다운로드 디렉토리 설정
    save_dir = "/Users/yohan.an/Downloads/pdf"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print("디렉토리 생성됨:", save_dir)


    profile = {
        "printing.print_preview_sticky_settings.appState": str(app_state),
        "savefile.default_directory": save_dir,  # PDF 저장 경로 지정
        "download.prompt_for_download": False,  # 다운로드 시 창 띄우지 않음
        "profile.default_content_setting_values.automatic_downloads": 1,  # 자동 다운로드 허용
        "download.default_directory": save_dir,  # 기본 다운로드 경로
        "download.directory_upgrade": True,  # 디렉토리 업그레이드 허용
        "safebrowsing.enabled": True,  # 안전한 다운로드 기능 활성화
    }
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", profile)
    chrome_options.add_argument("--kiosk-printing")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-software-rasterizer")

    # 로그 설정
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--v=2")  # 로그 레벨을 높임
    chrome_options.add_argument("--log-path="+save_dir+"/chrome-file.log")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver


def retrieve_healthin_checkUp_target_result(driver):
    """
        개인정보 조회 ->
    """
    captcha = Captcha()
    captcha.captcha_processing_loop(driver)



if __name__ == "__main__":
    main()
