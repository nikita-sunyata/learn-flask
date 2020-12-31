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
import os
from flask_sqlalchemy import SQLAlchemy

#every class derived from FlaskForm will be a webform.
class NameForm(FlaskForm):
    name = StringField('What is your name?',validators=[DataRequired()])
    submit = SubmitField('Submit')


#set sqlite path
basedir = os.path.abspath(os.path.dirname(__file__))



app = Flask(__name__) # when this program is the main program , '__main__' is going to be the parameter
app.config['SECRET_KEY'] = 'this is the secret key'
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir,'data.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
#define db's tables
class Role(db.Model):
    __tablename__  = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    #add backref
    users = db.relationship('User',backref='role',lazy='dynamic')
    def __repr__(self):
        return '<Role {}>'.format(self.name)
    # def __init__(self,id,name,users):
    #     self.id = id
    #     self.name = name
    #     self.users = users

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User {}>'.format(self.username)
    # def __init__(self,id,username,role_id):
    #     self.id = id
    #     self.username = username
    #     self.role_id = role_id

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,User=User,Role=Role)


#two way to route
# first is using decorator
@app.route('/',methods=['GET','POST'])
def index():
    # name = None
    form = NameForm() # create an instence of NameForm() class
    if form.validate_on_submit():
        #use the user input name to search database to see if the person is already in it.
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
        #create new user row
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            # add a new pair data to our app session dictionary. (like cookies)
            session['known']=False
        else:
            session['known']=True
        # add another app session data , cuz we're redircting the page , we need to remember this value
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',current_time=datetime.utcnow(),form=form,name=session.get('name'),known=session.get('known',False))




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