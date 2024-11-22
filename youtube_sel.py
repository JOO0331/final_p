from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Chrome 옵션 설정 (헤드리스 모드 + User-Agent 설정)
chrome_options = Options()
chrome_options.add_argument("--headless")  # 화면을 표시하지 않음 (헤드리스 모드)
chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화
chrome_options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')  # User-Agent 설정

# Chrome WebDriver 설정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# YouTube 비디오 URL
video_id = 'ESrJX0OIIwc'  # 예시 비디오 ID  ESrJX0OIIwc thDV5A0IULs
url = f'https://www.youtube.com/watch?v={video_id}'

# YouTube 비디오 페이지 열기
driver.get(url)

# 페이지가 완전히 로드될 때까지 대기 (최대 10초)
try:
    # 게임 이름 추출 (첫 번째 XPath)
    game_name_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/ytd-metadata-row-container-renderer/div[1]/ytd-rich-metadata-row-renderer/div/ytd-rich-metadata-renderer[1]/a/div[2]/div[1]'))
    )
    game_name = game_name_element.text  # 게임 이름 추출

    # 출시 연도 추출 (두 번째 XPath)
    release_year_element = driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/ytd-metadata-row-container-renderer/div[1]/ytd-rich-metadata-row-renderer/div/ytd-rich-metadata-renderer[1]/a/div[2]/div[2]')
    release_year = release_year_element.text  # 출시 연도 추출

    # 결과 출력
    print("게임명:", game_name)
    print("출시 연도:", release_year)

except Exception as e:
    print(f"오류 발생: {e}")

# 브라우저 종료
driver.quit()