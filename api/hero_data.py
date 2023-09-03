from flask import Blueprint, current_app,request,jsonify

hero_data= Blueprint('hero_data',__name__,url_prefix='/api')

@hero_data.route('/get_heros',methods=['GET'])
def get_heros():
    try:
        db =  current_app.config['Mongo_db']

        heros = db.heros.find_one({'name': 'hero_list'})
        return jsonify({'heros':heros['heros']}),200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500
    