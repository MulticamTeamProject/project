# 지역별 구글맵 데이터 가져오기
from selenium import webdriver
from itertools import count
import time
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import shutil, os

#나중에 지역별 사진폴더를 만들 기본 주소(개별 pc에서 돌리려면 폴더 주소 지정하셔야 합니다. 그리고 파일명 구분은 /로 다 바꾸셔야 함)
base_dir_img = './data_set/해외관광지사진'
base_dir_csv = './data_set/해외관광지자료'

nation = '스페인' # 나라이름
location = ['바야돌리드'] # 나라 안에 포함된 지역이름
# final_result = [] # 최종 데이터 저장변수

# csv 자료를 담아놓을 폴더 만들기(이미 만든것이 있다면 넘어가고 없다면 만들기)
# 경로 선언
csv_path = base_dir_csv + '/' + str(nation)  # base_dir_csv + 나라이름
if os.path.exists(csv_path):
    #shutil.rmtree(csv_path)  
    #os.makedirs(csv_path)
    pass
else:
    os.makedirs(csv_path)

for loc in location:
    final_result = [] # 최종 데이터 저장변수
    # 사진을 담아놓을 폴더 만들기(이미 만든것이 있다면 지우고 폴더 만들기, 없다면 만들기)
    # 경로 선언
    img_path = base_dir_img + '/' + str(nation) + '/' + str(loc)  # base_dir_img + 나라이름 + 지역이름
    if os.path.exists(img_path):
        pass
    else:
        os.makedirs(img_path)

    target = str(loc) + ' 관광명소'
    url = 'https://www.google.com/maps/?hl=ko'
    driver = webdriver.Chrome(executable_path="./chromedriver.exe")
    driver.get(url) # 드라이버로 열기
    time.sleep(4)
    driver.find_element_by_xpath('//*[@id="searchboxinput"]').send_keys(target) # 검색어 입력
    driver.find_element_by_xpath('//*[@id="searchbox-searchbutton"]').click() # 검색클릭
    time.sleep(4)

    for _ in range(0,1):
        
        for i in range(3,42,2): # 40까지 해야 20개 추출함

            # 페이지별 항목들에 대한 접근
            xpath = '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[' + str(i) + ']' # 요소별 클릭 주소
            driver.find_element_by_xpath(xpath).click()                                 # 요소클릭
            time.sleep(4)

            # 항목에 대한 정보 받아오기
            rcv_data = driver.page_source                       # 검색한 웹페이지 소스코드 긁어오기
            soupData = BeautifulSoup(rcv_data, 'html.parser')   # html이라는 부분 데이터를 가져옴
            datas = soupData.find('div',{'id':'pane'})          # 긁어오고자 하는 데이터들이 담긴 div~ 데이터들

            # 추출할 데이터 지정하기
            target_name = ['h1', 'span', 'div']        # 찾고자 하는 데이터의 태그(순서 : 관광지이름, 별점, 간략설명)
            target_class = [                           # 찾고자하는 데이터의 태그들의 클래스
                {'class':"section-hero-header-title-title GLOBAL__gm2-headline-5"},
                {'class':"section-star-display"},
                {'class':"section-editorial-quote"},
            ]

            # 데이터 추출 및 정돈하여 저장
            r_data = []                          # 웹페이지에서 문자만을 담을 변수(정돈할 변수)
            for i in range(len(target_name)):    # 3개의 데이터 돌아가면서 찾기
                for data in datas.findAll(target_name[i],target_class[i]):
                    temp = list(data.strings)
                    #print(temp)
                    if (len(temp) == 4) | (len(temp) == 3):
                        r_data.append(temp[1])
                    else:
                        r_data.append(temp[0])
                        
            # 데이터가 없는 경우에 대한 전처리
            if len(r_data) ==1:
                r_data.append('-')
            if len(r_data) == 2:
                r_data.append('-')
                
            final_result.append(r_data) # 마지막에 정돈된 하나의 행 데이터를 결과에 추가
            try:   
                # 이미지 저장하기
                # 사진이 담겨있는 태그데이터를 긁어오기
                img_data = datas.find('div', {'class':'section-hero-header-image-hero-container collapsible-hero-image'})
                # 태그데이터 안의 src 경로 얻어오기
                imgUrl = img_data.find('img').get('src')
                if imgUrl[:2] =='//':
                    imgUrl = 'https:' + imgUrl
                urllib.request.urlretrieve(imgUrl, img_path + '/' + str(r_data[0]) +'.jpg')    # 폴더에 사진 저장
            except:
                pass
    
            driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/button').click() # 뒤로가기
            time.sleep(5)
        
        try:
            # 페이지 하나 넘어가기
            driver.find_element_by_xpath('//*[@id="n7lv7yjyC35__section-pagination-button-next"]/span').click()
            time.sleep(5)
        except:
            pass

    driver.close()      # 브라우저 종료

    df = pd.DataFrame(final_result,columns=['Name','Score','Description'])
    df.to_csv(csv_path + '/' + str(loc) + '.csv', encoding='utf8')