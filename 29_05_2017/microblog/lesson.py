from flask import Flask, render_template, request, redirect

app = Flask(__name__)  ## __name__ что бы привязать фласк с текущей директории


@app.route('/')
#@app.route('/<name>')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        print(request.form['post'], request.form['name'])

        post =  request.form.get('post', '')
        name = request.form.get('name', '')
        if post and name:
            return redirect('/')
    return render_template('add.html', name=name, post=post)

if __name__ == '__main__':
    app.run(debug=True)

