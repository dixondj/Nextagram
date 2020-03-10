import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def endorsement_email(receiver,amount):
    print(receiver.email)
    message = Mail(
        from_email='dixondj94@gmail.com',
        to_emails='dixondj94@gmail.com',
        subject='Thanks for your Endorsement',
        html_content=f"<h1>Dear {receiver.username},</h1><br/>Thank you very much for your recent donation of {amount} USD.<br/><br/><h1>NEXTAGRAM</h1>")
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e)) 