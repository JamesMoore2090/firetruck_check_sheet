import os
import uuid
import psycopg2
import psycopg2.extras
from flask import Flask, session, jsonify, render_template, redirect, request, url_for 
# from flask_socketio import join_room, leave_room
# from flask.ext.socketio import SocketIO, emit


app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')

def connectToDB():
  connectionString = 'dbname=quiz user=postgres password=Moore3700 host=localhost'
#   print connectionString
  try:
    return psycopg2.connect(connectionString)
  except:
    print("Can't connect to database")
    
@app.route('/', methods=['GET', 'POST'])
def mainIndex():
    
    if request.method == 'POST':
        db = connectToDB()
        cur = db.cursor()
        print('logging in')
        username = request.form['username']
        session['username'] = username
        pw = request.form['password']
        query = "select * from users WHERE usersname = '%s' AND password = crypt('%s', password)" % (username, pw)
        print query
        try:
            cur.execute(query)
        except:
            print('Login Failed')
            return render_template('login.html')
        user = cur.fetchone()
        session['usertype'] = user[3]
        print user[3]
        if user[4] is not None:
            session['class'] = user[4]
        else: 
            session['class'] = ''
        if user[3] == 1:
            return render_template('adminhome.html', username = session['username'], userType = session['usertype'])
        else:
            return render_template('userhome.html', username = session['username'], userType = session['usertype'])
    else:
        return render_template('login.html')

@app.route('/adminhome')
def adminhome():
    return render_template('adminhome.html', username = session['username'], userType = session['usertype'])

@app.route('/settings', methods = ['GET', 'POST'])
def settings():
        return render_template('settings.html', username = session['username'], userType = session['usertype'])

@app.route('/changePassword', methods = ['POST'])
def passChange():
    print('test before post')
    if request.method == 'POST':
        print 'test after post'
        password = request.form['password']
        print(password)
        update = "UPDATE users set password = crypt('%s', gen_salt('bf')) WHERE usersname = '%s'" % (password, session['username'])
        print(update)
        try:
            db = connectToDB()
            cur = db.cursor()
            cur.execute(update)
        except:
            print("update failed")
            db.rollback()
        db.commit()
        return render_template('adminhome.html', username = session['username'], userType = session['usertype'])

@app.route('/allusers')
def allusers():
    db = connectToDB()
    cur = db.cursor()
    query = "SELECT users.username, class.class, userType.userType from users join on id_class.class = users.class, users join on id.usertype = users.usertype"
    try:
        cur.execute(query)
    except:
        print('failed '+query)
    users = cur.fetchall()
    return render_template('allusers.html', users=users, username = session['username'], userType = session['usertype'])
        

@app.route('/logout', methods = ['GET'])
def logout():
    if request.method == 'GET':

      session.pop('username', None)
      session.pop('class', None)
      session.pop('usertype', None)
      
    return redirect(url_for("mainIndex"))




if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=8080)