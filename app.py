from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_login import LoginManager
import os


base_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'base2002'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


    


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    first_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    posts = db.relationship('Post')
    
    
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('home'))

    return render_template("sign-up.html", user=current_user)




@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        post_data = request.form['post']
        new_post = Post(data=post_data, user_id=current_user.id)
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect('/')
        except:
            return 'There was an issue'
    else:
        posts = Post.query.order_by(Post.date).all()
        users = User.query.order_by(User.id).all()
        return render_template('home.html', posts=posts, users=users, user=current_user)


@app.route('/delete/<int:id>')
def delete(id):
    post_to_delete = Post.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the post'
    
@app.route('/edit-post/<int:id>', methods=['GET','POST'])
def update(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        post.data = request.form['data']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'An error occured'
    else:
        return render_template('edit-post.html', user=current_user, post=post)

@app.route('/about')
def about():
    return render_template('about.html', user=current_user)
@app.route('/contact')
def contact():
    return render_template('contact.html', user=current_user)



if __name__ == "__main__":
    app.run(debug=True)
