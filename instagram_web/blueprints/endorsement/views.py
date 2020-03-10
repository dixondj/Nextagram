from flask import Blueprint, render_template,request,redirect,url_for,flash
from models.user import User
from models.image import Image
from models.endorsement import Endorsement
from flask_login import current_user, login_required
import os
import braintree
from instagram_web.util.mail_helpers import endorsement_email

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.environ.get("BT_MERCHANT_ID"),
        public_key=os.environ.get("BT_PUBLIC_KEY"),
        private_key=os.environ.get("BT_PRIVATE_KEY")
    )
)

endorsement_blueprint = Blueprint('endorsement',
                            __name__,
                            template_folder='templates')


@endorsement_blueprint.route('/new/<id>', methods=['GET'])
def new(id):
    image = Image.get_by_id(id)
    # create client token and pass to template
    return render_template('endorsement/new.html',token=gateway.client_token.generate(),image=image)


@endorsement_blueprint.route('/<id>', methods=['POST'])
@login_required
def create(id):
    amount = float(request.form['amount'])
    result = gateway.transaction.sale({
        "amount": ("%.2f" % amount ),
        "payment_method_nonce": request.form['payment_method_nonce'],
        "options": {
            "submit_for_settlement": True
        }
    })
    if result.is_success or result.transaction:
        print(result)
        endorse = Endorsement(donor=current_user.id,image=id,amount=result.transaction.amount)
        if endorse.save():
            endorsement_email(current_user,result.transaction.amount)
            flash("Payment made.","success")
            return redirect(url_for('users.show',username=current_user.username))
        else:
            flash("Something went wrong. Try again later.","danger")
            render_template("users/show.html",username=current_user.username)
    else:
        for x in result.errors.deep_errors: 
            flash(f'Error- {x.code}: {x.message}' ,"danger")
        return redirect(url_for('users.show',username=current_user.username))