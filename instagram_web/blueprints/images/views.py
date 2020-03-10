from flask import Blueprint, render_template,request,redirect,url_for,flash
from models.user import User
from models.image import Image
from flask_login import current_user, login_required
from instagram_web.util.helpers import upload_file_to_s3,allowed_file
from werkzeug.utils import secure_filename
import datetime

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')


# @images_blueprint.route('/new', methods=['GET'])
# def new():
#     return render_template('images/new.html')


@images_blueprint.route('/', methods=['POST'])
def create():
    
    if 'image_file' not in request.files:
        flash('No image_file key in request.files')
        return render_template("home.html")

    file = request.files['image_file']

    if file.filename == '':
        flash('No selected file')
        return render_template("home.html")

    if file and allowed_file(file.filename):
        file.filename = secure_filename(f"{str(datetime.datetime.now())}{file.filename}")
        output = upload_file_to_s3(file) 
        if output:
            image = Image(user=current_user.id,image_path=file.filename,caption=request.form.get("caption"))
            image.save()
            flash("Image successfully uploaded","success")
            return redirect(url_for('users.show',username=current_user.username))
        else:
            flash(output,"danger")
            return render_template("home.html")

    else:
        flash("File type not accepted,please try again.")
        return render_template("home.html")
