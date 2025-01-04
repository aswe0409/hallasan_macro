# 한라산 예약 메크로

# 1. 코스 정하고
# 2. 예약 가능한지 확인
# 2-1 예약 가능
# 2-2 예약 불가능

# 3. 예약 불가능일 때 
# 성판악이면 -> 관음사로
# 관음사면 성판악으로 반복

# 4. 예약 가능일 때
# 예약하기로 들어가 and stop

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time


# 1. webdriver 설정
def setup_driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    return driver

# 2. 코스 설정 디폴트 성판악
def choose_route(driver):
    #현재 성판악이면 관음사로, 관음사면 성판악으로
    select_element = driver.find_element(By.ID, "courseSeq")
    select = Select(select_element)
    
    current_option = select.first_selected_option
    current_value = current_option.get_attribute("value")
    
    print(f"현재 선택된 코스: {current_option.text} (value: {current_value})")

    # 코스 변경
    if current_value == "242":  # 성판악
        select.select_by_value("244")  # 관음사로 변경
        print("코스를 관음사로 변경했습니다.")
    elif current_value == "244":  # 관음사
        select.select_by_value("242")  # 성판악으로 변경
        print("코스를 성판악으로 변경했습니다.")
    else:
        print("알 수 없는 코스입니다. 기본값으로 성판악 설정.")
        select.select_by_value("242")

    # 변경 후 확인
    updated_option = select.first_selected_option
    print(f"변경된 코스: {updated_option.text} (value: {updated_option.get_attribute('value')})")
    

 # 3. 예약 가능한지 확인
def check_availability(driver, date_element_id):
    try:
        date_element = driver.find_element(By.ID, date_element_id)
        class_name = date_element.get_attribute("class")
        
        # 예약 상태 확인
        if "rev_full" in class_name:
            print(f"{date_element_id}: 예약이 꽉 찼습니다.")
            return False  # 예약 불가능
        else:
            print(f"{date_element_id}: 예약 가능합니다!")
            return True  # 예약 가능
    except Exception as e:
        print(f"예약 상태 확인 중 오류 발생: {e}")
        return False
    
def main():
    driver = setup_driver()
    driver.get("https://visithalla.jeju.go.kr/reservation/status.do")
    
    성판악_date_id = "TD_20250109"
    관음사_date_id = "TD_20250109"

    while True:
        try:
            # 현재 선택된 코스에 따라 예약 상태 확인
            choose_route(driver)  # 코스를 변경
            current_route_id = 성판악_date_id if driver.find_element(By.ID, "courseSeq").get_attribute("value") == "242" else 관음사_date_id

            if check_availability(driver, current_route_id):
                print("예약 가능! 예약 시도를 시작합니다...")
                # todo: 예약 시도 로직 추가
                break
            else:
                print("예약 불가능. 다음 코스를 확인합니다...")
                time.sleep(5)
        except Exception as e:
            print(f"메인 루프 실행 중 오류 발생: {e}")
            time.sleep(5)

    driver.quit()
    
if __name__ == "__main__":
    main()
