import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


#############################################################################
#                                 << 설정값 >>
# 헤더 설정
headers_louisvuitton = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Referer": "https://kr.louisvuitton.com/kor-kr/women/handbags/_/N-tfr7qdp",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ko-KR,ko;q=0.9"
}

# 목적에 맞는 헤더를 설정한다
headers = headers_louisvuitton


###############################################################################
#                                 << 함수들 >>                                 #
###############################################################################

# get_driver()
# 사용 전제 조건 : Users 폴더에 버전에 맞는 chromedriver.exe를 다운받아주세요
# 기능 : driver를 반환합니다
# 리턴값 : driver
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


#############################################################################
# get_soup()
# 기능 : url을 받아 requests를 사용하여 soup를 리턴하는 함수입니다
# 특징 : 오류발생 시 재귀하기 때문에, 성공적으로 soup를 받아올 수 있습니다.
def get_soup(url, time_sleep=0, max_retries=600):
    try:
        print("in soup")
        if max_retries <= 0:
            print("[최대 재시도 횟수 초과 : get_soup()]")
            return None
        with requests.Session() as session:
            response = session.get(url, headers=headers)
            time.sleep(time_sleep)
        soup = BeautifulSoup(response.text, "html.parser")
        print(soup)
        if len(soup) == 0:  # 불러오는데 실패하면
            print(f"[soup 로딩 실패, 반복] [get_soup(time_sleep=1)]")
            soup = get_soup(url, 1)
    except Exception as e:
        print(f"[오류 발생, 반복] [get_soup(time_sleep=1)] ", e)
        soup = get_soup(url, 1, max_retries-1)
    return soup



# lv
#####################################
# 기능 : 에러 로그를 검사하고, 에러가 있으면 csv 파일을 만든다
def check_error_logs(error_logs, file_path_='./'):
    # error 발생 했는지 확인
    max_print_count = 5
    if len(error_logs) > 0:                             # 에러 로그가 존재하면
        print("[에러 발생 로그 입니다]")
        for index, error_log in enumerate(error_logs):  # 에러 로그를 출력한다
            print(f"[Index {index}] {error_log[-1]}")
            if index >= max_print_count:                # 사용자에게 보여주기 위해 출력하는 용도이므로, 조금만 출력
                break
        error_log_columns = ['crawler_type', 'error_info']
        df_error_logs = pd.DataFrame(error_logs, columns=error_log_columns)        # df 생성 후 .csv 파일로 저장
        df_error_logs.to_csv(file_path_, encoding='ANSI', index=False)
        print(f"[총 {len(error_logs)}개의 에러 로그가 파일로 저장되었습니다]")
    else:                                               # 에러가 존재하지 않으면, 종료
        print("[에러가 없었습니다]")
    return len(error_logs)

