# 지역별 구글맵 데이터 가져오기(미완성)
from selenium import webdriver
from itertools import count
import time
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import shutil, os

target_data = pd.read_csv('./temp/international_data.csv', engine='python')

#나중에 지역별 사진폴더를 만들 기본 주소(개별 pc에서 돌리려면 폴더 주소 지정하셔야 합니다. 그리고 파일명 구분은 /로 다 바꾸셔야 함)
base_dir_img = 'C:/Users/gypig/OneDrive/문서/project/관광지사진/국내'
base_dir_csv = 'C:/Users/gypig/OneDrive/문서/project/관광지자료'

final_result = []
# 추출할 데이터 지정하기
target_name = ['h1', 'span', 'div']        # 찾고자 하는 데이터의 태그(순서 : 관광지이름, 별점, 간략설명)
target_class = [                           # 찾고자하는 데이터의 태그들의 클래스
    {'class':"section-hero-header-title-title GLOBAL__gm2-headline-5"},
    {'class':"section-star-display"},
    {'class':"section-editorial-quote"},
]

for data in target_data.index:
    hint = target_data.iloc[data,0][:2]
    name = target_data.iloc[data][2]
    # 네이버 열기
    url = 'https://www.google.co.kr/maps/search/' + name
    driver = webdriver.Chrome(executable_path="./chromedriver.exe")
    driver.get(url) 
    time.sleep(4)
    
    # csv 자료를 담아놓을 폴더 만들기(이미 만든것이 있다면 지우고 폴더 만들기, 없다면 만들기)
    # 경로 선언
    csv_path = base_dir_csv  # base_dir_img + 지역이름
    if os.path.exists(csv_path):
        pass
    else:
        os.makedirs(csv_path)
    
    # 사진을 담아놓을 폴더 만들기(이미 만든것이 있다면 지우고 폴더 만들기, 없다면 만들기)
    # 경로 선언
    img_path = base_dir_img + '/' + str(hint) #se_dir_img + 지역이름
    if os.path.exists(img_path):
        pass
    else:
        os.makedirs(img_path)
    
    
    rcv_data = driver.page_source                       # 검색한 웹페이지 소스코드 긁어오기
    soupData = BeautifulSoup(rcv_data, 'html.parser')   # html이라는 부분 데이터를 가져옴
    datas = soupData.find('div',{'class':'section-layout section-layout-root'})          # 긁어오고자 하는 데이터들이 담긴 div~ 데이터들
    try:
        # 데이터 추출 및 정돈하여 저장
        r_data = []                          # 웹페이지에서 문자만을 담을 변수(정돈할 변수)
        for i in range(len(target_name)):    # 3개의 데이터 돌아가면서 찾기
            for data in datas.findAll(target_name[i],target_class[i]):
                temp = list(data.strings)
                #print(temp)
                if (len(temp) == 4) | (len(temp) == 3):
                    r_data.append([temp[1]])
                else:
                    r_data.append(temp)
                            
        # 데이터가 없는 경우에 대한 전처리
        if len(r_data) ==1:
            r_data.append('-')
        if len(r_data) == 2:
            r_data.append('-')
                    
        final_result.append(r_data) # 마지막에 정돈된 하나의 행 데이터를 결과에 추가
        
        img_data = datas.find('div', {'class':'section-hero-header-image'})
        # 태그데이터 안의 src 경로 얻어오기
        imgUrl = img_data.find('img').get('src')
        if imgUrl[:2] =='//':
            imgUrl = 'https:' + imgUrl
        urllib.request.urlretrieve(imgUrl, img_path + '/' + str(r_data[0][0]) +'.jpg')    # 폴더에 사진 저장
        driver.close()
    except:
        driver.close()
    
df = pd.DataFrame(final_result,columns=['Name','Score','Description'])
df.to_csv(csv_path+'.csv', encoding='utf-8')
