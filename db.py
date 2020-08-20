#db 접속
import pymysql
import json

# 1) pyMySQL 모듈 임포트 
# 2) DB 연결
# 3) 커서 생성 
# 4) 테이블 => 리스트로 저장 
# 5) 테이블 => 딕셔너리 리스트로 저장

# app에서 import 위해 함수로 빼기
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
    conn = pymysql.connect(host='127.0.0.1', user='multi',
            password='multi', db='tourpointdb'
            , charset='utf8')
    if conn:
        print('f 디비 접속 완료')
    return conn

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

def get_popular_list_month(month):
    # 커서 생성
    conn = get_connection()
    cursor = conn.cursor()

    sql = '''with abc(gungu, name, korean, foreigner)
        as (select GUNGU, name, sum(korean) as korean, sum(foreigner) as foreigner from seoultbl where month = %s group by name)
        select gungu, name, korean, foreigner, korean+foreigner as total from abc order by total desc limit 5; '''
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
    return temp_list

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

if __name__ == "__main__":
    # temp_list = get_tourpoint_list()
    temp_list = get_popular_list()
    print(temp_list)

    # st_json = json.dumps(temp_list[0], indent=4)
    # print(st_json)

    temp_list = get_popular_list_year(2020)
    print(temp_list)






    # print(country(10))
    # print(search_country_list('kor'))
    # # country_add('FIN', 'Finland', 121914.00, 1376)
    # # country_delete(35)
    # country_update(37, 90000, 90000)