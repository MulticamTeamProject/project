# flask 모듈 임포트
from flask import Flask, render_template, request
import db
import datetime

city_db = {'일본':'japan_tbl', '중국':'china_tbl'}

# flask 객체 생성
app = Flask(__name__)

# 라우터 등록
@app.route('/') # 메인 페이지 주소
def index():
    return render_template('home.html')

@app.route('/advise_course') # 추천 코스 주소
def advise_course():
    return render_template('course_main.html')

@app.route('/overseas') # 해외 월별 추천
def month():
    today = datetime.date.today()
    month = today.month
    popular_dict = db.get_popular_list_month_loc_fo(month)
    return render_template('overseas.html', popular_dict=popular_dict, month=month)

@app.route('/overseas_<no1>') # 해외 월별 추천
def overseas_month(no1):
    popular_dict = db.get_popular_list_month_loc_fo(no1)
    return render_template('overseas+month.html', popular_dict=popular_dict, month=no1)

# @app.route('/month_1') # 1월테스트
# def month_1():
#     return render_template('month_1.html')

# @app.route('/month_2') # 2월테스트
# def month_2():
#     return render_template('month_2.html')

@app.route('/test') # 테스트화면 임시
def test():
    return render_template('test.html')
    
@app.route('/advise_korea') # 국내여행지추천
def advise_korea():
    today = datetime.date.today()
    month = today.month
    year = today.year-1
    popular_dict = db.get_popular_list_month(month)
    popular_dict_year = db.get_popular_list_year(year)
    return render_template('korea_advise.html', popular_dict=popular_dict, month=month, popular_dict_year=popular_dict_year, year=year)

# 메인에서는 현재 월/년도 인기 관광지 표시
# @app.route('/advise_nation') # 추천 여행지 주소
# def advise_nation():
#     popular_dict = db.get_popular_list_month(8)
#     popular_dict_year = db.get_popular_list_year(2020)
#     # popular_dict = db.get_popular_list()
#     return render_template('advise_main.html', popular_dict=popular_dict, month=8, popular_dict_year=popular_dict_year, year=2020)

# 월(지역별)은 top5/내-외국인비율 표시
# @app.route('/korea_month_<no1>+loc_<no2>')
# def month_loc(no1, no2):
#     popular_dict, city = db.get_popular_list_month_loc(no1, int(no2))
#     return render_template('korea_month+loc.html', popular_dict=popular_dict, month=no1, city=city)

@app.route('/korea_month_<no1>')
def month_loc(no1):
    popular_dict = db.get_popular_list_month(no1)
    return render_template('korea_month+loc.html', popular_dict=popular_dict, month=no1)

@app.route('/korea_nation_<name>')
def nation_loc(name):
    popular_dict = db.get_popular_list_nation(name)
    return render_template('korea_nation.html', popular_dict=popular_dict, name=name)
# 서버실행
#app.run('127.0.0.1',5000,debug=True)


# 해외 top3 화면에서 해당하는 페이지 보이기
@app.route('/overseas_course<country>')
def overseas_course(country):
    course_dict = db.get_course(city_db[country])
    city_list = db.get_city_list(city_db[country])
    return render_template('country_course.html', course_dict = course_dict, totalCount = len(course_dict), city_list = city_list)

# 해외 코스 화면에서 나라선택
@app.route('/select_country_course')
def country_course():
    return render_template('select_country_course.html')

# 선택된 나라 뿌리기
@app.route('/select_country_course<continent>+<country>')
def select_country_course(continent, country):
    course_dict = db.get_course_select(continent, country)
    city_list = db.get_city_list_select(continent, country)
    path = []
    for x in course_dict:
        p = 'images/external_img/' + x['name'] + '.jpg'
        print(p)
        path.append(p)
    return render_template('country_course.html', course_dict = course_dict, totalCount = len(course_dict), city_list = city_list, path = path)

@app.route('/internal_course') # 국내 코스 리스트 10개만
def internal_course():
    data = db.get_course_internal_list_data()
    path = []
    for x in data:
        p = 'images/internal_img/' + x['name'] + '.jpg'
        print(p)
        path.append(p)
    return render_template('internal_course.html', data = data, path = path)

# 서버실행
app.run('127.0.0.1',5000,debug=True)
