from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.endorsement.views import endorsement_blueprint
from instagram_web.blueprints.follows.views import follows_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from flask_login import login_required,current_user
from instagram_web.util.google_oauth import oauth

assets = Environment(app)
assets.register(bundles)

oauth.init_app(app)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(endorsement_blueprint, url_prefix="/endorsement")
app.register_blueprint(follows_blueprint, url_prefix="/follows")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
@login_required
def home():
    from models.image import Image
    from models.user import User
    from models.fanidol import FanIdol
    from peewee import JOIN
    # show all this
    idols = User.select().join(FanIdol,on=(FanIdol.idol==User.id)).where(FanIdol.fan==current_user.id)
    idol_list = [x.id for x in idols]
    idol_list.append(current_user.id)
    images = Image.select().where((Image.user.in_(idol_list))).order_by(Image.created_at.desc())
    not_following = User.select().where(User.id.not_in(idol_list))
    return render_template('home.html',images=images,users=idols,not_following=not_following)

