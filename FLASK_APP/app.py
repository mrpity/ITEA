from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'mr.pity!'

@app.route('/user')
def user(): pass

@app.route('/user/<username>')
def show_user_profile(username):
    # show user profile
    # return 'User: %s' % username
     return render_template('visual.html', name=username)



if __name__ == '__main__':
    app.run(host='flask-app.dev.whirl.sg', port=5001)