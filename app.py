from flask import Flask, render_template, request, redirect, session, url_for, flash, g
#import cv2
#import numpy as np
import sqlite3
import base64
import subprocess



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'


con=sqlite3.connect("database.db")
con.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL,mobile INTEGER NOT NULL,password TEXT NOT NULL)")
con.close()


username=""

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            username=request.form['username'] 
            mobile=request.form['mobile']
            password=request.form['password']
            print(username)
            print(mobile)
            print(password)
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("insert into users(username,mobile,password)values(?,?,?)",(username,mobile,password))
            con.commit()    
            flash("Record Added Successfully","success")
            return render_template("login.html")
        except:
            flash("Error in Insert Operations","danger")

    return render_template("register.html")


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        
        username=request.form['username'] 
        session["username"]=request.form['username'] 
        password=request.form['password']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from users where username=? and password=?",(username,password))
        data=cur.fetchone()
        
        if data:
            session["username"]=data["username"]
            return render_template("function.html")
        else:
            flash("Usernaem and Password Mismatch","danger")
            return redirect("login")

    return render_template("login.html")


@app.route('/speech')
def speech():
    import speech1
    return render_template("function.html")


@app.route('/object')
def object():
    subprocess.call(["python", "object.py", session["username"]])
    import object
    return render_template("function.html")


if __name__ == '__main__':
    app.run(debug=True)

