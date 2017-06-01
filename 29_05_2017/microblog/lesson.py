from flask import Flask, render_template, request, redirect, session, g
import sqlite3

app = Flask(__name__)  ## __name__ что бы привязать фласк с текущей директории
app.secret_key = 'asdadasda'


@app.before_request
def before_request():
    g.db = sqlite3.connect('blog.db')

@app.after_request
def after_request(f):
    g.db.close()
    return f

@app.route('/')
#@app.route('/<name>')
def index():
    #db = sqlite3.connect('blog.db')
    cursor = g.db.execute('select * from postss order by id desc')
    postss = cursor.fetchall()
    #db.close()
    message = session.pop('message', '')
    return render_template('index.html', postss=postss, message=message)

@app.route('/add', methods=['GET', 'POST'])
def add():
    name = post = ''
    if request.method == 'POST':
        print(request.form['post'], request.form['name'])
        post =  request.form.get('post', '')
        name = request.form.get('name', '')
        if post and name:
            #db = sqlite3.connect('blog.db')
            g.db.execute('INSERT INTO postss (name, post) VALUES (?,?)', (name,post))
            g.db.commit()
            #db.close()
            session['message'] = 'Post has been added successfully'
            return redirect('/')
    return render_template('add.html', name=name, post=post)

if __name__ == '__main__':
    app.run(debug=True)

