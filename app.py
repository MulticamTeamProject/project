# flask 모듈 임포트
from flask import Flask, render_template, request

# flask 객체 생성
app = Flask(__name__)

# 라우터 등록
@app.route('/') # 메인 페이지 주소
def index():
    return render_template('home.html')

@app.route('/advise_nation') # 추천 여행지 주소
def advise_nation():
    return render_template('advise_main.html')

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


# 서버실행
app.run('127.0.0.1',5000,debug=True)
