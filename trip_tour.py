from selenium import webdriver
from itertools import count
import time
from bs4 import BeautifulSoup
import pandas as pd

nation = ['홍콩'] # 나라이름
result = [] # 데이터 정리를 위한 임시변수
final_result = [] # 최종 데이터 저장변수

for na in nation:
    target = na + ' 관광명소'
    url = 'https://www.google.com/maps/?hl=ko'
    driver = webdriver.Chrome(executable_path="./chromedriver.exe")
    driver.get(url) # 드라이버로 열기
    time.sleep(4)
    driver.find_element_by_xpath('//*[@id="searchboxinput"]').send_keys(target) # 검색어 입력
    driver.find_element_by_xpath('//*[@id="searchbox-searchbutton"]').click() # 검색클릭
    time.sleep(4)

    for _ in range(0,3):
        for i in range(1,40,2): # 40까지 해야 20개 추출함

            xpath = '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[%d]' % (i)    # 요소별 클릭 주소
            driver.find_element_by_xpath(xpath).click()                                 # 요소클릭
            time.sleep(4)
            rcv_data = driver.page_source                       # 검색한 웹페이지 소스코드 긁어오기
            soupData = BeautifulSoup(rcv_data, 'html.parser')   # html이라는 부분 데이터를 가져옴
            datas = soupData.find('div',{'id':'pane'})          # 긁어오고자 하는 데이터들이 담긴 div~ 데이터들

            target_name = ['h1', 'span', 'div']        # 찾고자 하는 데이터의 태그(순서 : 관광지이름, 별점, 간략설명, 위도, 경도)
            target_class = [                           # 찾고자하는 데이터의 태그들의 클래스
                {'class':"section-hero-header-title-title GLOBAL__gm2-headline-5"},
                {'class':"section-star-display"},
                {'class':"section-editorial-quote"},
            ]

            r_data = []                          # 웹페이지에서 문자만을 담을 변수(정돈할 변수)
            for i in range(len(target_name)):    # 4개의 데이터 돌아가면서 찾기
                for data in datas.findAll(target_name[i],target_class[i]):
                    temp = list(data.strings)
                    if (len(temp) == 4) | (len(temp) == 3):
                        r_data.append([temp[1]])
                    else:
                        r_data.append(temp)

            if len(r_data) == 2:
                r_data.append('-')              # 앞에서 간략설명에 대한 데이터 태그가 없는 경우에 - 를 추가하여 데이터 전처리

            current_url = driver.current_url    # 위도,경도를 받기위한 현재주소 얻어오기
            current_url = current_url.split('@')    
            current_url = current_url[1].split(',') 
            r_data.append([current_url[0]]) # 위도
            r_data.append([current_url[1]]) # 경도

            result.append(r_data) # 마지막에 정돈된 하나의 행 데이터를 추가 / 근데 이때 살펴보면 알겠지만 12개 중에 필요없는 데이터 발생

            driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/button').click() # 뒤로가기
            time.sleep(5)

        driver.find_element_by_xpath('//*[@id="n7lv7yjyC35__section-pagination-button-next"]/span').click()
        time.sleep(5)

    driver.close()      # 브라우저 종료

    for x in result:    # 최종데이터 정리하여 추가
        temp = []
        for i in range(0,len(target_name)):
            temp.append(x[i][0])
        temp.append(x[-2][0])
        temp.append(x[-1][0])
        final_result.append(temp)

    df = pd.DataFrame(final_result,columns=['Name','Score','Description','Latitude','Longitude'])
    df.to_csv('test.csv', encoding='cp949')