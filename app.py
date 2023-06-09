from flask import Flask, request, render_template
from scheduling import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/result', methods=['GET', 'POST'])
def result():
    date = request.args.to_dict();
    year = date['year'];
    month = date['month'];
    day = date['day'];
    time = date['time'];
    print(year, month, day, time);
    date = str(year) + str(month).zfill(2) + str(day).zfill(2) + str(time).zfill(2) + "00";
    return render_template("result.html", year=year, month=month, day=day, time=time, date=date)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)