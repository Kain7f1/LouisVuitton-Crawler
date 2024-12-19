# import pandas as pd
#
# data = []
#
# for i in range(3):
#     for j in range(4):
#         data.append([f"제품 {i}", j, i*j, i-j])
#
#
# df = pd.DataFrame(data, columns=["product_name", "price", "product_url", "image_url"])
#
# # 엑셀 파일로 저장
# excel_file_name = "ex.csv"
# df.to_csv(excel_file_name, encoding="ANSI", index=False)
#
# print(f"데이터가 {excel_file_name} 파일로 저장되었습니다.")


import crawling_tool as cr
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("[크롬 드라이버 세팅중]")
driver = cr.get_driver()  # 크롬 웹드라이버
driver.get("https://kr.louisvuitton.com/kor-kr/women/handbags/_/N-tfr7qdp")
print("[크롬 드라이버 세팅 완료]")
print("[프로세스 1 - 맨 밑까지 스크롤]")
element = driver.find_element("tag name", "body")  # body 태그를 찾아 element 변수에 저장
scroll_count = 30  # 스크롤 할 횟수

# 스크롤 다운
for i in range(1, scroll_count + 1):
    print(f"{i}번째 스크롤")
    element.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)  # 스크롤 사이 로딩 시간 고려 (필요에 따라 조절)

print("[프로세스 1 완료]")

# -------------------------------------

print("[프로세스 2 - 모든 더보기 버튼 클릭]")
max_button_count = 9  # 더보기 버튼 갯수
for j in range(1, max_button_count + 1):
    print(f"{j}번째 버튼 클릭")
    try:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f"/html/body/div[1]/div/div/main/div/div[3]/ul/li[{j}]/div/div/button"))
        )
        # Javascript를 사용하여 버튼 클릭
        driver.execute_script("arguments[0].click();", button)
        print(f"{j}번쨰 버튼 클릭 성공!")

    except Exception as e:
        print(f"버튼 클릭 실패 ㅠㅠ: {e}")

print("[프로세스 2 완료]")

for i in range(1, 9 + 1):
    # XPath를 사용하여 모든 li 요소를 찾습니다.
    elements = driver.find_elements(By.XPATH, f"/html/body/div[1]/div/div/main/div/div[3]/ul/li[{i}]/div/ul/li")


    # 찾은 요소의 개수를 출력합니다.
    print(f"그룹 {i}의 제품 수: {len(elements)}")

driver.quit()

time.sleep(10)