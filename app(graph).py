# flask 모듈 임포트
from flask import Flask, render_template, request

import db
import json

# flask 객체 생성
app = Flask(__name__)

# 라우터 등록
@app.route('/') # 메인 페이지 주소
def index():
    return render_template('home.html')

@app.route('/advise_nation') # 추천 여행지 주소
def advise_nation():
    popular_dict = db.get_popular_list_month(12)
    popular_dict_year = db.get_popular_list_year(2020)
    # popular_dict = db.get_popular_list()
    return render_template('advise_main.html', popular_dict=popular_dict, month=12, popular_dict_year=popular_dict_year, year=2020)

@app.route('/advise_course') # 추천 코스 주소
def advise_course():
    return render_template('course_main.html')

# 서버실행
app.run('127.0.0.1',5000,debug=True)
