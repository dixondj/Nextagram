from flask import Blueprint, render_template,request,flash,redirect,url_for
from models.user import User
from flask_login import current_user
from werkzeug.utils import secure_filename
from instagram_web.util.helpers import upload_file_to_s3,allowed_file
import datetime



users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/signup', methods=['POST'])
def create():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    u = User(username=username, email=email, password=password)

    if u.save():
        flash("Successfully Registered")
        return redirect(url_for('users.new'))
    else:
        for error in u.errors:
            flash(error)
        return render_template('users/new.html')
    

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get(User.username==username)
    return render_template('users/show.html',user=user)



@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<sid>/edit', methods=['GET'])
def edit(sid):
    return render_template('users/edit.html')


@users_blueprint.route('/<sid>/update', methods=['POST'])
def edit_user(sid):
    # new_username = User.update(username = request.form.get('username')).where(User.id == sid)
    # new_email = User.update(email = request.form.get('email')).where(User.id == sid)
    # new_password = User.update(password = request.form.get('password')).where(User.id == sid)
    # n_user = User(username= new_username, email=new_email, password= new_password)sho
    n_user = User.get_by_id(sid)

    n_user.username  = request.form.get('username')
    n_user.email  = request.form.get('email')
    n_user.password  = request.form.get('password')

    if n_user.save():
        flash("successfully saved")
        return redirect(url_for('sessions.new',id=sid))
    else:
        flash(n_user.errors)
        return render_template('sessions/new.html',id=sid)



@users_blueprint.route("/upload", methods=["POST"])
def upload():

    # check whether an input field with name 'user_file' exist
    if 'user_file' not in request.files:
        flash('No user_file key in request.files')
        return redirect(url_for('users.new'))

    # after confirm 'user_file' exist, get the file from input
    file = request.files['user_file']

    # check whether a file is selected
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('users.new'))

        # check whether the file extension is allowed (eg. png,jpeg,jpg,gif)
    if file and allowed_file(file.filename):
        file.filename = secure_filename(f"{str(datetime.datetime.now())}{file.filename}")
        output = upload_file_to_s3(file) 
        print(output)
        # if upload success,will return file name of uploaded file
        if output:
            User.update(profile_image=file.filename).where(User.id==current_user.id).execute()
            flash("Profile image successfully uploaded","success")
            return redirect(url_for('users.show',username=current_user.username))
        # upload failed, redirect to upload page
        else:
            flash(output,"danger")
            return redirect(url_for('users.edit',id=current_user.id))

    # if file extension not allowed
    else:
        flash("File type not accepted,please try again.")
        return redirect(url_for('users.edit',sid=current_user.id))


