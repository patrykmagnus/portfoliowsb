from flask import Flask, render_template, request, abort, redirect, url_for, make_response
from flask import Flask, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google

import secrets
import os
from azureDB import AzureDB

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

github_blueprint = make_github_blueprint(
    client_id="8158ba3ef7e6bbfcdef3",
    client_secret="fbeae5a4ae4bc73fad49d0c503aae61dc6194c01",
)
app.register_blueprint(github_blueprint, url_prefix='/login')

blueprint = make_google_blueprint(
    client_id="520736820992-0odhuoa8ihcc5sv5t8leom1mo177mpnb.apps.googleusercontent.com",
    client_secret="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",
    scope=["https://www.googleapis.com/auth/drive.metadata.readonly"]
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route('/')
def login():
    if google.authorized:
        return render_template('index.html')
    if github.authorized:
        return render_template('index.html')

    return render_template('login.html')

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/guestbook')
def result():
    with AzureDB() as a:
        data = a.azureGetData()
    return render_template("result.html", data=data)




# @app.route('/error_denied')
# def error_denied():
#     abort(401)
#
# @app.route('/error_internal')
# def error_internal():
#     return render_template('template.html', name='ERROR 505'), 505
#
# @app.route('/error_not_found')
# def error_not_found():
#     response = make_response(render_template('template.html', name='ERROR 404'), 404)
#     response.headers['X-Something'] = 'A value'
#     return response
#
# @app.errorhandler(404)
# def not_found_error(error):
#     return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
