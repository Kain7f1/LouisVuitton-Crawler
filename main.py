#############################################################################
# 만든이 : Kain7f1 (Hansol Lee)
# 생성일 : 2024-12-16
# 사용 전제 조건 : C:\Users 폴더에 현재 크롬 버전에 맞는 chromedriver.exe를 다운받아주세요
# 목적 : 크롤링 및 정보 엑셀에 저장 - "https://kr.louisvuitton.com/kor-kr/women/handbags/_/N-tfr7qdp"
# 요구사항 1 - 모든 상품 정보 엑셀로 저장 : 1. 상품명 / 2. 가격 / 3. 상품 링크 URL / 4. 이미지 URL
# 요구사항 2 - 페이지 군데군데 더보기 버튼을 눌러 모든 상품을 로딩 후 크롤링 작업 시작
# 요구사항 3 - 코드로 인한 접속시 사이트 차단 우회

from lv_crawler import crawl_lv

target_url = "https://kr.louisvuitton.com/kor-kr/women/handbags/_/N-tfr7qdp"

crawl_lv(target_url)