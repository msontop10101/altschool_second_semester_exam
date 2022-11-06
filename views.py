# from flask import Blueprint, render_template, request, flash
# from flask_login import login_user, login_required, logout_user, current_user
# from models import Post

# page = Blueprint('views', __name__)

# @page.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         post = request.form.get('post')

#         if len(post) < 1:
#             flash('Note is too short!', category='error')
#         else:
#             new_post = Post(data=post, user_id=current_user.id)
#             db.session.add(new_post)
#             db.session.commit()
#             flash('Note added!', category='success')

#     return render_template("home.html", user=current_user)
# @page.route('/about')
# def about():
#     return render_template('about.html', user=current_user)
# @page.route('/contact')
# def contact():
#     return render_template('contact.html', user=current_user)