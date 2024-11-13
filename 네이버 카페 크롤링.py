#https://velog.io/@mino0121/Python-Selenium%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%9C-Naver-cafe-%EA%B2%8C%EC%8B%9C%EB%AC%BC-%ED%85%8D%EC%8A%A4%ED%8A%B8-%EC%8A%A4%ED%81%AC%EB%9E%98%ED%95%91-2
import time
import pickle
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm

def open_browser():
    op = webdriver.ChromeOptions()
    chrome_service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service = chrome_service, options=op)
    return driver

def naver_login(naver_id, naver_pw):
    driver.get("https://nid.naver.com/nidlogin.login")

    try:
        driver.find_element(By.CSS_SELECTOR,'#id') #예외처리에 필요 이 구문이 없으면 아이디가 클립보드에 계속 복사됨
        time.sleep(2)

        pyperclip.copy(my_id)
        driver.find_element(By.CSS_SELECTOR,'#id').send_keys(Keys.CONTROL+'v')
        time.sleep(1)

        pyperclip.copy(my_pw)
        secure='blank'
        driver.find_element(By.CSS_SELECTOR,'#pw').send_keys(Keys.CONTROL + 'v')
        pyperclip.copy(secure)  #비밀번호 보안을 위해 클립보드에 blank 저장

        driver.find_element(By.XPATH,'//*[@id="log.login"]').click()
    except:
        print("no such element")          #예외처리

# Example login credentials
my_id = ""
my_pw = ""

urls = {"쇼핑떼샷&인증": "https://cafe.naver.com/momsolleh?iframe_url=/ArticleList.nhn%3Fsearch.clubid=25312684%26search.menuid=2743%26search.boardtype=L",
        "텍스리펀&쇼핑팁": "https://cafe.naver.com/momsolleh?iframe_url=/ArticleList.nhn%3Fsearch.clubid=25312684%26search.menuid=1235%26search.boardtype=L",
       }
cities = urls.keys()  # ['쇼핑떼샷&인증', '텍스리펀&쇼핑팁']

data = []

max_board = 1  # 게시판별로 탐색할 최대 페이지 수

# 셀레니움 브라우저 오픈
driver = open_browser()

# 최초 로그인
naver_login(my_id, my_pw)

# 최대 대기 시간 설정 : 페이지가 다 로드되지 않았을 때 element를 찾다가
# 오류가 나는 것을 방지하기 위한 설정. 최대 50초까지 기다리고,
# 그 이전에 페이지가 로드되면 자동으로 다음 명령을 실행한다.
driver.implicitly_wait(50)

# 각 지역별로 게시판에 접속하여 순회
for city in cities:
    for i in tqdm(range(1, max_board + 1)):
        driver.get(urls[city] + str(i))
        driver.switch_to.frame("cafe_main")
        time.sleep(2)

        for j in range(1, 51):
            # 페이지 오류 등으로 게시물 목록이 오픈되지 않으면 순회 중단
            try:
                driver.find_element(By.XPATH,
                                    f'//*[@id="main-area"]/div[4]/table/tbody/tr[{j}]/td[1]/div[2]/div/a[1]').send_keys(
                    Keys.CONTROL + "\n")
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(3.5)
                driver.switch_to.frame("cafe_main")
                time.sleep(0.5)
            except:
                break

            # 게시물 이상 등으로 데이터를 추출하지 못하더라도 다음 게시물로 넘어가도록 설정
            try:
                city_name = city
                cont_url = driver.find_element(By.XPATH, '//*[@id="spiButton"]').get_attribute('data-url')
                cont_num = cont_url.split("/")[-1]
                cont_date = driver.find_element(By.CLASS_NAME, 'date').text
                cont_author = driver.find_element(By.CLASS_NAME, 'nickname').text
                cont_title = driver.find_element(By.CLASS_NAME, 'title_text').text
                cont_text = driver.find_element(By.CLASS_NAME, 'se-main-container').text
            except:
                pass

            if len(cont_text) > 0:
                data.append([city_name, cont_url, cont_num, cont_date, cont_author, cont_title, cont_text])

            # 띄워 놓은 새 탭을 닫고 이전 탭(게시판)으로 이동
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            driver.switch_to.frame("cafe_main")

        # 추가한 데이터가 2021년 이전 데이터일 경우 탐색을 중단
        if cont_date[:4] <= '2020':
            break

        if i % 2 == 0:  # 게시물 100개 탐색 시마다 데이터 저장 후 브라우저 재시작
            # 크롤링한 데이터를 pickle 파일로 저장
            with open("./naver_vietnam_city_review.pkl", 'wb') as f:
                pickle.dump(data, f)

            # 브라우저 재시작
            driver.quit()
            time.sleep(1)
            driver = open_browser()
            time.sleep(1)
            naver_login(my_id, my_pw)
            time.sleep(1)

    # 도시별 탐색이 마무리될 때마다 데이터 저장
    with open("./naver_vietnam_city_review.pkl", 'wb') as f:
        pickle.dump(data, f)

