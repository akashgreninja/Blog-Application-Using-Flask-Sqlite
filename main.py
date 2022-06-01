
from datetime import date
from flask import Flask, render_template, redirect, url_for,request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField




app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts_2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=True)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts= db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
   show_post_1=BlogPost.query.get(index)
   return render_template('post.html',post=show_post_1)

    
    

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/delete/<int:id>")
def delete_form(id):
    
    delete_form=BlogPost.query.get(id)
    db.session.delete(delete_form)
    db.session.commit()
    return redirect(url_for("get_all_posts"))





@app.route("/contact")
def contact():
    return render_template("contact.html")



@app.route("/new-post",methods=["POST","GET"])
def new_post():
    form=CreatePostForm()
    if form.validate_on_submit():
        create_post=BlogPost(

                title = form.title.data,
                subtitle =  form.subtitle.data,
                date = date.today().strftime("%B %d %Y"),
                body =form.body.data,
                author =form.author.data,
                img_url = form.img_url.data,


            )
        db.session.add(create_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))


    

    return render_template("make-post.html",form=form)


@app.route("/edit-post/<int:post_id>",methods=["GET", "POST"])
def edit_post(post_id):
   
    edit_post=BlogPost.query.get(post_id)
    form = CreatePostForm(
    title=edit_post.title,
    subtitle=edit_post.subtitle,
    img_url=edit_post.img_url,
    author=edit_post.author,
    body=edit_post.body
    )
    if form.validate_on_submit():
       
        
        edit_post.title=form.title.data
        edit_post.subtitle = form.subtitle.data
        edit_post.body =form.body.data
        edit_post.author =form.author.data
        edit_post.img_url = form.img_url.data
        db.session.commit()
        return redirect(url_for("show_post", index=edit_post.id))


    return render_template("make-post.html",form=form,editable=True)    





if __name__ == "__main__":
    app.run(debug=True)