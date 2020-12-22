from flask import Flask
from flask import request
from flask import current_app
from flask import redirect
from flask import render_template
from flask_bootstrap import Bootstrap
from flask import url_for
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField , SubmitField
from wtforms.validators import DataRequired
from flask import session
from flask import redirect
from flask import flash

class NameForm(FlaskForm):
    name = StringField('What is your name?',validators=[DataRequired()])
    submit = SubmitField('Submit')



app = Flask(__name__) # when this program is the main program , '__main__' is going to be the parameter
app.config['SECRET_KEY'] = 'this is the secret key'
bootstrap = Bootstrap(app)
moment = Moment(app)
#two way to route
# first is using decorator
@app.route('/',methods=['GET','POST'])
def index():
    # name = None
    form = NameForm() # create an instence of NameForm() class
    if form.validate_on_submit():
        old_name = session.get('name') # check if there is an old session name
        if (old_name is not None) and (old_name != form.name.data):
            flash('Looks like you have changed your name !')
        session['name'] = form.name.data # store the current name to session
        return redirect(url_for('index'))
    return render_template('index.html',current_time=datetime.utcnow(),form=form,name=session.get('name'))
    # return '<h1>Hello World</h1>'
#second is using app.add_url_rule() function to do so
# def index():
#     return '<h1>Hello World</h1>'
# app.add_url_rule('/','index',index)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name = name)
    # return '<h1>Hello, {}</h1>'.format(name)
    # return '<h1>{}</h1>'.format(request.values)
    # return current_app.name
    # return r'<h1>{}</h1>'.format(app.url_map)

@app.route('/google')
def google():
    return redirect('https://www.google.com')



# error handle
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404
@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'),500


if __name__ == '__main__':
    print(app.url_map)
    # print(url_for('static',filename='favicon.ico'))
    # print(app.config)
    app.run(port=5000,debug=True)