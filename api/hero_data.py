import json
from bson import ObjectId,json_util
from flask import Blueprint, current_app,request,jsonify
from validation.matches import validate_match

hero_data= Blueprint('hero_data',__name__,url_prefix='/api')



@hero_data.route('/get_heros',methods=['GET'])
def get_heros():
    try:
        db =  current_app.config['Mongo_db']
        heros = db.heros.find_one({'name': 'hero_list'})
        return jsonify({'heros':heros['heros']}),200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

@hero_data.route('/save_match',methods=['POST'])
def save_match():
    try:
        db =  current_app.config['Mongo_db']
        match = request.json
        validate_match(match)
        result = db.matches.insert_one(match)
        if result.inserted_id:
            return jsonify({'msg':'match inserted sucessfully'}),200
        else:
            return jsonify({'error':"Error"}),500
    except (ValueError, TypeError) as ve_te:
        return jsonify({'error': 'Invalid data format: ' + str(ve_te)}), 400
    except Exception as e:
        return jsonify({'error':'An unexpected error occurred'}),500

@hero_data.route('/get_matches',methods=['POST'])
def get_matches():
    try:
        db =  current_app.config['Mongo_db']
        user = request.json
        pipe = [
            {"$match":{"uid":user['uid']}},
            {"$skip":(user['page']-1)*10},
            {"$limit":10}
        ]
        results = list(db.matches.aggregate(pipe))
        data= json.loads(json_util.dumps(results))
        return jsonify({'matches':data}),200
    except Exception as e:
        print(e)
        return jsonify({'error':'An unexpected error occurred'}),500

@hero_data.route('/provide_feedback',methods = ['PUT'])
def provide_feedback():
    try:
        db =  current_app.config['Mongo_db']
        match_data = request.json
        db.matches.find_one_and_update(
            {"_id":ObjectId(match_data['id'])},
            {"$set":{
                "feedback": match_data['feedback']
            }},upsert =False
        )
        return jsonify({'msg':"Feedback added"}),200
    except Exception as e:
         return jsonify({'error':'An unexpected error occurred'}),500
    
@hero_data.route('/delete_match',methods = ['DELETE'])
def delete_match():
    try:
        db = current_app.config['Mongo_db']
        match_data = request.json
        db.matches.delete_one({"_id":ObjectId(match_data['id'])})
        return jsonify({'msg':"Match record deleted"}),200
    except Exception as e:
        return jsonify({'error':'An unexpected error occurred'}),500
