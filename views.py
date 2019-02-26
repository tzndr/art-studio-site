from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def showMain():
    return render_template('main.html')

@app.route('/studio')
def showStudio():
    return render_template('studio.html')

@app.route('/aboutamy')
def showAboutAmy():
    return render_template('about_amy.html')

@app.route('/artnight')
def showArtNight():
    return render_template('art_night.html')

@app.route('/catalog')
def showCatalog():
    return render_template('catalog.html')

@app.route('/privateevents')
def showPrivateEvents():
    return render_template('private_events.html')

@app.route('/blog')
def showBlog():
    return render_template('blog.html')

@app.route('/reachamy')
def showReachAmy():
    return render_template('reach_amy.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.secret_key = 'UdacityProject'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
