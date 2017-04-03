# We'll need the session object to manage session variables
# render_template to render html content from templates
# url_for to extract the url for a given view/route
# request to access the GET data request for the form view
# redirect to perform redirects to different routes
from flask import Flask, session, render_template, url_for, request, redirect
app = Flask(__name__)
@app.route('/hi')
def get_session_sgd():
    #if session.get('tmp') == 43:
    #    return 'yes'
    #return 'no'
    if 'tmp' in session:
        print session['tmp']
    return "vdbfj"    
@app.route('/')
def run_meri_ghodi():

    session['tmp'] = 43
    print session['tmp']
    return '43'
if __name__ == '__main__':
    app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
    app.run(
        host="127.0.0.1",
        port=int("8080")
  )
