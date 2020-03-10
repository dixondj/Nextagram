from flask import Blueprint, render_template,request,redirect,url_for,flash
from models.user import User
from models.fanidol import FanIdol
from flask_login import current_user, login_required
import os


follows_blueprint = Blueprint('follows',
                            __name__,
                            template_folder='templates')

@follows_blueprint.route('/<idol_id>')
@login_required
def create(idol_id):
    idol = User.get_by_id(idol_id)
    if current_user.follow(idol):
        flash(f"You send follow request to {idol.username}","success")
        return redirect(url_for('users.show',username=current_user.username))
    else:
        flash(f"You not yet follow {idol.username}","danger")
        return render_template('users/show.html',username=idol.username)

@follows_blueprint.route('/<fan_id>/delete')
@login_required
def destroy(fan_id):
    fan = User.get_by_id(fan_id)
    # for delete request from fan
    # 1 send follow request to 2, create a row in fanidol with approved == False
    # 2 is current user, want to delete request of 1
    if fan.unfollow(current_user):
        flash(f"You deleted request from {fan.username}","success")
        return redirect(url_for('users.show',username=current_user.username))
    else:
        flash("Something went wrong, try again later.","danger")
        return render_template('users/show.html',username=current_user.username) 

@follows_blueprint.route('/<idol_id>unfollow')
@login_required
def unfollow(idol_id):
    idol = User.get_by_id(idol_id)
    # for unfollow idol
    # 2 already follow 1, doesn't matter approve status
    # 2 is current user, want unfollow 1
    if current_user.unfollow (idol):
        flash(f"You unfollow {idol.username}","success")
        return redirect(url_for('users.show',username=idol.username))
    else:
        flash("Something went wrong, try again later.","danger")
        return render_template('users/show.html',username=idol.username)

@follows_blueprint.route('/<fan_id>/update')
@login_required
def update(fan_id):
    fan = User.get_by_id(fan_id)
    if current_user.approve_request(fan):
        flash(f"You approved follow request from {fan.username}","sucess")
        return redirect(url_for('users.show',username=current_user.username))
    else:
        flash("Something went wrong, try again later.","danger")
        return render_template('users/show.html',username=current_user.username)
