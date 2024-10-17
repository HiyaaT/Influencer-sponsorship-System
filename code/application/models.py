from flask import current_app as app
from application.database import db
import simplejson as json


class Admin(db.Model):
    __tablename__="admin"
    username=db.Column(db.String, primary_key=True)
    password=db.Column(db.String, nullable=False)
#one influecer can have many adds
  
class Influencer(db.Model):
    __tablename__="influencer"
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String, nullable=False, unique=True)
    name=db.Column(db.String)
    password=db.Column(db.String, nullable=False)
    reach=db.Column(db.Integer, nullable=False)
    neiche=db.Column(db.Enum('Youtube', 'Instagram', 'TickTok', name='types'), nullable=False)
    category_id=db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    adrequests=db.relationship('Adrequest', backref='influencer', lazy=True)
    flagged=db.Column(db.Integer, default=0)
    
class Sponser(db.Model):
    __tablename__="sponser"
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String, nullable=False, unique=True)
    name=db.Column(db.String)
    password=db.Column(db.String, nullable=False)
    category_id=db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    campaigns=db.relationship('Campaign', backref='sponser', lazy=True)
    flagged=db.Column(db.Integer, default=0)

    
#one category can have many influencers /sponsers 
class Category(db.Model):
    __tablename__="category"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, nullable=False)
    influencers=db.relationship('Influencer', backref='category', lazy=True)
    sponsers=db.relationship('Sponser', backref='category', lazy=True)
    
    def to_dict(self):
        return {"id": self.id, "name":self.name}
    
#ONE campaing consist of many ads   
class Campaign(db.Model):
    __tablename__="campaign"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, nullable=False)
    sponser_id=db.Column(db.Integer, db.ForeignKey('sponser.id'), nullable=False)
    description=db.Column(db.Text, nullable=True)
    startdate=db.Column(db.Date, nullable=False)
    enddate=db.Column(db.Date, nullable=False)
    budget=db.Column(db.Numeric, nullable=False)
    visibility=db.Column(db.Enum('public', 'private', name='types'), nullable=False)
    goals=db.Column(db.Text, nullable=True)
    ads=db.relationship('Adrequest', backref='campaign', lazy=True)
    
    def to_dict(self):
        return {"id":self.id, "name": self.name, "sponser_id":self.sponser_id, "description": self.description, "startdate":self.startdate, "enddate":self.enddate, "budget":self.budget, "visibility": self.visibility, "goals":self.goals}
    
class Adrequest(db.Model):
    __tablename__="adrequest"
    id=db.Column(db.Integer, primary_key=True)
    influencer_id=db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=True)
    campaign_id=db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=True)
    messages=db.Column(db.Text, nullable=True)
    requirements=db.Column(db.Text, nullable=True)
    payment_amount=db.Column(db.Numeric, nullable=False)
    status=db.Column(db.Enum('Pending', 'Accepted', 'Rejected', name='types'), nullable=True)
    req_sent=db.Column(db.String)
    
    def to_dict(self):
        return {"id":self.id, "influencer_id":self.influencer_id, "campaign_id":self.campaign_id, "messages":self.messages, "requirements":self.requirements, "payment_amount":self.payment_amount, "status": self.status, "req_sent":self.req_sent}
    
    # wrote below line in app.py
    
