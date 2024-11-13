from bs4 import BeautifulSoup
import requests
import re
import time
import os
import sys
import urllib.request
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import pandas as pd

# 이미지 저장 폴더 생성
os.makedirs("images", exist_ok=True)


# 웹드라이버 설정
options = webdriver.ChromeOptions()
# 크롬 브라우저에서 자동화 탐지 기능 비활성화로 일반적인 사용자로 인식하게 함
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

## 버전에 상관 없이 os에 설치된 크롬 브라우저 사용
options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # 컴퓨터에 맞게 크롬 경로 지정
service = Service(ChromeDriverManager().install())         # 크롬 드라이버 자동 다운로드
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(3)                # 암시적 대기 시간 설정하여 로딩 기다림
driver.get("https://www.google.com")
# 버전에 상관 없이 os에 설치된 크롬 브라우저 사용


# Naver API key 입력
client_id = 'rUMrDAYkvqoyvnITE284'
client_secret = 'Y4ykyPLEie'

# selenium으로 검색 페이지 불러오기 #
naver_urls = []
postdate = []
titles = []

# 검색어 입력
keword = input("검색할 키워드를 입력해주세요:")
encText = urllib.parse.quote(keword)    # 검색어를 url 인코딩

# 검색을 끝낼 페이지 입력
end = input("\n크롤링을 끝낼 위치를 입력해주세요. (기본값:1, 최대값:100):")
if end == "":
    end = 1
else:
    end = int(end)
print("\n 1 ~ ", end, "페이지 까지 크롤링을 진행 합니다")

# 한번에 가져올 페이지 입력
display = input("\n한번에 가져올 페이지 개수를 입력해주세요.(기본값:10, 최대값: 100):")
if display == "":
    display = 10
else:
    display = int(display)
print("\n한번에 가져올 페이지 : ", display, "페이지")

# Naver 블로그 검색 함수
for start in range(end):
    url = "https://openapi.naver.com/v1/search/blog?query=" + encText + "&start=" + str(start + 1) + "&display=" + str(
        display + 1)
    # JSON 결과 (encText : 검색할 키워드, start : 검색을 시작할 페이지, display : 한 번에 가져올 검색 결과)
    request = urllib.request.Request(url)  # 인코딩
    request.add_header("X-Naver-Client-Id", client_id) # API 키 추가
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request) # 네이버 API 서버에 HTTP 요청을 보내고 응답을 받은 걸 response에 저장
    rescode = response.getcode()  # 응답코드(HTTP)를 가져옴.(일반적으로 200이 성공)
    if (rescode == 200):
        response_body = response.read()
        data = json.loads(response_body.decode('utf-8'))['items']   # 읽어온 걸 UTF8로 인코딩/items를 추출 후 JSON으로 저장
        for row in data:
            if ('blog.naver' in row['link']):
                naver_urls.append(row['link'])  # URL
                postdate.append(row['postdate']) # 작성날짜
                title = row['title']   # 제목
                # html태그제거
                pattern1 = '<[^>]*>'  # 정규표현식을 이용하여 HTML 태그 제거
                title = re.sub(pattern=pattern1, repl='', string=title) # 위 정규표현식에 해당하는 태그를 빈 문자열로 대체
                titles.append(title)

                ## 가져올 수 있는 목록
                # title: 블로그 글의 제목
                # link: 해당 블로그 글의 URL
                # description: 블로그 글의 요약(본문 중 일부)
                # bloggername: 블로그 작성자 이름
                # bloggerlink: 블로그의 홈 링크
                # postdate: 블로그 글의 작성일 (YYYYMMDD 형식)

        time.sleep(2)  # 서버에 과도한 요청을 보내지 않게 하기 위해 2초 설정
    else:
        print("Error Code:" + rescode)

###naver 기사 본문 및 제목 가져오기###

# ConnectionError방지(일반 브라우저로 인식하게 만드는 기능)
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

contents = []
all_images = []
try:
    for idx, url in enumerate(naver_urls):
        print(f"크롤링중 : {url}")
        driver.get(url) # 블로그 페이지를 드라이버로 오픈
        time.sleep(3)  # 대기시간 변경 가능

        iframe = driver.find_element(By.ID, "mainFrame")  # id가 mainFrame이라는 요소를 찾아내고 -> iframe임
        driver.switch_to.frame(iframe)  # 이 iframe이 내가 찾고자하는 html을 포함하고 있는 내용. 찾은 iframe으로 포커스 전환

        source = driver.page_source  # 현재 html 소스를 가져옴.(본문 내용 포함)
        html = BeautifulSoup(source, "html.parser") # HTML 소스 파싱
        # 검색결과 확인용
        # with open("Output.txt", "w") as text_file:
        #     text_file.write(str(html))

        # 기사 텍스트만 가져오기
        content = html.select("div.se-main-container") # 블로그 본문을 나타내는 컨테이너 클래스
        #  list합치기
        content = ''.join(str(content)) # 리스트형태로 도출된 것을 하나의 문자열로 합침.

        # html태그제거 및 텍스트 다듬기
        content = re.sub(pattern=pattern1, repl='', string=content)  # HTML 태그 없애기
        pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
        content = content.replace(pattern2, '') # FLASH 오류 관련 텍스트를 본문에서 제거하기
        content = content.replace('\n', '') # 불필요한 개행 문자 제거
        content = content.replace('\u200b', '') # 불필요한 유니코드 제거
        contents.append(content)

        # 이미지 URL 수집 및 다운로드
        img_tags = html.select("div.se-main-container img") # 본문 내 이미지만 선택
        img_urls = []
        for img_idx, img in enumerate(img_tags):
            img_url = img.get("src")
            if img_url and img_url.startswith("http"):  # 이미지 URL 유효성 체크
                img_urls.append(img_url)
                # 이미지 URL에서 쿼리 매개변수 제거 후 파일 이름 생성
                post_id = url.split('/')[-1]
                img_name = f"{post_id}_{img_idx + 1}.jpg"
                img_path = os.path.join("images", img_name)

                try:
                    urllib.request.urlretrieve(img_url, img_path)
                    print(f"이미지 다운로드 완료: {img_name}")
                except Exception as e:
                    print(f"이미지 다운로드 실패 ({img_url}): {e}")

        # 이미지 URL 리스트를 전체 이미지 목록에 추가
        all_images.append(", ".join(img_urls))



    # CSV 파일 생성
    news_df = pd.DataFrame({
        'title': titles,
        'content': contents,
        'date': postdate,
        'link': naver_urls,
        'images': all_images
    })
    news_df.to_csv('blog.csv', index=False, encoding='utf-8-sig')

except Exception as e:
    print(f"에러 발생: {e}")

finally:
    driver.quit()