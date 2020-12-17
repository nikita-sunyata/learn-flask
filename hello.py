from flask import Flask
from flask import request
from flask import current_app
app = Flask(__name__) # when this program is the main program , '__main__' is going to be the parameter

#two way to route
# first is using decorator
@app.route('/')
def index():
    return '<h1>Hello World</h1>'

#second is using app.add_url_rule() function to do so
# def index():
#     return '<h1>Hello World</h1>'
# app.add_url_rule('/','index',index)

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}</h1>'.format(name)
    # return '<h1>{}</h1>'.format(request.values)
    # return current_app.name
    # return r'<h1>{}</h1>'.format(app.url_map)



if __name__ == '__main__':
    print(app.url_map)
    app.run(port=5000,debug=True)