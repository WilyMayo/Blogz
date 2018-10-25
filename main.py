from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:1234@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'qwerfs1357XvBk'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(200))

    def __init__(self, title, body):
        self.title = title
        self.body = body
   


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_id = request.args.get('id')
    if blog_id is not None:
        blogs = Blog.query.filter_by(id=blog_id)
        return render_template('show.html', blogs=blogs)


    all_blogs = Blog.query.all()

   
    
    return render_template('blog.html',title="Build A Blog",blogs=all_blogs)

@app.route('/newpost', methods=['POST','GET'] )
def display_newpost():
    if request.method == 'POST':
       blog_title = request.form['title']
       blog_body = request.form['body']
       new_post = Blog(blog_title, blog_body)
       db.session.add(new_post)
       db.session.commit()
       return redirect('/blog?id={0}'.format(new_post.id))


    return render_template('newpost.html')

    
    
    



@app.route('/old-post', methods=['POST'])
def old_post():

    title_id = int(request.form['title-id'])
    title = Title.query.get(title_id)
    title.body = True
    db.session.add(title)
    db.session.commit()

    return redirect('/blog')


if __name__ == '__main__':
    app.run()