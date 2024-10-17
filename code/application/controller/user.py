from flask import render_template
from flask import current_app as app
from flask import request
from datetime import date
from datetime import datetime
from flask import jsonify
from flask import redirect, url_for
from application.models import *
from sqlalchemy import func
user_logged=None

from flask import render_template
from flask import current_app as app
from flask import request
from datetime import date
from datetime import datetime
from flask import jsonify
from flask import redirect, url_for
from application.models import *
from sqlalchemy import func
user_logged=None
#user login
@app.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    if request.method=="GET":
        return render_template("user_login.html")
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        type=request.form.get("type")
        user=None
        if type=="influencer":
            user=Influencer.query.filter_by(username=username).first()
        elif type=="sponser":
            user=Sponser.query.filter_by(username=username).first()
        if user!=None:
            password_user=user.password
            if password_user==password:
                global user_logged
                user_logged=username
                if user.flagged==1:
                        return render_template('user_login.html', message="you have been flagged")
                if type=="influencer":
                    return redirect(url_for("influencer_dash"))
                elif type=='sponser':
                    return redirect(url_for("sponser_dash")) 
            else:
                return render_template('user_login.html', message="wrong pass")
            
        else:
            return render_template('user_login.html', message='user not present register')

#influencer registration

@app.route('/influencerregister', methods=['GET','POST'])
def influencerregister():
    if request.method=='GET':
        cats=Category.query.all()
        return render_template('register_influencer.html', cats=cats)
    if request.method=='POST':
        name=request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        reach = request.form.get("reach")
        neiche = request.form.get("neiche")
        category_id = request.form.get("category")
        new_in=Influencer(name=name, username=username, password=password, reach=reach, neiche=neiche, category_id=category_id, flagged=False)
        db.session.add(new_in)
        db.session.commit()
        print(new_in.category.name)
        
        return redirect(url_for("userlogin"))

@app.route('/sponserregister', methods=['GET','POST'])
def sponserregister():
    if request.method=='GET':
        cats=Category.query.all()
        return render_template('register_sponser.html',cats=cats)
    if request.method=='POST':
        name=request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        category_id = request.form.get("category")
        new_sp=Sponser(name=name, username=username, password=password, category_id=category_id, flagged=False)
        db.session.add(new_sp)
        db.session.commit()
        return redirect(url_for('userlogin'))
        
@app.route('/sponser_dash', methods=['GET'])
def sponser_dash():
    global user_logged
    if not user_logged:
        return render_template('user_login.html')
    camps=Campaign.query.all()
    current_date = datetime.now().date()
    user=Sponser.query.filter_by(username=user_logged).first()
    return render_template('sponser_dash.html', camps=camps, user=user, current_date=current_date)

@app.route('/create_camp', methods=['GET', 'POST'])
def create_camp():
    global user_logged
    if not user_logged:
        return redirect(url_for('home'))
    if request.method=='GET':
        return render_template('create_camp.html')
    if request.method=='POST':
        name=request.form.get('name')
        description=request.form.get('description')
        start= request.form['startdate']
        end= request.form['enddate']
        startdate = date.fromisoformat(start)
        enddate = date.fromisoformat(end)
        budget=request.form.get('budget')
        visibility=request.form.get('visibility')
        goals=request.form.get('goals')
        sponser_id=Sponser.query.filter_by(username=user_logged).first().id
        new_camp=Campaign(name=name, sponser_id=sponser_id, description=description, startdate=startdate, enddate=enddate, budget=budget, visibility=visibility, goals=goals)
        db.session.add(new_camp)
        db.session.commit()
        
        return redirect(url_for('sponser_dash'))
        
@app.route('/delete_update_camp', methods=['GET','POST'])
def delete_camp():
    global user_logged
    if not user_logged:
        return redirect(url_for('home'))
    if request.method=='GET':
        camps=Campaign.query.all()
        user_id=Sponser.query.filter_by(username=user_logged).first().id
        
        return render_template('delete_camp.html', camps=camps, user_id=user_id)      
    if request.method=='POST':
        camp_id = request.form.get('id')
        camp_del=Campaign.query.get(camp_id)
        for ad in camp_del.ads:
            db.session.delete(ad)
        db.session.delete(camp_del)
        db.session.commit()
        return redirect(url_for('delete_camp'))
        
        
@app.route('/update_camp<int:id>', methods=['GET', 'POST'])
def update_camp(id):
    global user_logged
    if not user_logged:
        return redirect(url_for('userlogin'))
    if request.method=='GET':
        camp=Campaign.query.get(id)
        return render_template('update_camp.html', camp=camp)
    if request.method=='POST':
        name=request.form.get('name')
        description=request.form.get('description')
        start= request.form['startdate']
        end= request.form['enddate']
        startdate = date.fromisoformat(start)
        enddate = date.fromisoformat(end)
        budget=request.form.get('budget')
        visibility=request.form.get('visibility')
        goals=request.form.get('goals')
        
        camp_update=Campaign.query.get(id)
        camp_update.name=name
        camp_update.description=description
        camp_update.startdate=startdate
        camp_update.enddate=enddate
        camp_update.budget=budget
        camp_update.visibility=visibility
        camp_update.goals=goals
        db.session.commit()
        return redirect(url_for('delete_camp'))
        
    
@app.route('/make_request<int:id>', methods=['GET', 'POST'])
def make_request(id):
    global user_logged
    if not user_logged:
        return render_template('index.html')
    if request.method=='GET':
        camps=Sponser.query.filter_by(username=user_logged).first().campaigns
        iname=Influencer.query.get(id).name
        current_date = datetime.now().date()

        return render_template('make_request.html', iname=iname, camps=camps, current_date=current_date)
    if request.method=='POST':
        influencer_id=id
        campaign_id=request.form.get('camp')
        messages=request.form.get('message')
        requirements=request.form.get('requirements')
        payment_amount=request.form.get('payment_amount')
        status='Pending'
        req_sent='sp'
        new_ad=Adrequest(influencer_id=influencer_id, campaign_id=campaign_id, messages=messages, requirements=requirements, payment_amount=payment_amount, status=status, req_sent=req_sent)
        db.session.add(new_ad)
        db.session.commit()
        return redirect(url_for('sponser_dash'))
    
@app.route('/in_sb')
def in_sb():
    return render_template('in_sb.html')  
    
@app.route('/influencer_sb', methods=['GET'])
def influencer_sb():
    global user_logged
    if not user_logged:
        return render_template('index.html')
    category=request.args.get('category')
    min_reach=request.args.get('min_reach')
    max_reach=request.args.get('max_reach')
    if category or min_reach or max_reach:
        query = Influencer.query
        if category:
            cat=Category.query.filter(func.lower(Category.name).ilike(f'%{category.lower()}%')).first()
            if cat:
                category_id=cat.id
                query = query.filter_by(category_id=category_id)
            else: return render_template('browse_influencer.html', influencers=[])

        #query = query.filter(Influencer.category.ilike('category'))
        if min_reach:
            query = query.filter(Influencer.reach >= min_reach)
        if max_reach:
            query = query.filter(Influencer.reach<= max_reach)
        
        influencers = query.all()
        if influencers==[]:
            return render_template('browse_influencer.html', influencers=influencers)
        return render_template('browse_influencer.html', influencers=influencers)
    else:
        influencers=Influencer.query.all()
        return render_template('browse_influencer.html', influencers=influencers)

    
@app.route('/influencer_dash', methods=['GET', 'POST'])
def influencer_dash():
    global user_logged
    if not user_logged:
        return render_template('index.html')
    inf=Influencer.query.filter_by(username=user_logged).first()
    return render_template('influencer_dash.html', inf=inf)


@app.route('/accept_ad_inf<int:id>')
def accept_ad_inf(id):
    ad=Adrequest.query.get(id)
    ad.status="Accepted"
    db.session.commit()
    return redirect(url_for('influencer_dash'))


@app.route('/reject_ad_inf<int:id>')
def reject_ad_inf(id):
    ad=Adrequest.query.get(id)
    ad.status="Rejected"
    db.session.commit()
    return redirect(url_for('influencer_dash'))


@app.route('/negociate<int:id>', methods=['GET', 'POST'])
def negociate(id):
    global user_logged
    if not user_logged:
        return render_template('index.html')
    if request.method=='GET':
        ad=Adrequest.query.get(id)
        return render_template('negociate.html', ad=ad)
    if request.method=='POST':
        id=request.form.get('id')
        payment_amount=request.form.get('amount')
        ad_mod =Adrequest.query.get(id)
        ad_mod.payment_amount=payment_amount
        ad_mod.req_sent='negociate_by_inf'
        db.session.commit()
        return redirect(url_for('influencer_dash'))
    
@app.route('/profile')
def profile():
    global user_logged
    if not user_logged:
        return render_template('index.html')
    inf=Influencer.query.filter_by(username=user_logged).first()
    return render_template('profile.html', inf=inf)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    global user_logged
    if not user_logged:
        return render_template('index.html')
    if request.method=='GET':
        categories=Category.query.all()
        inf=Influencer.query.filter_by(username=user_logged).first()
        return render_template('edit_profile.html', inf=inf, categories=categories)
    if request.method=='POST':
        name=request.form.get('name')
        password=request.form.get('password')
        reach=request.form.get('reach')
        neiche=request.form.get('neiche')
        category_id=request.form.get('category')
        
        
        edit_in=Influencer.query.filter_by(username=user_logged).first()
        edit_in.name=name
        edit_in.password=password
        edit_in.reach=reach
        edit_in.neiche=neiche
        edit_in.category_id=category_id
        db.session.commit()
        return redirect(url_for('profile'))


@app.route('/create_ad', methods=['GET','POST'])
def create_ad():
    global user_logged
    if not user_logged:
        return redirect(url_for('home'))
    if request.method=='GET':
        sp= Sponser.query.filter_by(username=user_logged).first()
        current_date = datetime.now().date()

        return render_template('create_ad.html', sp=sp, current_date=current_date)
    if request.method=='POST':
        campaign_id=request.form.get('camp')
        messages=request.form.get('message')
        requirements=request.form.get('requirements')
        payment_amount=request.form.get('payment_amount')
        ad=Adrequest(campaign_id=campaign_id, messages=messages, requirements=requirements, req_sent='sp', payment_amount=payment_amount)
        db.session.add(ad)
        db.session.commit()
        return redirect(url_for('sponser_dash'))
    
    
@app.route('/update_ad', methods=['GET','POST'])
def update_ad():
    global user_logged
    if not user_logged:
        return render_template('index.html')
    if request.method=='GET':
        id=Sponser.query.filter_by(username=user_logged).first().id
        ads= Adrequest.query.all()
        return render_template('update_ad.html', ads=ads, id=id)
    
    
@app.route('/update_page<int:id>', methods=['GET', 'POST'])
def update_page(id):
    global user_logged
    if not user_logged:
        return redirect(url_for('home'))
    if request.method=='GET':
        sp= Sponser.query.filter_by(username=user_logged).first()
        ad=Adrequest.query.get(id)
        return render_template('update_page.html', ad=ad, sp=sp)
    if request.method=='POST':
        update_ad=Adrequest.query.get(id)
        influencer=request.form.get('influencer')
        in_id=Influencer.query.filter_by(name=influencer).first()
        if in_id:
            update_ad.influencer_id=in_id.id
        else:
            update_ad.influencer_id=None
        messages=request.form.get('message')
        requirements=request.form.get('requirements')
        payment_amount=request.form.get('payment_amount')
        update_ad.messages=messages
        update_ad.requirements=requirements
        update_ad.payment_amount=payment_amount
        update_ad.status='Pending'
        db.session.commit()
        return redirect(url_for('update_ad'))
        

@app.route('/in_sb1<int:ad_id>')
def in_sb1(ad_id):
    print(ad_id)
    return render_template('in_sb1.html', ad_id=ad_id)  


@app.route('/influencer_sb1<int:ad_id>', methods=['GET'])
def influencer_sb1(ad_id):
    global user_logged
    if not user_logged:
        return render_template('index.html')
    category=request.args.get('category')
    min_reach=request.args.get('min_reach')
    max_reach=request.args.get('max_reach')
    ad=Adrequest.query.get(ad_id)
    
    if category or min_reach or max_reach:
        query = Influencer.query
        if category:
            cat=Category.query.filter(func.lower(Category.name).ilike(f'%{category.lower()}%')).first()
            if cat:
                category_id=cat.id
                query = query.filter_by(category_id=category_id)
            else: return render_template('browse_influencer1.html', influencers=[], ad_id=ad_id, ad=ad)

        #query = query.filter(Influencer.category.ilike('category'))
        if min_reach:
            query = query.filter(Influencer.reach >= min_reach)
        if max_reach:
            query = query.filter(Influencer.reach<= max_reach)
        
        influencers = query.all()
        if influencers==[]:
            return render_template('browse_influencer1.html', influencers=influencers, ad_id=ad_id, ad=ad)
        return render_template('browse_influencer1.html', influencers=influencers, ad_id=ad_id, ad=ad)
    else:
        influencers=Influencer.query.all()
        return render_template('browse_influencer1.html', influencers=influencers, ad_id=ad_id, ad=ad)

        
        
@app.route('/update_request/<int:id>/<int:ad_id>', methods=['GET', 'POST'])
def update_request(id, ad_id):
    print(id)
    global user_logged
    if not user_logged:
        return render_template('index.html')
    if request.method=='GET':
        inf=Influencer.query.get(id)
        sp= Sponser.query.filter_by(username=user_logged).first()
        ad=Adrequest.query.get(ad_id)
        return render_template('update_request.html', inf=inf, ad=ad, sp=sp)
    if request.method=='POST':
        update_ad=Adrequest.query.get(ad_id)
        influencer_id=id
        campaign_id=request.form.get('camp')
        messages=request.form.get('message')
        requirements=request.form.get('requirements')
        payment_amount=request.form.get('payment_amount')
        status='Pending'
        req_sent='sp'
        update_ad.influencer_id=influencer_id
        update_ad.messages=messages
        update_ad.requirements=requirements
        update_ad.payment_amount=payment_amount
        update_ad.status=status
        update_ad.req_sent=req_sent
        
        db.session.commit()
        return redirect(url_for('update_ad'))
       
@app.route('/delete_ad<int:id>')
def delete_ad(id):
    ad=Adrequest.query.get(id)
    db.session.delete(ad)
    db.session.commit()
    return redirect(url_for('update_ad'))    

    
    
@app.route('/search_campaign')
def search_campaign():
    
    global user_logged
    if not user_logged:
        return redirect(url_for('home'))
    if request.method=='GET':
        category=request.args.get('category')
        query = Sponser.query
        sps=[]
        if category:
            cat=Category.query.filter(func.lower(Category.name).ilike(f'%{category.lower()}%')).first()
            if cat:
                category_id=cat.id
                query = query.filter_by(category_id=category_id)
                sps=query.all()
        else:
            sps=Sponser.query.all()
        camps=[]
        for sp in sps:
            camps+=sp.campaigns
        current_date = datetime.now().date()

        inf=Influencer.query.filter_by(username=user_logged).first()
        ads=inf.adrequests
        camp_ids=[ad.campaign_id for ad in ads if ad.req_sent=='inf' or (ad.req_sent=='negociate_by_inf' and ad.status=='Pending')]
        print(camp_ids)
        return render_template('search_campaign.html', camps=camps, current_date=current_date, camp_ids=camp_ids)
    
    
@app.route('/camp_sb')
def camp_sb():
    return render_template('camp_sb.html') 



@app.route('/adreq_by_inf<int:camp_id>', methods=['GET', 'POST'])
def adreq_by_inf(camp_id):
    global user_logged
    if not user_logged:
        return redirect(url_for('home'))
    if request.method=='GET':
        camp=Campaign.query.get(camp_id)
        return render_template('adreq_by_inf.html', camp=camp)
    if request.method=='POST':
        influencer_id=Influencer.query.filter_by(username=user_logged).first().id
        campaign_id=request.form.get('id')
        payment_amount=request.form.get('payment_amount')
        status='Pending'
        req_sent='inf'
        ad_req=Adrequest(campaign_id=campaign_id, influencer_id=influencer_id, payment_amount=payment_amount, status=status, req_sent=req_sent)
        db.session.add(ad_req)
        db.session.commit()
        return redirect(url_for('influencer_dash'))
    
    
@app.route('/recieved_ad')
def recieved_ad():
    global user_logged
    if not user_logged:
        return redirect((url_for('home')))
    if request.method=='GET':
        sp=Sponser.query.filter_by(username=user_logged).first()
        camp=sp.campaigns
        ads=[]
        for c in camp:
            ads=ads+c.ads
        req=[ad for ad in ads if ad.req_sent=='negociate_by_inf' or ad.req_sent=='inf']
        print(req)
        return render_template('recieved_ad.html', req=req)
        
@app.route('/accept_ad_sp<int:id>')
def accept_ad_sp(id):
    ad=Adrequest.query.get(id)
    ad.status="Accepted"
    db.session.commit()
    return redirect(url_for('sponser_dash'))


@app.route('/reject_ad_sp<int:id>')
def reject_ad_sp(id):
    ad=Adrequest.query.get(id)
    ad.status="Rejected"
    db.session.commit()
    return redirect(url_for('sponser_dash'))


@app.route('/negociate_sp<int:id>', methods=['GET', 'POST'])
def negociate_sp(id):
    global user_logged
    if not user_logged:
        return render_template('index.html')
    if request.method=='GET':
        ad=Adrequest.query.get(id)
        return render_template('negociate_sp.html', ad=ad)
    if request.method=='POST':
        id=request.form.get('id')
        payment_amount=request.form.get('amount')
        ad_mod =Adrequest.query.get(id)
        ad_mod.payment_amount=payment_amount
        ad_mod.req_sent='negociate_by_sp'
        db.session.commit()
        return redirect(url_for('sponser_dash'))
    


@app.route('/req_sent_inf')
def req_sent_inf():
    global user_logged
    if not user_logged:
        return render_template('index.html')
    inf=Influencer.query.filter_by(username=user_logged).first()
    ads=[]
    print(inf)
   
    adrequests = inf.adrequests
    
   
    for ad in adrequests:
        if ad.req_sent=='inf' or ad.req_sent=='negociate_by_inf':
            ads.append(ad)
    return render_template('req_sent_inf.html', ads=ads)

@app.route('/req_sent_sp')
def req_sent_sp():
    global user_logged
    if not user_logged:
        return render_template('index.html')
    sp=Sponser.query.filter_by(username=user_logged).first()
    ads=[]
    print(sp)
   
    camps=sp.campaigns
    adrequest=[]
    for camp in camps:
        adrequest+=camp.ads
   
    for ad in adrequest:
        if ad.req_sent=='sp' or ad.req_sent=='negociate_by_sp':
            ads.append(ad)
    return render_template('req_sent_sp.html', ads=ads)