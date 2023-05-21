from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/result', methods=['GET', 'POST'])
def result():
    date = request.form.get('demo-name')
    print("year : ", date[:4])
    print("month : ", date[5:7])
    print("day : ", date[8:10])

	return render_template("result.html")

@app.route('/method', methods=['GET', 'POST'])
def method():
    if request.method == 'GET':
        return "GET으로 전달"
    else:
        return "POST로 전달"

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)