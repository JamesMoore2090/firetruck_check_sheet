import os
import dbConnect
import allcaps
import uuid
import psycopg2
import psycopg2.extras
import wtform
from flask import Flask, session, jsonify, render_template, redirect, request, url_for 
# from flask_socketio import join_room, leave_room
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')
socketio = SocketIO(app)

@socketio.on('connect', namespace='/check')
def makeConnection():
    session['uuid'] = uuid.uuid1()
    print ('Connected')
    
@socketio.on('identify', namespace='/check')
def on_identify(user):
    print('Identify: ' + user)
    # users[session['uuid']] = {'username' : user}
    
    
   
@socketio.on('search', namespace='/check')
def search(searchItem):
    select = '''SELECT engine.engine_id, u1.username as driver, users.username as officer, truck.truck FROM checksheet JOIN engine ON 
    checksheet.engine_id = engine.engine_id JOIN users u1 ON engine.driver = u1.user_id JOIN truck 
    ON checksheet.truck = truck.truck_id JOIN users ON engine.officer = users.user_id
    WHERE engine.check_date = %s '''
    print("I am here")
    
    db = dbConnect.connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    searchQuery = ""
    results = []
    queryResults = []
    searchTerm = '%{0}%'.format(searchItem)
    
    
    #print(searchItem)
    
    cur.execute(select, (searchItem,));
    results = cur.fetchall();
    
    print(results)
    
    # for i in range(len(results)):
    #     resultsDict = {'text' : results[i]['movie_title']}
    #     queryResults.append(resultsDict)
        
    emit('searchResults', results)
    cur.close()
    db.close()
    
@socketio.on('searchApproval', namespace='/check')
def searchApproval(searchItem):
    select = '''SELECT engine.engine_id, u1.username as driver, users.username as officer, truck.truck, checksheet.officerapproval FROM checksheet JOIN engine ON 
    checksheet.engine_id = engine.engine_id JOIN users u1 ON engine.driver = u1.user_id JOIN truck 
    ON checksheet.truck = truck.truck_id JOIN users ON engine.officer = users.user_id
    WHERE engine.check_date = %s '''
    print("I am here")
    
    db = dbConnect.connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    searchQuery = ""
    results = []
    queryResults = []
    searchTerm = '%{0}%'.format(searchItem)
    
    
    #print(searchItem)
    
    cur.execute(select, (searchItem,));
    results = cur.fetchall();
    
    print(results)
    
    # for i in range(len(results)):
    #     resultsDict = {'text' : results[i]['movie_title']}
    #     queryResults.append(resultsDict)
        
    emit('approvalResults', results)
    cur.close()
    db.close()


@app.route('/', methods=['GET', 'POST'])
def mainIndex():
    
    if request.method == 'POST':
        db = dbConnect.connectToDB()
        cur = db.cursor()
        print('logging in')
        username = request.form['username']
        session['username'] = username
        pw = request.form['password']
        query = "select * from users WHERE username = %s AND password = crypt(%s, password)" 
        print(query,(username, pw))
        try:
            cur.execute(query, (username, pw,))
        except:
            print('Login Failed')
            return render_template('login.html')
        user = cur.fetchone()
        print user
        if user > 0:
            
            session['usertype'] = user[3]
            print session['username'] 
            print session['usertype']
            return(sendToPage())
        
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/step1', methods = ['GET', 'POST'])
def step1():
    db = dbConnect.connectToDB()
    cur = db.cursor()
    if request.method == 'POST':
        truck = request.form['truck']
        driver = request.form['driver']
        officer = request.form['officer']
        date = request.form['date']
        mileage = request.form['mileage']
        engHours = request.form['hours']
        fuel = request.form['fuel']
        # do special stuff because it is a brush truck
        if truck == 'brush':
            insert = 'INSERT INTO brush_truck (truck, check_date, driver, officer,miles,fuel,hours) VALUES (3, %s, %s, %s, %s, %s, %s)'
            print insert
            try:
                cur.execute(insert, (date,driver,officer,mileage,fuel,engHours,))
            except:
                print 'insert brush Failed'
                db.rollback()
            db.commit()
            select = 'SELECT brush_truck_id FROM brush_truck WHERE check_date = %s AND driver = %s'
            try:
                cur.execute(select, (date,driver,))
            except:
                print 'select Failed'
            engID = cur.fetchone()
            eng_ID = engID[0]
            insert = 'INSERT INTO checksheet (user_id, officerApproval, brush_id, truck) VALUES ((SELECT user_id FROM users WHERE username = %s), FALSE, %s, 3)'
            try:
                cur.execute(insert, (session['username'], eng_ID,))
                db.commit()
            except:
                db.rollback()
                print 'insert into checksheet failed'
                
            return render_template('brush.html', engID = eng_ID, username = session['username'], userType = session['usertype'])
        else:
            rescue_engine = None
            truckID = None
            if truck == 'rescue_engine':
                rescue_engine = truck
                truckID = 1
            elif truck == 'engine':
                truckID = 2
            elif truck == 'brush':
                truckID = 3
            else:
                truckID = 4
            insert = 'INSERT INTO engine (truck, check_date, driver, officer,miles,fuel,hours) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            print insert
            try:
                cur.execute(insert, (truckID,date,driver,officer,mileage,fuel,engHours,))
            except:
                print 'insert Failed'
                db.rollback()
            db.commit()
 
            select = 'SELECT engine_id FROM engine WHERE check_date = %s AND driver = %s'
            try:
                cur.execute(select, (date,driver,))
            except:
                print 'select Failed'
            engID = cur.fetchone()
            
            eng_ID = engID[0]
            insert = 'INSERT INTO checksheet (user_id, officerApproval, engine_id, truck) VALUES ((SELECT user_id FROM users WHERE username = %s), FALSE, %s, %s)'
            try:
                cur.execute(insert, (session['username'], eng_ID,truckID,))
                db.commit()
            except:
                db.rollback()
                print 'insert into checksheet failed'
            
        
        return render_template('step2.html', engID = eng_ID, rescue_engine = rescue_engine, username = session['username'], userType = session['usertype'])
        
    else:
        select = 'SELECT user_id, username FROM users WHERE usertype in (1,2,3,4,5,6)' 
        try:
            cur.execute(select)
        except:
            print select 
            print 'failed^'
        drivers = cur.fetchall()
        select = 'SELECT user_id, username FROM users WHERE usertype in (3,4,5,6,7,8,11,12)'
        try:
            cur.execute(select)
        except:
            print select 
            print 'failed^'
        officers = cur.fetchall()
        return render_template('step1.html', drivers = drivers, officers = officers, username = session['username'], userType = session['usertype'])

@app.route('/step2', methods = ['GET', 'POST'])
def step2():
    print 'step 2'
    db = dbConnect.connectToDB()
    cur = db.cursor()
    if request.method == 'POST':
        truck = request.form['rescue_engine']
        engID = request.form['check_id']
        print truck + " " + engID 
        fuelCard = 'fuelCard' in request.form
        fuelCard = allcaps.allCaps(fuelCard)
        headlights = 'headlights' in request.form
        headlights = allcaps.allCaps(headlights)
        markerlights = 'markerlights' in request.form
        markerlights = allcaps.allCaps(markerlights)
        turnsignals = 'turnsignals' in request.form
        turnsignals = allcaps.allCaps(turnsignals)
        warninglights = 'warninglights' in request.form
        warninglights = allcaps.allCaps(warninglights)
        siren = 'siren' in request.form
        siren = allcaps.allCaps(siren)
        airhorn = 'airhorn' in request.form
        airhorn = allcaps.allCaps(airhorn)
        tires = 'tires' in request.form
        tires = allcaps.allCaps(tires)
        
        
        print headlights
        insert = 'UPDATE engine SET fuelcard = %s, headlights = %s, markerlights = %s, turnsignals = %s, warninglights = %s, sirens = %s, airhorn = %s, tires = %s WHERE engine_id = %s'
        try:
            cur.execute(insert,(fuelCard, headlights, markerlights, turnsignals, warninglights, siren, airhorn, tires, engID,))
        except:
            print 'Update Failed :{'
            db.rollback()
        db.commit()
        return render_template('step3.html',engID = engID, rescue_engine = truck, username = session['username'], userType = session['usertype'])
        
@app.route('/step3', methods = ['GET', 'POST'])
def step3():
    print 'step3'
    db = dbConnect.connectToDB()
    cur = db.cursor()
    if request.method == 'POST':
        truck = request.form['rescue_engine']
        engID = request.form['check_id']
        pumpOperation = 'pumpoperation' in request.form
        pumpOperation = allcaps.allCaps(pumpOperation)
        waterlevel = request.form['waterlevel']
        foamlevel = request.form['foamlevel']
        generator = 'generator' in request.form
        generator = allcaps.allCaps(generator)
        scenelights = 'scenelights' in request.form
        scenelights = allcaps.allCaps(scenelights)
        update = 'UPDATE engine SET pumpOperation = %s, waterlevel = %s, foamlevel = %s, generator = %s, scenelights = %s WHERE engine_id = %s'
        try:
            cur.execute(update, (pumpOperation, waterlevel, foamlevel, generator, scenelights, engID,))
            db.commit()
        except:
            db.rollback()
            print 'update 3 failed'
        return render_template('step4.html', engID = engID, rescue_engine = truck, username = session['username'], userType = session['usertype'])
        
        
@app.route('/step4', methods = ['GET', 'POST'])
def step4():
    print 'step4'
    db = dbConnect.connectToDB()
    cur = db.cursor()
    if request.method == 'POST':
        truck = request.form['rescue_engine']
        engID = request.form['check_id']
        helmetmarkers = 'helmetmarkers' in request.form
        helmetmarkers = allcaps.allCaps(helmetmarkers)
        portableradio = request.form['portRadio']
        passport = 'passport' in request.form
        passport = allcaps.allCaps(passport)
        commandboard = 'commandboard' in request.form
        commandboard = allcaps.allCaps(commandboard)
        erg = 'erg' in request.form
        erg = allcaps.allCaps(erg)
        mapbook = 'mapbooks' in request.form
        mapbook = allcaps.allCaps(mapbook)
        headsets = 'headsets' in request.form
        headsets = allcaps.allCaps(headsets)
        forms = 'forms' in request.form
        forms = allcaps.allCaps(forms)
        
        update = 'UPDATE engine SET helmetmarkers = %s, portableradio = %s, passport = %s, commandboard = %s, erg = %s, mapbook= %s, headsets = %s, forms = %s WHERE engine_id = %s'
        try:
            cur.execute(update, (helmetmarkers, portableradio, passport, commandboard, erg, mapbook, headsets, forms, engID,))
            db.commit()
        except:
            print(update, (helmetmarkers, portableradio, passport, commandboard, erg, mapbook, headsets, forms,))
            db.rollback()
            print 'update 4 failed'
        return render_template('step5.html', engID = engID, rescue_engine = truck, username = session['username'], userType = session['usertype'])
        
@app.route('/step5', methods = ['GET', 'POST'])
def step5():
    print 'step5'
    db = dbConnect.connectToDB()
    cur = db.cursor()
    if request.method == 'POST':
        truck = request.form['rescue_engine']
        engID = request.form['check_id']
        thermalimager = 'thermalimager' in request.form
        thermalimager = allcaps.allCaps(thermalimager)
        paktracker = 'paktracker' in request.form
        paktracker = allcaps.allCaps(paktracker)
        ladders = 'ladders' in request.form
        ladders = allcaps.allCaps(ladders)
        gasmonitor = request.form['gasmonitor']
        handlights = request.form['handlights']
        binoculars = 'binoculars' in request.form
        binoculars = allcaps.allCaps(binoculars)
        smokedetectors = request.form['smokedetectors']
        batteries = request.form['batteries']
        SCBA = request.form['SCBA']
        ritpack = 'RITpack' in request.form
        ritpack = allcaps.allCaps(ritpack)
        roadflares = request.form['roadflares']
        eroadflares = request.form['portRadio']
        hoses = 'hosenozzles' in request.form
        hoses = allcaps.allCaps(hoses)
        appliances = 'appliances' in request.form
        appliances = allcaps.allCaps(appliances)
        roadsign = 'roadsign' in request.form
        roadsign = allcaps.allCaps(roadsign)
        absorbant = 'absorbant' in request.form
        absorbant = allcaps.allCaps(absorbant)
        handtools = 'handtools' in request.form
        handtools = allcaps.allCaps(handtools)
        sawzall = 'sawzall' in request.form
        sawzall = allcaps.allCaps(sawzall)
        chimneykit = 'chimneykit' in request.form
        chimneykit = allcaps.allCaps(chimneykit)
        saws = 'saws' in request.form
        saws = allcaps.allCaps(saws)
        extinguishers = 'extinguishers' in request.form
        extinguishers = allcaps.allCaps(extinguishers)
        fans = 'fans' in request.form
        fans = allcaps.allCaps(fans)
        spillcont = 'spillcont' in request.form
        spillcont = allcaps.allCaps(spillcont)
        salvage = 'salvage' in request.form
        salvage = allcaps.allCaps(salvage)
        lifeline = 'lifeline' in request.form
        lifeline = allcaps.allCaps(lifeline)
        utilityrope = 'utilityrope' in request.form
        utilityrope = allcaps.allCaps(utilityrope)
        rigging = 'rigging' in request.form
        rigging = allcaps.allCaps(rigging)
        pikepoles = 'pikepoles' in request.form
        pikepoles = allcaps.allCaps(pikepoles)
        electicalequip = 'electicalequip' in request.form
        electicalequip = allcaps.allCaps(electicalequip)
        hondalight = 'hondalight' in request.form
        hondalight = allcaps.allCaps(hondalight)
        cribbing = 'cribbing' in request.form
        cribbing = allcaps.allCaps(cribbing)
        spreaders = 'spreaders' in request.form
        spreaders = allcaps.allCaps(spreaders)
        ocutters = 'ocutters' in request.form
        ocutters = allcaps.allCaps(ocutters)
        hydropump = 'hydropump' in request.form
        hydropump = allcaps.allCaps(hydropump)
        paratech = 'paratech' in request.form
        paratech = allcaps.allCaps(paratech)
        lchannel = 'lchannel' in request.form
        lchannel = allcaps.allCaps(lchannel)
        portaPump = 'portaPump' in request.form
        portaPump = allcaps.allCaps(portaPump)
        airbagcontroler = 'airbagcontroller' in request.form
        airbagcontroler = allcaps.allCaps(airbagcontroler)
        airbags = 'airbags' in request.form
        airbags = allcaps.allCaps(airbags)
        update = '''UPDATE engine SET thermalimager = %s, paktracker = %s, ladders = %s, gasmonitor = %s, 
                handlights = %s, binoculars = %s, smokedetectors = %s, batteries = %s, SCBA = %s, ritpack = %s,
                roadflares = %s, eroadflares = %s, hoses = %s, appliances = %s, roadsign = %s, absorbant= %s,
                handtools = %s, sawzall = %s, chimneykit = %s, saws = %s, extinguishers = %s, fans = %s,
                spillcont = %s, salvage = %s, lifeline = %s, utilityrope = %s, rigging = %s, pikepoles = %s,
                electicalequip = %s, hondalight = %s, cribbing = %s, spreaders = %s, ocutters= %s, hydropump = %s,
                paratech = %s, lchannel = %s, portaPump = %s, airbagcontroler = %s, airbags = %s
                WHERE engine_id = %s'''
        try:
            cur.execute(update, (thermalimager,paktracker, ladders,gasmonitor, handlights, binoculars, smokedetectors,
                batteries, SCBA, ritpack, roadflares, eroadflares, hoses, appliances, roadsign, absorbant, handtools, sawzall,
                chimneykit, saws, extinguishers, fans, spillcont, salvage, lifeline, utilityrope, rigging, pikepoles,
                electicalequip, hondalight, cribbing, spreaders, ocutters, hydropump,paratech, lchannel, portaPump,
                airbagcontroler, airbags, engID,))
            db.commit()
        except:
            db.rollback()
            print 'UPDATE 5 failed......'
        return render_template('step6.html', engID = engID, username = session['username'], userType = session['usertype'])


@app.route('/step6', methods = ['GET', 'POST'])
def step6():
    print 'step5'
    db = dbConnect.connectToDB()
    cur = db.cursor()
    if request.method == 'POST':
        engID = request.form['check_id']
        jumpbag = 'jumpbag' in request.form
        jumpbag = allcaps.allCaps(jumpbag)
        o2level = request.form['o2level']
        spareo2 = 'spareo2' in request.form
        spareo2 = allcaps.allCaps(spareo2)
        collarbag = 'collarbag' in request.form
        collarbag = allcaps.allCaps(collarbag)
        gloves = 'golves' in request.form
        gloves = allcaps.allCaps(gloves)
        clipboard = 'clipboard' in request.form
        clipboard = allcaps.allCaps(clipboard)
        suckunit = 'suckunit' in request.form
        suckunit = allcaps.allCaps(suckunit)
        triagebag = 'triagebag' in request.form
        triagebag = allcaps.allCaps(triagebag)
        lifepak = request.form['lifepak']
        toughbook = 'toughbook' in request.form
        toughbook = allcaps.allCaps(toughbook)
        notes = request.form['notes']
        update = '''UPDATE engine SET jumpbag = %s, o2level = %s, spareo2 = %s, collarbag = %s, gloves = %s,
                clipboard = %s, suckunit = %s, triagebag = %s, lifepak = %s, toughbook = %s, notes = %s 
                WHERE engine_id = %s'''
        try:
            cur.execute(update, (jumpbag, o2level, spareo2, collarbag,gloves, clipboard, suckunit, triagebag, lifepak, toughbook, notes, engID,))
            db.commit()
        except:
            db.rollback()
            print 'step6 failed'
        return(sendToPage())
    
@app.route('/review', methods = ['GET'])
def review():
    db = dbConnect.connectToDB()
    cur = db.cursor()
    data = None
    brushdata = None
    select = '''select checksheet.check_id, checksheet.officerapproval, truck.truck, engine.check_date FROM 
                checksheet JOIN truck ON checksheet.truck = truck.truck_id JOIN engine ON 
                checksheet.engine_id = engine.engine_id
                WHERE checksheet.user_id = (SELECT user_id FROM users WHERE username = %s)'''
    try:
        cur.execute(select, (session['username'],))
        data = cur.fetchall()
    except:
        print 'review query failed'
    
    select = '''select checksheet.check_id, checksheet.officerapproval, truck.truck, brush_truck.check_date FROM 
                checksheet JOIN truck ON checksheet.truck = truck.truck_id JOIN brush_truck ON 
                checksheet.brush_id = brush_truck.brush_truck_id
                WHERE checksheet.user_id = (SELECT user_id FROM users WHERE username = %s)'''
    try:
        cur.execute(select, (session['username'],))
        brushdata = cur.fetchall()
    except:
        print 'review query failed'
    print brushdata
    #newData = data.append(brushdata)
    return render_template('review.html', data = data, brushdata = brushdata, username = session['username'], userType = session['usertype'])
  
#   Need to add a join for the usernames!
@app.route('/view')
def view():
    db = dbConnect.connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    checkID = request.args.get('check')
    select = '''SELECT engine.*, u1.username as driver, users.username as officer, truck.truck FROM checksheet JOIN engine ON 
    checksheet.engine_id = engine.engine_id JOIN users u1 ON engine.driver = u1.user_id JOIN truck 
    ON checksheet.truck = truck.truck_id JOIN users ON engine.officer = users.user_id
    WHERE check_id = %s'''
    try:
        cur.execute(select, (checkID,))
    except:
        print 'view select failed'
    eng_check = cur.fetchone()
    if eng_check < 1:
        select = '''SELECT brush_truck.*, u1.username as driver, users.username as officer, truck.truck FROM checksheet JOIN brush_truck ON 
            checksheet.brush_id = brush_truck.brush_truck_id JOIN users u1 ON brush_truck.driver = u1.user_id JOIN truck 
            ON checksheet.truck = truck.truck_id JOIN users ON brush_truck.officer = users.user_id
            WHERE check_id = %s'''
        try:
            cur.execute(select, (checkID,))
        except:
            print 'view select failed'
        brush_truck = cur.fetchone()
        return render_template('view.html', brush = brush_truck, username = session['username'], userType = session['usertype'])
    else:
        return render_template('view.html', eng = eng_check, username = session['username'], userType = session['usertype'])

    
@app.route('/submitBrush', methods = ['POST'])
def submitBrush():
    db = dbConnect.connectToDB()
    cur = db.cursor()
    if request.method == 'POST':
        print 'submitBrush'
        brushID = request.form['check_id']
        portableRadios = request.form['portRadio']
        
        headlights = 'headlights' in request.form
        headlights = allcaps.allCaps(headlights)
        
        turnsignals = 'turnsignals' in request.form
        turnsignals = allcaps.allCaps(turnsignals)
        
        mapbook = 'mapbook' in request.form
        mapbook = allcaps.allCaps(mapbook)
        
        warninglights = 'warninglights' in request.form
        warninglights = allcaps.allCaps(warninglights)
        
        spotlight = 'spotlight' in request.form
        spotlight = allcaps.allCaps(spotlight)
        
        waterlevel = request.form['waterlevel']
        foamlevel = request.form['foamlevel']
        
        hoses = 'hoses' in request.form
        hoses = allcaps.allCaps(hoses)
        
        pumpOperation = 'pumpOperation' in request.form
        pumpOperation = allcaps.allCaps(pumpOperation)
        
        handtools = 'handtools' in request.form
        handtools = allcaps.allCaps(handtools)
        
        chainsaw = 'chainsaw' in request.form
        chainsaw = allcaps.allCaps(chainsaw)
        
        wench = 'wench' in request.form
        wench = allcaps.allCaps(wench)
        
        notes = request.form['notes']
        
        update = '''UPDATE brush_truck SET mapbook = %s, headlights = %s, turnsignals = %s, portableradio = %s,
                    emlights = %s, spotlight = %s, waterLevel = %s, foamlevel = %s, hoses = %s, pumpOperation = %s,
                    handtools = %s, chainsaw = %s, wench = %s, notes = %s WHERE brush_truck_id = %s'''
        try:
            cur.execute(update, (mapbook, headlights, turnsignals, portableRadios, warninglights, spotlight, waterlevel, foamlevel, hoses, pumpOperation, handtools, chainsaw,wench,notes, brushID,))
            db.commit()
        except:
            db.rollback()
            print 'UPDATE BRUSH FAILS'
        return(sendToPage())
        
        
@app.route('/createuser', methods = ['GET','POST'])
def createuser():
    db = dbConnect.connectToDB()
    cur = db.cursor()
    if request.method == 'POST':
        print 'creating new user'
        username = request.form['username']
        password = request.form['password']
        utype = request.form['usertype']
        #we are checking to see if a username is already in the system
        check = 'SELECT user_id FROM users WHERE username = %s'
        try:
            cur.execute(check, (username,))
        except:
            print 'check Failed'
        isUser = cur.fetchall()
        if isUser < 1:
            select = 'SELECT * FROM usertype'
            try:
                cur.execute(select)
            except:
                print 'SELECT failed'
            usertype = cur.fetchall()
            error = 'This username is already in use: %s' % (username)
            return render_template('createuser.html', usertype = usertype, error=error, username = session['username'], userType = session['usertype'])
        #at this point we are assumming that they are not in the system now lets add them
        else:
            insert = "INSERT INTO users (username, password, usertype) VALUES (%s, crypt(%s, gen_salt('bf')), %s)"
            try:
                cur.execute(insert, (username, password, utype,))
                db.commit()
            except:
                db.rollback()
                print 'insert Failed'
            if session['usertype'] == 3:
                return render_template('officer.html', username = session['username'], userType = session['usertype'])
            else:
                return render_template('dofficer.html', username = session['username'], userType = session['usertype'])
    else:
        select = 'SELECT * FROM usertype'
        try:
            cur.execute(select)
        except:
            print 'SELECT failed'
        usertype = cur.fetchall()
        return render_template('createuser.html', usertype = usertype, username = session['username'], userType = session['usertype'])

@app.route('/approveCheck', methods = ['GET' , 'POST'])
def allChecks():
    db = dbConnect.connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    form = wtform.approvalForm()
    
    if request.method == 'POST':
        print(form.checkbox.data)
    else:
        data = None
        brushdata = None
        select = '''select checksheet.check_id, truck.truck, engine.check_date FROM 
                    checksheet JOIN truck ON checksheet.truck = truck.truck_id JOIN engine ON 
                    checksheet.engine_id = engine.engine_id WHERE checksheet.officerapproval = %s'''
        try:
            cur.execute(select, ('FALSE',))
            data = cur.fetchall()
        except:
            print 'review query failed'
        
        select = '''select checksheet.check_id, truck.truck, brush_truck.check_date FROM 
                    checksheet JOIN truck ON checksheet.truck = truck.truck_id JOIN brush_truck ON 
                    checksheet.brush_id = brush_truck.brush_truck_id WHERE checksheet.officerapproval = %s'''
        try:
            cur.execute(select, ('FALSE',))
            brushdata = cur.fetchall()
        except:
            print 'review query failed'
        print brushdata
        #newData = data.append(brushdata)
        return render_template('approveCheck.html',form = form, data = data, brushdata = brushdata, username = session['username'], userType = session['usertype'])
    
    
    
    
@app.route('/logout', methods = ['GET'])
def logout():
    if request.method == 'GET':

      session.pop('username', None)
      session.pop('usertype', None)
      
    return redirect(url_for("mainIndex"))


def sendToPage():
    print 'inthe sendtopage'
    if session['usertype'] >= 1 or session['usertype'] <= 4 :
        return render_template('driver.html', username = session['username'], userType = session['usertype'])
    if session['usertype'] >= 5 or session['usertype'] <= 8:
        return render_template('dOfficer.html', username = session['username'], userType = session['usertype'])
    if session['usertype'] >= 9 or session['usertype'] <= 14:
        return render_template('officer.html', username = session['username'], userType = session['usertype'])

if __name__ == '__main__':
    app.debug=True
    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))