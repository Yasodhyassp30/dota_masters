import os
from flask import Flask,request,jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from api.win_prediction import prediction
from api.counter_picking import picking
from api.user import user
from middleware.auth_validator import jwt_middleware
from pymongo import MongoClient
from api.hero_data import hero_data
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler.re_fit_model import refit_model



load_dotenv()

app = Flask(__name__)
client  = MongoClient(os.getenv('MONGO_URI'))
app.config['Mongo_db'] = client.dota_masters
CORS(app)
app.before_request(jwt_middleware)
app.register_blueprint(prediction)
app.register_blueprint(picking)
app.register_blueprint(hero_data)
app.register_blueprint(user)

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(refit_model, 'cron', month='*/4') 
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True,port=os.getenv('PORT')) 