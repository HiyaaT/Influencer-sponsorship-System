from flask import current_app as app
from application.models import *
from flask import request
from datetime import datetime

@app.route('/api_read_campaigns', methods=['GET'])
def api_read_campaigns():
    return {"data":[campaign.to_dict() for campaign in Campaign.query.all()]}, 200 

@app.route('/api_read_adrequests', methods=['GET'])
def api_read_adrequests():
    return {"data":[adrequest.to_dict() for adrequest in Adrequest.query.all()]}, 200

@app.route('/api_read_categories', methods=['GET'])
def api_read_categories():
    return {"data":[category.to_dict() for category in Category.query.all()]}, 200

@app.route('/api_create_categoty', methods=['POST'])
def api_create_category():
    data=request.get_json()
    name=data['name']
    new_cat=Category(name=name)
    db.session.add(new_cat)
    db.session.commit()
    return {"message":"category creation successful"}, 201
    
    
@app.route('/api_delete_category', methods=['DELETE'])
def api_delete_category():
    data=request.get_json()
    cat_id=int(data['id'])
    cat_del=Category.query.get(cat_id)
    for inf in cat_del.influencers:
        db.session.delete(inf)
    for sp in cat_del.sponsers:
        db.session.delete(sp)
    db.session.delete(cat_del)
    db.session.commit()
    return {"message":"succesful delete"}, 200

@app.route('/api_update_category/<int:id>', methods=['PUT'])
def api_update_category(id):
    data=request.get_json()
    name=data["name"]
    update_cat=Category.query.get(id)
    if not update_cat:
        return {"message":"no such category"}, 404
    update_cat.name=name
    db.session.commit()
    return {"message":"successful"}, 200
    
@app.route('/api_delete_campaign/<int:id>', methods=['DELETE'])
def api_delete_campaign(id):
    camp_del=Campaign.query.get(id)
    for ad in camp_del.ads:
        db.session.delete(ad)
    db.session.delete(camp_del)
    db.session.commit()
    return {"message":"successful"}, 200


@app.route('/api_update_campaign/<int:id>', methods=['PUT'])
def api_update_campaign(id):
    camp_update=Campaign.query.get(id)
    if not camp_update: return {"message":"campaign not found"}, 404
    data=request.get_json()
    name=data['name']
    description=data['description']
    enddate=datetime.strptime(data['enddate'], '%Y-%m-%d')
    budget=data['budget']
    visibility=data['visibility']
    goals=data['goals']
    
    camp_update.name=name
    camp_update.description=description
    camp_update.budget=budget
    camp_update.enddate=enddate
    camp_update.visibility=visibility
    camp_update.goals=goals
    db.session.commit()
    return {"message":"successful"}, 200

@app.route('/api_delete_adrequest/<int:id>', methods=['DELETE'])
def api_delete_adrequest(id):
    del_ad=Adrequest.query.get(id)
    db.session.delete(del_ad)
    db.session.commit()
    return {"message":"success"}, 200

@app.route('/api_update_adrequest/<int:id>', methods=['PUT'])
def api_update_adrequest(id):
    update_ad=Adrequest.query.get(id)
    if not update_ad: return {"message": "no such data"}, 404
    data=request.get_json()
    for key in data:
        if hasattr(update_ad, key):
            setattr(update_ad, key, data[key])
        else: return {"messasge": "attribute not found"}, 404
    db.session.commit()
    return {"message":"successful updation"}


        
    