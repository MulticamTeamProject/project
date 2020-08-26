# flask 모듈 임포트
from flask import Flask, render_template, request
import db
import datetime

city_db = {'일본':'japan_tbl', '중국':'china_tbl', '베트남':'vietnam_tbl', '미국':'usa_tbl'}

# flask 객체 생성
app = Flask(__name__)

# 라우터 등록
@app.route('/') # 메인 페이지 주소
def index():
    return render_template('home.html')

#=========================국내 추천==========================#
@app.route('/advise_korea') # 국내 월별 인기 관광지/첫 화면에서는 현재 월 결과 보임
def advise_korea():
    today = datetime.date.today()
    month = today.month
    # year = today.year-1
    # popular_dict_year = db.get_popular_list_year(year)
    return render_template('korea_advise.html', month=month)

@app.route('/korea_month_<no1>') # 국내 선택한 월에 해당하는 인기 관광지
def month_loc(no1):
    popular_dict = db.get_popular_list_month(no1)
    return render_template('korea_month+loc.html', popular_dict=popular_dict, month=no1)

@app.route('/korea_nation_<name>') # 국내 선택한 지역에 해당하는 인기 관광지
def nation_loc(name):
    popular_dict, city = db.get_popular_list_nation(name)
    return render_template('korea_month+loc.html', popular_dict=popular_dict, name=city)


#=========================해외 추천==========================#
@app.route('/overseas') # 해외 월별 인기 관광지/첫 화면에서는 현재 월 결과 보임
def month():
    today = datetime.date.today()
    month = today.month
    return render_template('overseas.html', month=month)

@app.route('/overseas_<no1>') # 해외 선택한 월에 해당하는 인기 관광지
def overseas_month(no1):
    popular_dict = db.get_popular_list_month_loc_fo(no1)
    return render_template('overseas+month.html', popular_dict=popular_dict, month=no1)

@app.route('/overseas_course<country>') # 해외 결과 top3 클릭 -> 해당하는 페이지 보이기(새창)
def overseas_course(country):
    if(country == '미국'):
        course_dict, city_list = db.get_course_select('americadb', city_db[country])
    else:
        course_dict, city_list = db.get_course_select('asiadb', city_db[country])
    path = []
    for x in course_dict:
        p = 'images/external_img/' + x['name'] + '.jpg'
        print(p)
        path.append(p)
    return render_template('country_course.html', course_dict = course_dict, totalCount = len(course_dict), city_list = city_list, path = path)


#=========================국내 코스==========================#
@app.route('/select_internal_course') # 국내 코스 화면에서 지역선택
def internal_course():
    return render_template('select_internal_course.html')

@app.route('/select_internal_course<location>') # 선택된 지역 데이터 뿌리기
def select_internal_course(location):
    data, loc_name = db.get_course_internal_list_data(location)
    path = {}
    for x in data:
        path[x['name']] = 'images/internal_img/' + x['name'] + '.jpg'
    return render_template('internal_course.html', data = data, path = path, loc_name = loc_name)


#=========================해외 코스==========================#
@app.route('/select_country_course') # 해외 코스 화면에서 나라선택
def country_course():
    return render_template('select_country_course.html')

@app.route('/select_country_course<continent>+<country>') # 선택된 나라 데이터 뿌리기
def select_country_course(continent, country):
    course_dict, city_list = db.get_course_select(continent, country)
    path = []
    for x in course_dict:
        p = 'images/external_img/' + x['name'] + '.jpg'
        print(p)
        path.append(p)
    return render_template('country_course.html', course_dict = course_dict, totalCount = len(course_dict), city_list = city_list, path = path)

# 서버실행
app.run('127.0.0.1',5000,debug=True)
