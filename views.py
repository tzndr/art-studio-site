from flask import Flask, render_template, redirect, url_for, request, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from models import Base, User, Category, Item, BlogPost, ArtNight
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests
import json
from flask import make_response
import logging

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///amyzanderdb.db?check_same_thread=False')
Base.metadata.bind = create_engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=' + access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.' + access_token),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['email'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1 style = "text-align: center; font: bold 22pt helvetica, arial;">Welcome, '
    output += login_session['email']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' "style = "text-align: center; width: 300px; height: 300px; border-radius: 150px; -webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['email'])
    print("done!")
    return output

    # DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/logout')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s' % access_token)
    print('username is: %s' % login_session['email'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=' + login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Disconnected.'), 200)
        redirect('/')
        flash("You have successfully logged out")
        return redirect('/')
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.' + "------" + access_token + "------"),400)
        response.headers['Content-Type'] = 'application/json'
        return response

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

@app.route('/artnight/greenbay')
def showArtNightGreenBay():
    art_nights = session.query(ArtNight).all()
    city = "Green Bay"
    if 'email' not in login_session or login_session['email'] != 'tzcode35@gmail.com':
        return render_template('art_night_greenbay_public.html', art_nights = art_nights, city = city)
    else:
        return render_template('art_night_greenbay.html', art_nights = art_nights, city = city)

@app.route('/artnight/tworivers')
def showArtNightTwoRivers():
    art_nights = session.query(ArtNight).all()
    if 'email' not in login_session or login_session['email'] != 'tzcode35@gmail.com':
        return render_template('art_night_tworivers_public.html', art_nights = art_nights)
    else:
        return render_template('art_night_tworivers.html', art_nights = art_nights)

@app.route('/artnight/newgb')
def showNewArtNightGreenBay():
    nights = session.query(ArtNight).all()
    if 'email' not in login_session or login_session['email'] != 'tzcode35@gmail.com':
        flash("You are not authorized to view the requested page")
        return render_template('index.html')
    else:
        if request.method == 'POST':
            newArtNight = ArtNight(
                city = request.form['city'],
                title = request.form['title'],
                description = request.form['description'],
                project_img = request.form['project_img'],
                date = request.form['date'],
                time = request.form['time'],
                cost = request.form['cost'],
                location = request.form['location'],
                address = request.form['address'],
                upcoming_date_1 = request.form['upcoming_date_1'],
                upcoming_date_2 = request.form['upcoming_date_2'],
                upcoming_date_3 = request.form['upcoming_date_3']
            )
            session.add(newArtNight)
            session.commit()
            flash("%s has been posted sucessfully!" % newArtNight.title)
            return redirect(url_for('showArtNightGreenBay'))
        else:
            return render_template('new_art_night_gb.html', nights = nights)

@app.route('/artnight/newtr')
def showNewArtNightTwoRivers():
    nights = session.query(ArtNight).all()
    if 'email' not in login_session or login_session['email'] != 'tzcode35@gmail.com':
        flash("You are not authorized to view the requested page")
        return render_template('index.html')
    else:
        if request.method == 'POST':
            newArtNight = ArtNight(
                city = request.form['city'],
                title = request.form['title'],
                description = request.form['description'],
                project_img = request.form['project_img'],
                date = request.form['date'],
                time = request.form['time'],
                cost = request.form['cost'],
                location = request.form['location'],
                address = request.form['address'],
                upcoming_date_1 = request.form['upcoming_date_1'],
                upcoming_date_2 = request.form['upcoming_date_2'],
                upcoming_date_3 = request.form['upcoming_date_3']
            )
            session.add(newArtNight)
            session.commit()
            flash("%s has been posted sucessfully!" % newArtNight.title)
            return redirect(url_for('showArtNightTwoRivers'))
        else:
            return render_template('new_art_night_tr.html', nights = nights)

@app.route('/catalog')
def showCatalog():
    return render_template('catalog.html')

@app.route('/privateevents')
def showPrivateEvents():
    return render_template('private_events.html')

@app.route('/blog')
def showBlog():
    recent_posts = session.query(BlogPost).order_by(BlogPost.id.desc()).limit(6).all()
    all_posts = session.query(BlogPost).all()
    all_cats = session.query(BlogPost.category).all()
    all_cats_list = [value for value, in all_cats]
    unique_cats = list(set(all_cats_list))
    if 'email' not in login_session or login_session['email'] != 'tzcode35@gmail.com':
        return render_template('public_blog.html', recent_posts=recent_posts, all_posts=all_posts,
            cats=unique_cats)
    else:
        return render_template('blog.html', recent_posts=recent_posts, all_posts=all_posts,
            cats=unique_cats)

@app.route('/blog/<string:blogPost_cat>/view', methods=['GET'])
def showBlogCat(blogPost_cat):
    selected_cat = session.query(BlogPost).filter_by(category=blogPost_cat).all()
    returned_cat = blogPost_cat
    return render_template('view_cats.html', selected_cat=selected_cat, returned_cat=returned_cat)

@app.route('/blog/<int:blogPost_id>/read', methods=['GET'])
def readBlogPost(blogPost_id):
    selected_post = session.query(BlogPost).filter_by(id = blogPost_id).one()
    if 'email' not in login_session or login_session['email'] != 'tzcode35@gmail.com':
        return render_template('read_blog_post_public.html', selected_post = selected_post)
    else:
        return render_template('read_blog_post.html', selected_post = selected_post)

@app.route('/blog/new', methods=['GET', 'POST'])
def newBlogPost():
    posts = session.query(BlogPost).all()
    if 'email' not in login_session or login_session['email'] != 'tzcode35@gmail.com':
        flash("You are not authorized to view the requested page")
        return render_template('index.html')
    else:
        if request.method == 'POST':
            newPost = BlogPost(
                title = request.form['title'],
                subtitle = request.form['subtitle'],
                authorName = request.form['authorName'],
                authorImg = request.form['authorImg'],
                authorDescription = request.form['authorDescription'],
                mainImg = request.form['mainImg'],
                date = request.form['date'],
                category = request.form['category'],
                body_header_1 = request.form['body_header_1'],
                body_1 = request.form['body_1'],
                img_2 = request.form['img_2'],
                body_header_2 = request.form['body_header_2'],
                body_2 = request.form['body_2'],
                img_3 = request.form['img_3'],
                body_header_3 = request.form['body_header_3'],
                body_3 = request.form['body_3'],
                img_4 = request.form['img_4'],
                body_header_4 = request.form['body_header_4'],
                body_4 = request.form['body_4'],
                img_5 = request.form['img_5'],
                body_header_5 = request.form['body_header_5'],
                body_5 = request.form['body_5'],
                img_6 = request.form['img_6'],
                body_header_6 = request.form['body_header_6'],
                body_6 = request.form['body_6'],
                img_7 = request.form['img_7'],
                body_header_7 = request.form['body_header_7'],
                body_7 = request.form['body_7'],
                img_8 = request.form['img_8'],
                body_header_8 = request.form['body_header_8'],
                body_8 = request.form['body_8'],
                img_9 = request.form['img_9'],
                body_header_9 = request.form['body_header_9'],
                body_9 = request.form['body_9'],
                img_10 = request.form['img_10'],
                body_header_10 = request.form['body_header_10'],
                body_10 = request.form['body_10']
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
        if request.form['authorName']:
            editedPost.authorName = request.form['authorName']
        if request.form['authorImg']:
            editedPost.authorImg = request.form['authorImg']
        if request.form['authorDescription']:
            editedPost.authorDescription = request.form['authorDescription']
        if request.form['mainImg']:
            editedPost.mainImg = request.form['mainImg']
        if request.form ['date']:
            editedPost.date = request.form['date']
        if request.form['category']:
            editedPost.category = request.form['category']
        if request.form['body_header_1']:
            editedPost.body_header_1 = request.form['body_header_1']
        if request.form['body_1']:
            editedPost.body_1 = request.form['body_1']
        if request.form['img_2']:
            editedPost.img_2 = request.form['img_2']
        if request.form['body_header_2']:
            editedPost.body_header_2 = request.form['body_header_2']
        if request.form['body_2']:
            editedPost.body_2 = request.form['body_2']
        if request.form['img_3']:
            editedPost.img_3 = request.form['img_3']
        if request.form['body_header_3']:
            editedPost.body_header_3 = request.form['body_header_3']
        if request.form['body_3']:
            editedPost.body_3 = request.form['body_3']
        if request.form['img_4']:
            editedPost.img_4 = request.form['img_4']
        if request.form['body_header_4']:
            editedPost.body_header_4 = request.form['body_header_4']
        if request.form['body_4']:
            editedPost.body_4 = request.form['body_4']
        if request.form['img_5']:
            editedPost.img_5 = request.form['img_5']
        if request.form['body_header_5']:
            editedPost.body_header_5 = request.form['body_header_5']
        if request.form['body_5']:
            editedPost.body_5 = request.form['body_5']
        if request.form['img_6']:
            editedPost.img_6 = request.form['img_6']
        if request.form['body_header_6']:
            editedPost.body_header_6 = request.form['body_header_6']
        if request.form['body_6']:
            editedPost.body_6 = request.form['body_6']
        if request.form['img_7']:
            editedPost.img_7 = request.form['img_7']
        if request.form['body_header_7']:
            editedPost.body_header_7 = request.form['body_header_7']
        if request.form['body_7']:
            editedPost.body_7 = request.form['body_7']
        if request.form['img_8']:
            editedPost.img_8 = request.form['img_8']
        if request.form['body_header_8']:
            editedPost.body_header_8 = request.form['body_header_8']
        if request.form['body_8']:
            editedPost.body_8 = request.form['body_8']
        if request.form['img_9']:
            editedPost.img_9 = request.form['img_9']
        if request.form['body_header_9']:
            editedPost.body_header_9 = request.form['body_header_9']
        if request.form['body_9']:
            editedPost.body_9 = request.form['body_9']
        if request.form['img_10']:
            editedPost.img_10 = request.form['img_10']
        if request.form['body_header_10']:
            editedPost.body_header_10 = request.form['body_header_10']
        if request.form['body_10']:
            editedPost.body_10 = request.form['body_10']
        session.add(editedPost)
        session.commit()
        flash("%s has been updated" % editedPost.title)
        return redirect(url_for('readBlogPost', blogPost_id=blogPost_id))
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

if __name__ == '__main__':
    app.secret_key = 'azanderstudios'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
