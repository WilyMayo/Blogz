from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:1234@localhost:3306/Blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'qwerfs1357XvBk'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(200))
    owner_id = db.Column(db.String(200), db.ForeignKey('user.username'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def request_login():
    allowed_routes = ['login','blog','index', 'signup'] 
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user'] = username
            flash("Logged in")
            return redirect('/blog')
        else:
            flash('User password incorrect, or user does not exist')     

    return render_template('login.html')



@app.route('/signup', methods=['POST','GET'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
               #validate user

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = username
            return  redirect('/newpost')
        else:
            #user already have 
            return '<h1> Duplicate user</h1>'

           #validate user 

    return render_template('signup.html')
   









@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_id = request.args.get('id')
    user_id = request.args.get('user')
    if blog_id is not None:
        blogs = Blog.query.filter_by(id=blog_id)   
        return render_template('show.html', blogs=blogs)
    elif user_id is not None:
        blogs = Blog.query.filter_by(owner_id=user_id)
        return render_template('singleUser.html', blogs=blogs)    


    all_blogs = Blog.query.all()

   
    
    return render_template('blog.html',title="Build A Blog",blogs=all_blogs)

@app.route('/newpost', methods=['POST','GET'] )
def display_newpost():
    owner = User.query.filter_by(username=session['user']).first()
    if request.method == 'POST':
       blog_title = request.form['title']
       blog_body = request.form['body']
       new_post = Blog(blog_title, blog_body, owner)
       db.session.add(new_post)
       db.session.commit()
       return redirect('/blog?id={0}&user={1}'.format(new_post.id, owner.username))


    return render_template('newpost.html')

    
    
@app.route('/')
def index():
    all_users = User.query.all()
    return render_template('index.html', all_users=all_users)


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/blog')

if __name__ == '__main__':
    app.run()