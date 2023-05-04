import numpy as np


from flask import Flask,render_template,request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")
    

@app.route('/speech')
def home1():
    import speech
    return render_template("function.html")


@app.route('/object')
def home2():
    import object
    return render_template("function.html")

if __name__ == '__main__':
  app.run(debug=True,port=5000)