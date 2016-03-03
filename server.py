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

@app.route('/addUser', methods = ['GET', 'POST'])
def addUser():
    if request.method == 'POST':
        print 'add user to DB'
        username = request.form['username']
        password = request.form['password']
        usertype = request.form['admin_or_user']
        print(username + " " + password + " " + usertype)
        insert = "INSERT INTO users (usersname, password, userstype) VALUES ('%s', crypt('%s', gen_salt('bf')), %s)" % (username, password, usertype) 
        try:
            db = connectToDB()
            cur = db.cursor()
            cur.execute(insert)
        except:
            print('insert fialed')
            print(insert)
            db.rollback()
            return render_template('addUser.html', username = session['username'], userType = session['usertype'])
        db.commit()
        return render_template('adminhome.html', username = session['username'], userType = session['usertype'])
    else:
        return render_template('addUser.html', username = session['username'], userType = session['usertype'])

@app.route('/allUsers', methods = ['GET'])
def allusers():
    db = connectToDB()
    cur = db.cursor()
    query = "SELECT users.usersname, usersType.usersType FROM users INNER JOIN usersType ON userstype.id = users.userstype" #JOIN class ON class.id_class = users.class"
    try:
        cur.execute(query)
    except:
        print('failed '+query)
    users = cur.fetchall()
    return render_template('allUsers.html', users=users, username = session['username'], userType = session['usertype'])
        

@app.route('/addClass', methods = ['GET', 'POST'])
def addClass():
    if request.method == 'POST':
        # connect to the database
        db = connectToDB()
        cur = db.cursor()
        error = None
        classes = None
        print 'Add class'
        className = request.form['className']
        select = "SELECT exists(SELECT * FROM class WHERE class LIKE '%s')" % (className)
        try:
            print select
            cur.execute(select)
            classes = cur.fetchone()
            print classes
        except:
            print 'SELECT failed'
        if classes == True:
            error = "%s has been already entered" % (className)
            print error
        else:
            insert = "INSERT INTO class (class) VALUES ('%s')" % (className)
            try:
                cur.execute(insert)
            except:
                db.rollback()
                print insert
                print('insert Failed')
            db.commit()
  
        return render_template('addClass.html', error=error, username = session['username'], userType = session['usertype'])  
    else:
        return render_template('addClass.html', username = session['username'], userType = session['usertype'])

@app.route('/allClasses', methods = ['GET'])
def allclasses():
    db = connectToDB()
    cur = db.cursor()
    query = "SELECT class FROM class"
    try:
        cur.execute(query)
    except:
        print('failed '+query)
    classes = cur.fetchall()
    return render_template('allClasses.html', classes=classes, username = session['username'], userType = session['usertype'])
 
@app.route('/addBook', methods = ['GET', 'POST'])
def addBook():
    db = connectToDB()
    cur = db.cursor()
    if request.method == 'POST':
        print 'adding book'
        book = request.form['nameBook']
        Class = request.form['classes']
        insert = "INSERT INTO book (book, class) VALUES('%s', (SELECT id_class FROM class WHERE class = '%s'))" % (book, Class)
        print insert
        try:
            cur.execute(insert)
        except:
            db.rollback()
            print 'insert failed'
        db.commit()
        return render_template('adminhome.html', username = session['username'], userType = session['usertype'])
    else:
        
        query = "SELECT * FROM class"
        try:
            cur.execute(query)
        except:
            print('failed '+query)
        classes = cur.fetchall()
   
        return render_template('addBook.html', classes=classes, username = session['username'], userType = session['usertype'])


@app.route('/allBooks', methods = ['GET'])
def allBook():
    db = connectToDB()
    cur = db.cursor()
    select = "SELECT book.book, class.class FROM book JOIN class ON book.class = class.id_class"
    try:
        cur.execute(select)
    except:
        print(select)
        print("^failed")
    bookInfo = cur.fetchall()
    return render_template('allBooks.html', books = bookInfo, username = session['username'], userType = session['usertype'])

@app.route('/addChapters', methods = ['GET', 'POST'])
def addChapters():
    db = connectToDB()
    cur = db.cursor()
    if request.method == 'POST':
        book = request.form['book']
        chapter = request.form['Chapter']
        insert = "INSERT INTO chapter (chapter, book) VALUES ('%s', (SELECT id_book FROM book WHERE book = '%s'))" % (chapter, book)
        try:
            cur.execute(insert)
        except:
            db.rollback()
            print insert
            print "^failed"
        db.commit()
        select = "SELECT book from book"
        try:
            cur.execute(select)
        except:
            print "Select failed"
        books = cur.fetchall()
    else:
        select = "SELECT book from book"
        try:
            cur.execute(select)
        except:
            print "Select failed"
        books = cur.fetchall()
    return render_template('addChapters.html', books = books,username = session['username'], userType = session['usertype'])


@app.route('/allChapter', methods = ['GET', 'POST'])
def allChapter():
    db = connectToDB()
    cur = db.cursor()
    if request.method == 'POST':
        book = request.form['book']
        chapterSelect = "SELECT book.book, chapter.chapter FROM book JOIN chapter ON book.id_book = chapter.book WHERE book.book = '%s'" % (book)
        try:
            cur.execute(chapterSelect)
        except:
            print chapterSelect
            print "^Failed"
        allChapters = cur.fetchall()
        return render_template('allChapters.html', allChapters=allChapters,username = session['username'], userType = session['usertype'])
    else: 
        select = "SELECT book from book"
        try:
            cur.execute(select)
        except:
            print "Select failed"
        books = cur.fetchall()
        return render_template('allChapters.html', books = books ,username = session['username'], userType = session['usertype'])

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