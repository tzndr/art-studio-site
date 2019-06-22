from flask import Flask, render_template, redirect, url_for, request, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from models import Base, User, Category, Item, BlogPost
from flask import session as login_session
import httplib2
import requests

app = Flask(__name__)

engine = create_engine('sqlite:///amyzanderdb.db?check_same_thread=False')
Base.metadata.bind = create_engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

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
