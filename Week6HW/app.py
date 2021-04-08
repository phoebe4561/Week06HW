from flask import Flask,render_template,url_for,request,session,redirect,flash
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import os
import json

app = Flask(
    __name__
    # static_folder="static",
    # static_url_path="/"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mypassword@localhost:3306/website'
app.config['SECRET_KEY'] = os.urandom(24)

db = SQLAlchemy(app)

class newuser(db.Model):
    __table_args__ = {
        'comment': 'Notice table'
    }
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, comment='編號') 
    name = db.Column(db.String(50), nullable = False, comment = '姓名') 
    username = db.Column(db.String(50), nullable = False, comment = '帳號') 
    password = db.Column(db.String(50), nullable = False, comment = '密碼') 
    time = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True),nullable = False, server_default = sqlalchemy.sql.func.now(), comment = '註冊時間')

    def __init__ (self,name,username,password):
        self.name = name
        self.username = username
        self.password = password

@app.route("/")
def index():
    return render_template("index.html")


#註冊
@app.route("/signup", methods = ["POST", "GET"])
def signup():
    if request.method == "POST":
      user = request.form["name"]
      username = request.form["username"]
      password = request.form["password"]

      sameuser = newuser.query.filter_by(username=username).first() 
      if sameuser:
           return redirect (url_for("error", message="此帳號已被註冊"))
      else:
           new_user = newuser(name=user, username=username, password=password)
           db.session.add(new_user)
           db.session.commit()
           flash ("註冊成功請登入!")
           return redirect ("/")  

    return redirect("/")

#登入
@app.route("/signin", methods = ["POST", "GET"])
def signin():
    if request.method == "POST":
       username = request.form["username"]
       password = request.form["password"]
       session["username"] = username

       old_user = newuser.query.filter_by(username=username).first()
       if old_user and old_user.password == password:
            user = newuser.query.filter_by(name= old_user.name).first()
            session["user"] = user.name
            session.permanent=True
            session["count"]=1
            flash ("成功登入!")
            return redirect(url_for("member"))
       else:
            return redirect (url_for("error", message="帳號或密碼錯誤"))
    else:
        return redirect ("/member")



@app.route("/member")
def member():
    if "username" in session:
        if session["count"]>1:
            flash ("您已經登入過了!")
        session["count"]+=1
        return render_template("member.html",membername=session["user"])
    else:
        flash ("您尚未登入!")
        return redirect("/")


@app.route("/error")
def error():
    error_message = request.args.get("message")
    return render_template("error.html", message = error_message)

@app.route("/signout")
def signout():
    flash ("您已經登出!")
    session.pop("username", None)
    session.pop("count",None)
    return redirect("/")


if __name__ == "__main__": 
    app.run(port=3000,debug=True)





#登入
# @app.route("/signin", methods = ["POST", "GET"])
# def signin():
#     if request.method == "POST":
#        username = request.form["username"]
#        password = request.form["password"]
#        session["username"] = username
       
#        old_user = myuser.query.filter_by(username=username).first()
#        if old_user:
#           if old_user.password == password:
#              user = myuser.query.filter_by(name=user.name).first() 
#              session["user"] = user
#              return redirect (url_for("member",membername=user))
#           else:
#              return redirect (url_for("error", message="帳號或密碼錯誤"))
#     else:
#         return redirect ("/")
