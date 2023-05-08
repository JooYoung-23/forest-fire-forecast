from flask import Flask, request, render_template
from static.py.risk_map import view_risk_map

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template("result.html")

@app.route('/method', methods=['GET', 'POST'])
def method():
    if request.method == 'GET':
        return "GET으로 전달"
    else:
        return "POST로 전달"

@app.route('/risk_map')
def risk_map():
    return (view_risk_map())

if __name__ == '__main__':
    app.run(debug=True)