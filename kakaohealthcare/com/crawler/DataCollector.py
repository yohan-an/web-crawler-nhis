import time

import requests
from requests.utils import dict_from_cookiejar
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


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



    def health_result_download_pdf(self, driver):



        wait = WebDriverWait(driver, 10)
        from selenium.webdriver.support import expected_conditions as EC

        result_buttons = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.button.small.border"))
        )

        # 각각의 '결과' 버튼 클릭하기
        for index, button in enumerate(result_buttons):
            if "결과" in button.text:
                print(f"Clicking on result button {index + 1}")
                ActionChains(driver).move_to_element(button).perform()
                button.click()
                time.sleep(2)  # 페이지 로딩 또는 처리 대기

                # button = driver.find_element(By.XPATH, "//li[@id='crownix-toolbar-print_pdf']//button")
                #actions = ActionChains(driver)
                #actions.move_to_element(button).click().perform()

                # 버튼이 클릭 가능할 때까지 대기
                button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "crownix-toolbar-myItem1")))
                ActionChains(driver).move_to_element(button).click().perform()

                try:
                    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())  # alert가 뜰 때까지 기다림
                    alert.accept()  # 확인 버튼 클릭 (alert 창을 닫음)
                except:
                    print("Alert 창이 나타나지 않거나 다른 예외가 발생했습니다.")

                close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.button-group .closeLayer a.button.large.border")))
                close_button.click()

