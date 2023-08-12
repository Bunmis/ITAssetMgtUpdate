from flask import Flask, session, request
from views import views
import pandas as pd
import os
from flask_mail import Mail

app = Flask(__name__)
app.secret_key = "super secret key"

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

# Send email
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bunmistic@gmail.com'
app.config['MAIL_PASSWORD'] = 'kpxosjnjoohgidlu'#'mqgrobynqgarhlpo'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.register_blueprint(views, url_prefix="/")

if __name__ == '__main__':
    app.run(host="localhost", debug=True, port=8000)