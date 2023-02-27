from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from brick_inventory.forms import BrickForm
from brick_inventory.models import Brick, db
from brick_inventory.helpers import random_joke_generator, get_set_info #can also use 'from ..helpers'

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    my_brick = BrickForm()
    try:
        if request.method == "POST" and my_brick.validate_on_submit():
            set_num = my_brick.set_num.data
            name = my_brick.name.data
            year = my_brick.year.data
            theme_id = my_brick.theme_id.data
            num_parts = my_brick.num_parts.data
            set_img_url = my_brick.set_img_url.data
            set_url = my_brick.set_url.data
            set_info = get_set_info(set_num)
            name = set_info.get('name', '')
            year = set_info.get('year', '')
            theme_id = set_info.get('theme_id', '')
            num_parts = set_info.get('num_parts', '')
            set_img_url = set_info.get('set_img_url', '')
            set_url = set_info.get('set_url', '')
            
            random_joke = random_joke_generator()
            user_token = current_user.token
           
            brick = Brick(set_num, name, year, theme_id, num_parts, set_img_url, set_url, random_joke, user_token)

            db.session.add(brick)
            db.session.commit()

            return redirect(url_for('site.profile'))

    except:
        raise Exception("Brick not created. Please check your form and try again.")

    user_token = current_user.token

    bricks = Brick.query.filter_by(user_token = user_token)


    return render_template('profile.html', form=my_brick, bricks = bricks)
    


