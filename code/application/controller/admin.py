from flask import render_template
from flask import current_app as app
from flask import request
from datetime import date
from datetime import datetime
from flask import jsonify
from flask import redirect, url_for
from application.models import *
from sqlalchemy import func
admin_logged=None
#home page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        admin_from_db = Admin.query.get(username)
        if admin_from_db:
            password_from_db = admin_from_db.password
            if password_from_db == password:
                global admin_logged
                admin_logged = username
                return redirect(url_for("admin_dash"))
                #return render_template('admin_dash.html')
            else:
                return render_template("login.html", message="Password failed")
        else:
            return render_template("login.html", message="id failed")
        
        
@app.route('/monitor_influencer', methods=['GET', 'POST'])
def monitor_influencer():
    global admin_logged
    if not admin_logged:
        return render_template('index.html')
    if request.method=='GET':
        influencers=Influencer.query.all()
        return render_template('monitor_influencer.html', influencers=influencers)
    if request.method=='POST':
        id=request.form.get('id')
        inf=Influencer.query.get(id)
        if inf.flagged==1:
            inf.flagged=0
        else: inf.flagged=1
        db.session.commit()
        return redirect(url_for('monitor_influencer'))
    
@app.route('/monitor_sponser', methods=['GET', 'POST'])
def monitor_sponser():
    global admin_logged
    if not admin_logged:
        return render_template('index.html')
    if request.method=='GET':
        sponsers=Sponser.query.all()
        return render_template('monitor_sponser.html', sponsers=sponsers)
    if request.method=='POST':
        id=request.form.get('id')
        inf=Sponser.query.get(id)
        if inf.flagged==1:
            inf.flagged=0
        else: inf.flagged=1
        db.session.commit()
        return redirect(url_for('monitor_sponser'))
    
    
@app.route('/admin_dash', methods=['GET'])
def admin_dash():
    global admin_logged
    if not admin_logged:
        return render_template('index.html')
    ads=Adrequest.query.all()
    dict={}
    for ad in ads:
        if ad.status=='Pending':
            if 'Pending' not in dict.keys():
                dict['Pending']=1
            else: dict['Pending']+=1
        if ad.status=='Rejected':
            if 'Rejected' not in dict.keys():
                dict['Rejected']=1
            else: dict['Rejected']+=1
        if ad.status=='Accepted':
            if 'Accepted' not in dict.keys():
                dict['Accepted']=1
            else: dict['Accepted']+=1
        
    inf=Influencer.query.count()
    sp=Sponser.query.count()
    user={"Influencers":inf, "Sponser":sp}
    camps=Campaign.query.all()
    cats=Category.query.all()
    cat_dict={cat.name:0 for cat in cats}
    current_date = datetime.now().date()
    finished_camp={"Ongoing":0, "Completed":0}
    for camp in camps:
        if camp.enddate>current_date: finished_camp["Ongoing"]+=1
        else: finished_camp["Completed"]+=1
    for camp in camps:
        cat_dict[camp.sponser.category.name]+=1
    
    visibility_camp={"Public":0, "Private":0}
    for camp in camps:
        if camp.visibility=="public": visibility_camp["Public"]+=1
        else: visibility_camp["Private"]+=1
        
    flagged={"Sponsers":0, "Influencers":0}
    unflagged={"Sponsers":0, "Influencers":0}
    sps=Sponser.query.all()
    for sp in sps:
        if sp.flagged==1: flagged["Sponsers"]+=1
        else: unflagged["Sponsers"]+=1
        
    infs=Influencer.query.all()
    for inf in infs:
        if inf.flagged==1: flagged["Influencers"]+=1
        else: unflagged["Influencers"]+=1
        
    return render_template('admin_dash.html',dict=dict, user=user, cat_dict=cat_dict, finished_camp=finished_camp, visibility_camp=visibility_camp, flagged=flagged, unflagged=unflagged)