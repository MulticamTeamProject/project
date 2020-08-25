#db 접속
import pymysql
import json
import datetime

locDict = {1:'seoultbl', 2:'gangwontbl', 3:'gyeonggitbl', 4:'gyeongnamtbl', 5:'gyeongbuktbl',
                 6:'gwangjutbl', 7:'daegutbl', 8:'daejeontbl', 9:'busantbl', 10:'sejongtbl', 
                 11:'ulsantbl', 12:'incheontbl', 13:'jeonnamtbl', 14:'jeonbuktbl', 15:'jejutbl', 16:'chungnamtbl', 17:'chungbuktbl'}

city = {'seoul':'서울', 'gangwon':'강원', 'gyeonggi':'경기', 'gyeongnam':'경남', 'gyeongbuk':'경북',
                 'gwangju':'광주', 'daegu':'대구', 'daejeon':'대전', 'busan':'부산', 'sejong':'세종', 
                 'ulsan':'울산', 'incheon':'인천', 'jeonnam':'전남', 'jeonbuk':'전북', 'jeju':'제주', 'chungnam':'충남', 'chungbuk':'충북'}

# 각 테이블의 전체 리스트 가져오는 함수
def get_tourpoint_list():
    # 커서 생성
    conn = get_connection()
    cursor = conn.cursor()

    # sql문 생성
    sql = '''SELECT * FROM seoultbl  '''
    cursor.execute(sql)
    result = cursor.fetchall()

    temp_list = []
    for row in result:
        temp_dic = {}
        temp_dic['gungu'] = row[0]
        temp_dic['name'] = row[1]
        temp_dic['year'] = row[2]
        temp_dic['month'] = row[3]
        temp_dic['korean'] = row[4]
        temp_dic['foreigner'] = row[5]
        temp_list.append(temp_dic)
    
    # 접속 종료
    conn.close()
    return temp_list

# 데이터 베이스에 접속하는 함수
def get_connection() :
    conn = pymysql.connect(host='70.12.227.62', user='user2',
            password='multicampus1111', db='koreatourpointdb'
            , charset='utf8')
    if conn:
        print('f 디비 접속 완료')
    return conn

# 해외db접속
def get_connection_fo() :
    conn = pymysql.connect(host='70.12.227.62', user='user2',
            password='multicampus1111', db='countrydb'
            , charset='utf8')
    if conn:
        print('f 디비 접속 완료')
    return conn

# 특정 월/년도 인기있는 관광지 가져오는 함수
def get_popular_list():
    # 커서 생성
    conn = get_connection()
    cursor = conn.cursor()

    # sql문 생성
    sql = '''select * from seoultbl where month = 1 and year = 2020 order by korean desc limit 5; '''
    cursor.execute(sql)
    result = cursor.fetchall()

    temp_list = []
    for row in result:
        temp_dic = {}
        temp_dic['gungu'] = row[0]
        temp_dic['name'] = row[1]
        temp_dic['year'] = row[2]
        temp_dic['month'] = row[3]
        temp_dic['korean'] = row[4]
        temp_dic['foreigner'] = row[5]
        # temp_dic1 = {i: temp_dic}
        # temp_list.append(temp_dic1)
        temp_list.append(temp_dic)
    
    # 접속 종료
    conn.close()
    return temp_list

# 최근 5년치 각 월별로 인기있는 관광지 가져오는 함수
def get_popular_list_month(month):
    # 커서 생성
    conn = get_connection()
    cursor = conn.cursor()

    sql = '''select name, sum(korean) as korean, sum(foreigner) as foreigner from seoultbl where month = %s group by name
            union select name, sum(korean) as korean, sum(foreigner) as foreigner from busantbl where month = %s group by name
            union select name, sum(korean) as korean, sum(foreigner) as foreigner from chungbuktbl where month = %s group by name
            union select name, sum(korean) as korean, sum(foreigner) as foreigner from chungnamtbl where month = %s group by name
            union select name, sum(korean) as korean, sum(foreigner) as foreigner from daegutbl where month = %s group by name
            union select name, sum(korean) as korean, sum(foreigner) as foreigner from daejeontbl where month = %s group by name
            union select name, sum(korean) as korean, sum(foreigner) as foreigner from gangwontbl where month = %s group by name
            union select name, sum(korean) as korean, sum(foreigner) as foreigner from gwangjutbl where month = %s group by name
            union select name, sum(korean) as korean, sum(foreigner) as foreigner from gyeongbuktbl where month = %s group by name
            union select name, sum(korean) as korean, sum(foreigner) as foreigner from gyeongnamtbl where month = %s group by name
            union select name, sum(korean) as korean, sum(foreigner) as foreigner from gyeonggitbl where month = %s group by name
            union select name, sum(korean) as korean, sum(foreigner) as foreigner from incheontbl where month = %s group by name
            union select name, sum(korean) as korean, sum(foreigner) as foreigner from jejutbl where month = %s group by name
            union select name, sum(korean) as korean, sum(foreigner) as foreigner from jeonbuktbl where month = %s group by name
            union select name, sum(korean) as korean, sum(foreigner) as foreigner from jeonnamtbl where month = %s group by name
            union select name, sum(korean) as korean, sum(foreigner) as foreigner from sejongtbl where month = %s group by name
            union select name, sum(korean) as korean, sum(foreigner) as foreigner from ulsantbl where month = %s group by name
            order by korean+foreigner desc limit 5;'''
    cursor.execute(sql, (month,month,month,month,month,month,month,month,month,month,month,month,month,month,month,month,month))
    result = cursor.fetchall()

    temp_list = []
    for row in result:
        temp_dic = {}
        temp_dic['name'] = row[0]
        temp_dic['korean'] = int(row[1])
        temp_dic['foreigner'] = int(row[2])
        temp_list.append(temp_dic)
        
    # 접속 종료
    conn.close()
    return temp_list
  
# 각 지역별로 인기있는 관광지 가져오는 함수
def get_popular_list_nation(name):
    # 커서 생성
    conn = get_connection()
    cursor = conn.cursor()

    # city name return
    cityname = city[name]
    name = name + 'tbl'
    sql = 'select name, sum(korean) as korean, sum(foreigner) as foreigner, sum(korean)+sum(foreigner) as total from '+ name + ' group by name order by total desc limit 5;'
    cursor.execute(sql)
    result = cursor.fetchall()

    temp_list = []
    for row in result:
        temp_dic = {}
        temp_dic['name'] = row[0]
        temp_dic['korean'] = int(row[1])
        temp_dic['foreigner'] = int(row[2])
        temp_list.append(temp_dic)

    # 접속 종료
    conn.close()
    return temp_list, cityname

# 최근 5년치 각 지역별+월별로 인기있는 관광지 가져오는 함수
def get_popular_list_month_loc(month, loc):
    # 커서 생성
    conn = get_connection()
    cursor = conn.cursor()

    sql = 'with abc(gungu, name, korean, foreigner) as (select GUNGU, name, sum(korean) as korean, sum(foreigner) as foreigner from ' + locDict[loc]+' where month = %s group by name) select gungu, name, korean, foreigner, korean+foreigner as total from abc order by total desc limit 5'

    cursor.execute(sql, month)
    result = cursor.fetchall()

    temp_list = []
    for row in result:
        temp_dic = {}
        temp_dic['gungu'] = row[0]
        temp_dic['name'] = row[1]
        temp_dic['korean'] = int(row[2])
        temp_dic['foreigner'] = int(row[3])
        temp_dic['total'] = int(row[4])
        # temp_dic1 = {i: temp_dic}
        # temp_list.append(temp_dic1)
        temp_list.append(temp_dic)
    
    # 접속 종료
    conn.close()
    
    return temp_list, city[loc]

# 최근 5년치 각 연도별로 인기있는 관광지 가져오는 함수 -> 어떤 데이터를 가져올지?
def get_popular_list_year(year):
    # 커서 생성
    conn = get_connection()
    cursor = conn.cursor()

    sql = '''with abc(gungu, name, korean, foreigner)
        as (select GUNGU, name, sum(korean) as korean, sum(foreigner) as foreigner from seoultbl where year = %s group by name)
        select gungu, name, korean, foreigner, korean+foreigner as total from abc order by total desc limit 5; '''
    cursor.execute(sql, year)
    result = cursor.fetchall()

    temp_list = []
    for row in result:
        temp_dic = {}
        temp_dic['gungu'] = row[0]
        temp_dic['name'] = row[1]
        temp_dic['korean'] = int(row[2])
        temp_dic['foreigner'] = int(row[3])
        temp_dic['total'] = int(row[4])
        # temp_dic1 = {i: temp_dic}
        # temp_list.append(temp_dic1)
        temp_list.append(temp_dic)
    
    # 접속 종료
    conn.close()
    return temp_list

#######################################해외###########################################

# 최근 5년치 각 지역별+월별로 인기있는 관광지 가져오는 함수
def get_popular_list_month_loc_fo(month):
    # 커서 생성
    conn = get_connection_fo()
    cursor = conn.cursor()

    sql = '''
        select country, sum(nTourist) as total from asiatbl where month = %s group by country
        union select country, sum(nTourist) as total from africatbl where month = %s group by country
        union select country, sum(nTourist) as total from americatbl where month = %s group by country
        union select country, sum(nTourist) as total from europetbl where month = %s group by country
        union select country, sum(nTourist) as total from oceaniatbl where month = %s group by country
        order by total desc limit 5;
    '''
    cursor.execute(sql, (month, month, month, month, month))
    result = cursor.fetchall()

    temp_list = []
    for row in result:
        temp_dic = {}
        temp_dic['country'] = row[0]
        temp_dic['total'] = int(row[1])
        temp_list.append(temp_dic)
    
    # 접속 종료
    conn.close()
    
    return temp_list

def get_course(country):
    conn = get_connection_fo()
    cursor = conn.cursor()
    sql = 'use asiadb'
    cursor.execute(sql)

    sql = 'select * from ' + country
    cursor.execute(sql)
    result = cursor.fetchall()

    temp_list = []
    for row in result:
        temp_dic = {}
        temp_dic['nation'] = row[2]
        temp_dic['city'] = row[3]
        temp_dic['name'] = row[4]
        temp_dic['score'] = row[5]
        temp_dic['description'] = row[6]
        temp_list.append(temp_dic)
    
    # 접속 종료
    conn.close()
    
    return temp_list

def get_city_list(country):
    conn = get_connection_fo()
    cursor = conn.cursor()
    sql = 'use asiadb'
    cursor.execute(sql)

    sql = 'select distinct city from ' + country
    cursor.execute(sql)
    result = cursor.fetchall()

    temp_list = []
    for row in result:
        temp_list.append(row[0])
    
    # 접속 종료
    conn.close()
    
    return temp_list

# 코스추천에서 넘어온 값으로 나라 선택해서 뿌리기
def get_course_select(continent, country):
    conn = get_connection_fo()
    cursor = conn.cursor()
    sql = 'use ' + continent
    cursor.execute(sql)

    sql = 'select * from ' + country
    cursor.execute(sql)
    result = cursor.fetchall()

    temp_list = []
    for row in result:
        temp_dic = {}
        temp_dic['nation'] = row[2]
        temp_dic['city'] = row[3]
        temp_dic['name'] = row[4]
        temp_dic['score'] = row[5]
        temp_dic['description'] = row[6]
        temp_list.append(temp_dic)
    
    # 접속 종료
    conn.close()
    
    return temp_list

def get_city_list_select(continent, country):
    conn = get_connection_fo()
    cursor = conn.cursor()
    sql = 'use ' + continent
    cursor.execute(sql)

    sql = 'select distinct city from ' + country
    cursor.execute(sql)
    result = cursor.fetchall()

    temp_list = []
    for row in result:
        temp_list.append(row[0])
    
    # 접속 종료
    conn.close()
    
    return temp_list

def get_connection_ch(choose) : # 원하는 db 접속
    conn = pymysql.connect(host='70.12.227.62', user='user2',
            password='multicampus1111', db=choose
            , charset='utf8')
    if conn:
        print('f 디비 접속 완료')
    return conn

def get_course_internal_list_data():    # 사진띄우기 간단하게 10개만
    # 커서 생성
    conn = get_connection_ch('korea_coursesdb')
    cursor = conn.cursor()

    sql = '''
        select name, score, description from busan_tbl limit 10;
    '''
    cursor.execute(sql)
    result = cursor.fetchall()

    temp_list = []
    for row in result:
        temp_dic = {}
        temp_dic['name'] = row[0]
        temp_dic['score'] = row[1]
        temp_dic['description'] = row[2]
        temp_list.append(temp_dic)
    
    # 접속 종료
    conn.close()
    
    return temp_list

if __name__ == "__main__":
    # # temp_list = get_tourpoint_list()
    # temp_list = get_popular_list()
    # print(temp_list)

    # # st_json = json.dumps(temp_list[0], indent=4)
    # # print(st_json)

    # temp_list = get_popular_list_year(2020)
    # print(temp_list)

    # temp_list = get_popular_list_month_loc(1, 1)
    # print(temp_list)

    # today = datetime.date.today()
    # print(today.year-1, today.month)

    # temp_list = get_popular_list_month_loc_fo(2)
    # print(temp_list)
    # temp_list = get_popular_list_month(1)
    # print(temp_list)

    # temp_list = get_course(1)
    # print(temp_list)
    print(get_city_list('japan_tbl'))







    # print(country(10))
    # print(search_country_list('kor'))
    # # country_add('FIN', 'Finland', 121914.00, 1376)
    # # country_delete(35)
    # country_update(37, 90000, 90000)


# # no으로 나라별 레코드 변환함수
# def country(no):
#     # 커서 생성
#     conn = get_connection()
#     cursor = conn.cursor()

#     # sql문 생성
#     sql = '''SELECT * FROM worldCity where No = %s '''
#     cursor.execute(sql, no)
#     result = cursor.fetchone()

#     # 딕셔너리 구조로 변환
#     temp_dic = {}
#     temp_dic['No'] = result[0]
#     temp_dic['Code'] = result[1]
#     temp_dic['Name'] = result[2]
#     temp_dic['GNP'] = result[3]
#     temp_dic['Population'] = result[4]

#     conn.close()
#     return temp_dic

# # 특정 단어가 들어가는 레코드 검색
# # select * from worldcity where name like "%단어%";
# def search_country_list(country_name):
#     # 커서 생성
#     conn = get_connection()
#     cursor = conn.cursor()

#     # sql문 생성
#     sql = '''select * from worldcity where name like %s  '''
#     country_name = '%'+country_name+'%' # 앞뒤로 %붙여주기
#     cursor.execute(sql, country_name)
#     result = cursor.fetchall()

#     temp_list = []
#     for row in result:
#         temp_dic = {}
#         temp_dic['No'] = row[0]
#         temp_dic['Code'] = row[1]
#         temp_dic['Name'] = row[2]
#         temp_dic['GNP'] = row[3]
#         temp_dic['Population'] = row[4]
#         temp_list.append(temp_dic)
    
#     # 접속 종료
#     conn.close()
#     return temp_list

# def get_country_list2():
#     # 커서 생성
#     conn = get_connection()
#     cursor = conn.cursor()

#     # sql문 생성
#     # 반대로
#     sql = '''SELECT * FROM worldCity order by no desc  '''
#     cursor.execute(sql)
#     result = cursor.fetchall()

#     temp_list = []
#     for row in result:
#         temp_dic = {}
#         temp_dic['No'] = row[0]
#         temp_dic['Code'] = row[1]
#         temp_dic['Name'] = row[2]
#         temp_dic['GNP'] = row[3]
#         temp_dic['Population'] = row[4]
#         temp_list.append(temp_dic)
    
#     # 접속 종료
#     conn.close()
#     return temp_list

# # 레코드 추가 함수
# def country_add(c_code, c_name, c_gnp, c_population):
#     # 데이타베이스 접속함수 호출
#     conn = get_connection()

#     # 작업변수 생성
#     cursor = conn.cursor()

#     # 레코드 추가와 관련된 sql
#     # INSERT INTO 테이블명 (컬럼명1,...,컬럼명n) VALUES (값1, ... 값N);
#     # 레코드 삭제와 관련된 sql 
#     # DELETE from 테이블명 where 조건식;
#     sql = '''
#             insert into worldCity
#                 (code, name, gnp, population)
#                 values (%s, %s, %s, %s)
#             '''
              
#     cursor.execute(sql, (c_code, c_name, c_gnp, c_population))
#     #DB에 반영(write)
#     conn.commit()
#     conn.close()

# # no으로 레코드 삭제
# def country_delete(country_no):

#     # 데이타베이스 접속함수 호출
#     conn = get_connection()
#     cursor = conn.cursor()

#     # 레코드 삭제와 관련된 sql 
#     # DELETE from 테이블명 where 조건식;
#     sql = '''
#             delete from worldCity
#                 where No = %s
#             '''
              
#     cursor.execute(sql, (country_no))
#     conn.commit()
#     conn.close()

# # 레코드 수정 함수
# # gnp, population 컬럼만 수정 
# # update 테이블명 set 컬럼명=값 where 조건식
# def country_update(c_no, c_gnp, c_population):
#     # 데이타베이스 접속함수 호출
#     conn = get_connection()
#     # 작업변수 생성
#     cursor = conn.cursor()

#     # 레코드 수정 sql 구문 
#     sql = '''
#             update worldcity
#                 set 
#                     GNP=%s, Population=%s
#                 where No=%s
#             '''

#     cursor.execute(sql, (c_gnp, c_population, c_no))
#     conn.commit()
#     conn.close()
