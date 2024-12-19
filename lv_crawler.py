#############################
# 만든이 : Kain7f1 (Hansol Lee)
# 생성일 : 2024-12-16
# 사용 전제 조건 : C:\Users 폴더에 현재 크롬 버전에 맞는 chromedriver.exe를 다운받아주세요
# 목적 : 크롤링 및 정보 엑셀에 저장 - "https://kr.louisvuitton.com/kor-kr/women/handbags/_/N-tfr7qdp"
# 요구사항 1 - 모든 상품 정보 엑셀로 저장 : 1. 상품명 / 2. 가격 / 3. 상품 링크 URL / 4. 이미지 URL
# 요구사항 2 - 페이지 군데군데 더보기 버튼을 눌러 모든 상품을 로딩 후 크롤링 작업 시작
# 요구사항 3 - 코드로 인한 접속시 사이트 차단 우회
#############################

from datetime import datetime
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 기능 : 크롬 driver 옵션을 설정하고 반환합니다
def get_driver():
    CHROME_DRIVER_PATH = "C:/Users/chromedriver.exe"    # (절대경로) Users 폴더에 chromedriver.exe를 설치했음
    options = webdriver.ChromeOptions()                 # 옵션 선언
    # [옵션 설정]
    options.add_argument("--start-maximized")         # 창이 최대화 되도록 열리게 한다.
    # options.add_argument("--headless")                  # 창이 없이 크롬이 실행이 되도록 만든다

    options.add_argument("disable-infobars")            # 안내바가 없이 열리게 한다.
    options.add_argument("disable-gpu")                 # 크롤링 실행시 GPU를 사용하지 않게 한다.
    options.add_argument("--disable-dev-shm-usage")     # 공유메모리를 사용하지 않는다
    options.add_argument("--blink-settings=imagesEnabled=false")    # 이미지 로딩 비활성화
    options.add_argument('--disk-cache-dir=/path/to/cache-dir')     # 캐시 사용 활성화
    options.page_load_strategy = 'none'             # 전체 페이지가 완전히 로드되기를 기다리지 않고 다음 작업을 수행 (중요)
    options.add_argument('--log-level=3')           # 웹 소켓을 통한 로그 메시지 비활성화
    options.add_argument('--no-sandbox')            # 브라우저 프로파일링 비활성화
    options.add_argument('--disable-plugins')       # 다양한 플러그인 및 기능 비활성화
    options.add_argument('--disable-extensions')    # 다양한 플러그인 및 기능 비활성화
    options.add_argument('--disable-sync')          # 다양한 플러그인 및 기능 비활성화
    driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)
    return driver


def crawl_lv(url):
    print("[기본값 세팅]")
    start_time = datetime.now().replace(microsecond=0)  # 시작 시각
    # 결과 파일 이름에 시작시간을 넣어 unique한 이름이 되도록 하고, 기존 파일을 덮어씌우는 일이 없도록 한다.
    str_start_time = str(start_time)[2:10].replace("-", "") + "_" + str(start_time)[11:].replace(":", "")

    # -------------------------------------

    # [크롤링]
    # 요구사항 1 - 모든 상품 정보 엑셀로 저장 : 1. 상품명 / 2. 가격 / 3. 상품 링크 URL / 4. 이미지 URL
    # 요구사항 2 - 페이지 군데군데 더보기 버튼을 눌러 모든 상품을 로딩 후 크롤링 작업 시작
    # 요구사항 3 - 코드로 인한 접속시 사이트 차단 우회

    # 프로세스 1 - 맨 밑까지 스크롤
    # 프로세스 2 - 모든 더보기 버튼 클릭
    # 프로세스 3 - 모든 정보 불러와서 엑셀 형태로 저장

    print("[크롬 드라이버 세팅중]")
    driver = get_driver()  # 크롬 웹드라이버. 드라이버 옵션 미리 설정해 두었음
    driver.get("https://kr.louisvuitton.com/kor-kr/women/handbags/_/N-tfr7qdp")  # 타겟 url : 루이비통
    print("[크롬 드라이버 세팅 완료]")

    print("[프로세스 1 - 맨 밑까지 스크롤]")
    element = driver.find_element("tag name", "body")  # body 태그를 찾아 element 변수에 저장
    scroll_count = 30  # 스크롤 할 횟수

    # 스크롤 다운
    for i in range(1, scroll_count+1):
        print(f"{i}번째 스크롤")
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)  # 스크롤 사이 로딩 시간 고려 (필요에 따라 조절)

    print("[프로세스 1 완료]")

    # -------------------------------------

    print("[프로세스 2 - 모든 더보기 버튼 클릭]")
    max_group_count = 9  # 더보기 버튼 갯수 = 제품군의 갯수
    for group_count in range(1, max_group_count+1):
        # 버튼클릭
        print(f"{group_count}번째 더보기 버튼 클릭")
        try:
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"/html/body/div[1]/div/div/main/div/div[3]/ul/li[{group_count}]/div/div/button"))
            )
            # Javascript를 사용하여 버튼 클릭
            driver.execute_script("arguments[0].click();", button)
            print(f"{group_count}번쨰 더보기 버튼 클릭 성공!")

        except Exception as e:
            print(f"더보기 버튼 클릭 실패 ㅠㅠ: {e}")
            return  # 정보 다 못불러오면 종료

    print("[프로세스 2 완료]")

    # -------------------------------------

    print("[프로세스 3 - 모든 정보 불러와서 엑셀 형태로 저장]")
    # 1. 제품명 / 2. 가격 / 3. 제품 링크 URL / 4. 이미지 URL

    data = []

    for group_count in range(1, max_group_count+1):
        # 제품 수 세고, 그만큼 for문 돌림
        product_elements = driver.find_elements(By.XPATH, f"/html/body/div[1]/div/div/main/div/div[3]/ul/li[{group_count}]/div/ul/li")  # 제품군 안의 제품 element
        len_products = len(product_elements)-1  # 제품군 안의 제품 수, for문 위해 필요. elements중 맨앞 1개는 제품 아니라서 -1
        print(f"group {i}의 제품 수: {len_products}")

        for product_count in range(1, len_products+1):  # 임의의 큰 숫자까지 반복문 돌리면, 알아서 break 한다.
            # 제품명, 제품 링크 URL의 xpath를 찾기 위해 필요한 작업.
            div_elements = driver.find_elements(By.XPATH,
                                                f"/html/body/div[1]/div/div/main/div/div[3]/ul/li[{group_count}]/div/ul/li[{product_count+1}]/div/div[1]/div[1]/div[1]/div[*]")  # 제품명, 제품 링크 URL이 있는 계층
            len_div_elements = len(div_elements)  # 쓸데없는 정보 1개 앞에 포함되어있으면 3개, 아니면 '제품명', '제품 링크 URL'의 2개이다.
            print(f"div 요소의 개수: {len_div_elements}")

            base_xpath = f"/html/body/div[1]/div/div/main/div/div[3]/ul/li[{group_count}]/div/ul/li[{product_count+1}]"  # html 까보니 처음 제품의 것이 li[2]이다
            product_info_xpath = base_xpath + f"/div/div[1]/div[1]/div[1]/div[{len_div_elements-1}]/h2/a"  # 제품명, 제품 링크 URL
            price_xpath = base_xpath + f"/div/div[1]/div[1]/div[1]/div[{len_div_elements}]/span"  # 가격 정보

            try:
                print(f"group {group_count}, product {product_count} 제품 정보 크롤링 중")

                # 1. 제품명, 3. 제품 링크 URL
                product_info_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, product_info_xpath))
                )  # 최대 5초 동안 `product_info_xpath` XPath에 해당하는 요소가 로드될 때까지 기다리고, 찾은 요소를 저장함.

                product_url = product_info_element.get_attribute("href")  # 3. 제품 링크 URL
                print(f"Product_url: {product_url}")
                product_name = product_info_element.text  # 1. 제품명
                print(f"Product_name: {product_name}")

                # 2. 가격
                price_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, price_xpath))  # XPATH로 로드 : 가격 정보
                )
                price = price_element.text  # 2. 가격
                price = price[1:]  # 원화기호 제거
                print(f"Price: {price}")

                # 4. 이미지 URL
                product_code = ""  # 제품 코드. ex) M13617
                parts = product_url.split("/")
                if parts:
                    product_code = parts[-1]
                # 이미지 URL은 일정한 형식을 띄고 있음. 제품 코드만 변경해 주면 된다. 불필요하게 요청을 보내지 않아도 해결 가능.
                image_url = f"https://kr.louisvuitton.com/images/is/image/lv/1/PP_VP_L/{product_code}_PM2_Front%20view.png"
                print(f"이미지 URL: {image_url}")

                data.append([product_name, price, product_url, image_url])

            except Exception as e:
                print(f"group {group_count}, product {product_count} 제품 정보 추출 실패: {e}")
                continue

    driver.quit()  # 드라이버 종료

    print("[엑셀 형태로 저장]")
    # 수집한 데이터를 데이터프레임 형태로 변환
    df = pd.DataFrame(data, columns=["product_name", "price", "product_url", "image_url"])

    # 엑셀 파일로 저장
    excel_file_name = f"product_{str_start_time}.csv"   # 엑셀 파일 이름. 시작시간을 덧붙어 unique하게 만들어 여러번 실행해도 파일이 덧씌워지지 않음.
    df.to_csv(excel_file_name, encoding="ANSI", index=False)  # 한글로 보이도록 인코딩 ANSI로 설정
    print(f"데이터가 {excel_file_name} 파일로 저장되었습니다.")

    print("[프로세스 3 완료]")
    print("crawl_lv() 종료")
