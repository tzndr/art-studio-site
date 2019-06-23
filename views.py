from flask import Flask, render_template, redirect, url_for, request, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from models import Base, User, Category, Item, BlogPost
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests
import json
from flask import make_response

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///amyzanderdb.db?check_same_thread=False')
Base.metadata.bind = create_engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 50)
        response.headers['Content-Type'] = 'application/json'
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given userID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_resonse(json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client id does not match app's")
        response.header['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        respnse = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'

    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/')
def showMain():
    return render_template('main.html')

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
    posts = session.query(BlogPost).order_by(BlogPost.id.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/blog/new', methods=['GET', 'POST'])
def newBlogPost():
    posts = session.query(BlogPost).all()
    if request.method == 'POST':
        newPost = BlogPost(
            title = request.form['title'],
            subtitle = request.form['subtitle'],
            author = request.form['author'],
            img = request.form['img'],
            date = request.form['date'],
            body_header_1 = request.form['body_header_1'],
            body_1 = request.form['body_1'],
            body_header_2 = request.form['body_header_2'],
            body_2 = request.form['body_2'],
            body_header_3 = request.form['body_header_3'],
            body_3 = request.form['body_3'],
            body_header_4 = request.form['body_header_4'],
            body_4 = request.form['body_4'],
            body_header_5 = request.form['body_header_5'],
            body_5 = request.form['body_5']
        )
        session.add(newPost)
        session.commit()
        flash("%s has been posted sucessfully!" % newPost.title)
        return redirect(url_for('showBlog'))
    else:
        return render_template('new_blog_post.html', posts = posts)

@app.route('/blog/<int:blogPost_id>/edit', methods=['GET', 'POST'])
def editBlogPost(blogPost_id):
    editedPost = session.query(BlogPost).filter_by(id=blogPost_id).one()
    if request.method == 'POST':
        if request.form['title']:
            editedPost.title = request.form['title']
        if request.form['subtitle']:
            editedPost.subtitle = request.form['subtitle']
        if request.form['author']:
            editedPost.author = request.form['author']
        if request.form['img']:
            editedPost.img = request.form['img']
        if request.form ['date']:
            editedPost.date = request.form['date']
        if request.form['body_header_1']:
            editedPost.body_header_1 = request.form['body_header_1']
        if request.form['body_1']:
            editedPost.body_1 = request.form['body_1']
        if request.form['body_header_2']:
            editedPost.body_header_2 = request.form['body_header_2']
        if request.form['body_2']:
            editedPost.body_2 = request.form['body_2']
        if request.form['body_header_3']:
            editedPost.body_header_3 = request.form['body_header_3']
        if request.form['body_3']:
            editedPost.body_3 = request.form['body_3']
        if request.form['body_header_4']:
            editedPost.body_header_4 = request.form['body_header_4']
        if request.form['body_4']:
            editedPost.body_4 = request.form['body_4']
        if request.form['body_header_5']:
            editedPost.body_header_5 = request.form['body_header_5']
        if request.form['body_5']:
                    editedPost.body_5 = request.form['body_5']
        session.add(editedPost)
        session.commit()
        flash("%s has been updated" % editedPost.title)
        return redirect(url_for('showBlog'))
    else:
        return render_template('edit_blog_post.html', editedPost=editedPost, blogPost_id=blogPost_id)

@app.route('/blog/<int:blogPost_id>/delete/', methods=['GET', 'POST'])
def deleteBlogPost(blogPost_id):
    deletedPost = session.query(BlogPost).filter_by(id=blogPost_id).one()
    if request.method == 'POST':
        session.delete(deletedPost)
        session.commit()
        flash("%s has been sucessfully deleted" % deletedPost.title)
        return redirect(url_for('showBlog'))
    else:
        return render_template('delete_blog_post.html', deletedPost=deletedPost, blogPost_id=blogPost_id)

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
