from flask import Flask, request, render_template

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

    return render_template("result.html", year=year, month=month, day=day, time=time)

@app.route('/method', methods=['GET', 'POST'])
def method():
    if request.method == 'GET':
        return "GET으로 전달"
    else:
        return "POST로 전달"

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)