#db 접속
import pymysql
import datetime

city_dict = {'seoul':'서울', 'gangwon':'강원', 'gyeonggi':'경기', 'gyeongnam':'경남', 'gyeongbuk':'경북',
                 'gwangju':'광주', 'daegu':'대구', 'daejeon':'대전', 'busan':'부산', 'sejong':'세종', 
                 'ulsan':'울산', 'incheon':'인천', 'jeonnam':'전남', 'jeonbuk':'전북', 'jeju':'제주', 'chungnam':'충남', 'chungbuk':'충북',
                 'chungcheong':'충청', 'gyeongsang':'경상', 'jeolla':'전라'}

# 데이터 베이스에 접속하는 함수
def get_connection() :
    conn = pymysql.connect(host='70.12.227.62', user='user2',
            password='multicampus1111', db='koreatourpointdb'
            , charset='utf8')
    if conn:
        print('f 디비 접속 완료')
    return conn

#70.12.227.62
# 해외db접속
def get_connection_fo() :
    conn = pymysql.connect(host='70.12.227.62', user='user2',
            password='multicampus1111', db='countrydb'
            , charset='utf8')
    if conn:
        print('f 디비 접속 완료')
    return conn

# 국내db접속
def get_connection_in():
    conn = pymysql.connect(host='70.12.227.62', user='user2',
            password='multicampus1111', db='korea_coursesdb'
            , charset='utf8')
    if conn:
        print('f 디비 접속 완료')
    return conn

# 최근 5년치 각 월별로 인기있는 관광지 가져오는 함수
def get_popular_list_month(month):
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
    conn = get_connection()
    cursor = conn.cursor()

    # city name return
    cityname = city_dict[name]
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

    conn.close()
    return temp_list, cityname

# 최근 5년치 월별로 인기있는 관광지 가져오는 함수
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

# 코스추천에서 넘어온 값으로 나라 선택해서 뿌리기 + 도시 리스트
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

    sql = 'select distinct city from ' + country
    cursor.execute(sql)
    result = cursor.fetchall()

    city_list = []
    for row in result:
        city_list.append(row[0])
    
    # 접속 종료
    conn.close()
    
    return temp_list, city_list

# 국내 지역코스 받아서 데이터 뿌리기
def get_course_internal_list_data(location):    
    
    print(location)
    conn = get_connection_in()
    cursor = conn.cursor()

    sql = 'select name, score, description from %s limit 30;'%(location)
    cursor.execute(sql)
    result = cursor.fetchall()

    # 지역명 받아오기
    name = location.split('_')[0]
    title = city_dict[name]

    temp_list = []
    for row in result:
        temp_dic = {}
        temp_dic['name'] = row[0]
        temp_dic['score'] = row[1]
        temp_dic['description'] = row[2]
        temp_list.append(temp_dic)
    
    # 접속 종료
    conn.close()
    
    return temp_list, title

if __name__ == "__main__":
    print('db.py')


# # 최근 5년치 각 연도별로 인기있는 관광지 가져오는 함수 -> 어떤 데이터를 가져올지?
# def get_popular_list_year(year):
#     # 커서 생성
#     conn = get_connection()
#     cursor = conn.cursor()

#     sql = '''with abc(gungu, name, korean, foreigner)
#         as (select GUNGU, name, sum(korean) as korean, sum(foreigner) as foreigner from seoultbl where year = %s group by name)
#         select gungu, name, korean, foreigner, korean+foreigner as total from abc order by total desc limit 5; '''
#     cursor.execute(sql, year)
#     result = cursor.fetchall()

#     temp_list = []
#     for row in result:
#         temp_dic = {}
#         temp_dic['gungu'] = row[0]
#         temp_dic['name'] = row[1]
#         temp_dic['korean'] = int(row[2])
#         temp_dic['foreigner'] = int(row[3])
#         temp_dic['total'] = int(row[4])
#         # temp_dic1 = {i: temp_dic}
#         # temp_list.append(temp_dic1)
#         temp_list.append(temp_dic)
    
#     # 접속 종료
#     conn.close()
#     return temp_list
