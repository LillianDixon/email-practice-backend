from flask import Flask, request, jsonify, session
from flask_mail import Mail, Message
from flask_cors import CORS
from flask_heroku import Heroku
# import config
import os

app=Flask(__name__)
CORS(app)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = os.environ('MAIL_USERNAME'),
    MAIL_PASSWORD = os.environ('MAIL_PASSWORD'),
    # MAIL_USERNAME = config.MAIL_USERNAME,
    # MAIL_PASSWORD = config.MAIL_PASSWORD,
    MAIL_DEFAULT_SENDER = 'myemail@testemail.com'
)

heroku=Heroku(app)
mail=Mail(app)

@app.route("/")
def home():
    return"<h1>Hi from Flask</h1>"

@app.route("/email", methods=['POST'])
def index():
    if request.content_type == 'application/json':
        get_data = request.get_json()
        name = get_data.get('name')
        sender = get_data.get('email')
        recipients = [os.environ('MAIL_USERNAME')]
        # recipients = [config.MAIL_USERNAME]
        headers = [name, sender] + recipients
        subject = get_data.get('subject')
        message = get_data.get('message')
        body = message + "\n\n" + name
    msg = Message(subject, headers, body)
    print(Message)
    mail.send(msg)
    return jsonify('Message has been sent')

    
if __name__ == "__main__":
    app.debug = True
    app.run()