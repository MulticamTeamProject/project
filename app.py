# flask 모듈 임포트
from flask import Flask, render_template, request
import db;

# flask 객체 생성
app = Flask(__name__)

# 라우터 등록
@app.route('/') # 메인 페이지 주소
def index():
    return render_template('home.html')

# 메인에서는 현재 월/년도 인기 관광지 표시
@app.route('/advise_nation') # 추천 여행지 주소
def advise_nation():
    popular_dict = db.get_popular_list_month(8)
    popular_dict_year = db.get_popular_list_year(2020)
    # popular_dict = db.get_popular_list()
    return render_template('advise_main.html', popular_dict=popular_dict, month=8, popular_dict_year=popular_dict_year, year=2020)

# 월(지역별)은 top5/내-외국인비율 표시
@app.route('/korea_month_<no1>+loc_<no2>')
def month_loc(no1, no2):
    popular_dict, city = db.get_popular_list_month_loc(no1, int(no2))
    return render_template('korea_month+loc.html', popular_dict=popular_dict, month=no1, city=city)

@app.route('/advise_course') # 추천 코스 주소
def advise_course():
    return render_template('course_main.html')

@app.route('/overseas') # 월별 추천
def month():
    return render_template('overseas.html')

@app.route('/month_1') # 1월테스트
def month_1():
    return render_template('month_1.html')

@app.route('/month_2') # 2월테스트
def month_2():
    return render_template('month_2.html')

@app.route('/test') # 테스트화면 임시
def test():
    return render_template('test.html')
    
@app.route('/advise_korea') # 국내여행지추천
def advise_korea():
    popular_dict = db.get_popular_list_month(8)
    popular_dict_year = db.get_popular_list_year(2020)
    # popular_dict = db.get_popular_list()
    return render_template('korea_advise.html', popular_dict=popular_dict, month=8, popular_dict_year=popular_dict_year, year=2020)


# 서버실행
app.run('127.0.0.1',5000,debug=True)
