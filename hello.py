from flask import Flask
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


if __name__ == '__main__':
    app.run(port=5000)
