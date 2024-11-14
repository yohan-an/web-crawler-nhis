import time

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class Login :
    def __init__(self):
        pass

    def login(self, driver):
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

    def certificateSelect(self, driver):
        try:
            from selenium.webdriver.support import expected_conditions as EC

            # 최대 10초 동안 span 클래스와 특정 텍스트가 로드될 때까지 대기
            wait = WebDriverWait(driver, 5)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "label-nm")))

            # span 요소가 로드된 후, 해당 요소의 텍스트가 "카카오톡"인지 확인
            # "카카오톡" 텍스트가 로드된 후, 해당 요소 찾기
            kakao_span = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[@class='label-nm']/p[text()='카카오톡']")))

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

    def certificateComplate(self, driver):
        # 인증 확인 완료

        from selenium.webdriver.support import expected_conditions as EC

        wait = WebDriverWait(driver, 3)
        certificate = False
        while not certificate:
            time.sleep(2)

            try:
                # 인증완료 버튼 버튼
                confirm_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.basic.sky.w70")))
                if confirm_button:
                    confirm_button.click()
                else:
                    break

            except (TimeoutException, NoSuchElementException):
                break
            except Exception as e:
                pass

            try:
                # Alert 버튼 찾기
                alert_button = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.btnArea button.pop.sky.full")))
                if alert_button:
                    alert_button.click()
                else:
                    certificate = True
                    break

            except (TimeoutException, NoSuchElementException):
                break
            except Exception as e:
                pass
