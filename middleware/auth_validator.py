from flask import Flask, request, jsonify
import os
import jwt 

def jwt_middleware():
    headers = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type' } 
    if request.method == 'OPTIONS' or request.method == 'options': return jsonify(headers), 200
    excluded_routes = ['/api/login', '/api/register']
    if request.path not in excluded_routes:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid JWT token"}), 401

        token = auth_header.split(' ')[1]
        try:
            payload  = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=['HS256'])
            if request.path == '/api/save_match' or request.path == '/api/get_matches':
                request.json['uid'] = payload['id']
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Expired JWT token"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid JWT token"}), 401