from flask import Blueprint, request
from flask import jsonify
from flask import make_response
from backend.db_connection import db

community = Blueprint('community', __name__)

# routes go here


# get all blog posts
@community.route('/blogPosts', methods=['GET'])
def get_blog_posts():
    try:
        query = '''
            SELECT postId, content, title, authorId
            FROM BlogPosts
        '''
        cursor = db.get_db().cursor()
        cursor.execute(query)
        return jsonify(cursor.fetchall()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# get records for a specific gym
@community.route('/gyms/<gymId>/records', methods=['GET'])
def get_gym_records(gymId):
    try:
        query = '''
            SELECT r.name, r.userId, r.type, r.weight, r.reps, r.gymId
            FROM Records r 
            WHERE r.gymId = %s
            '''

        cursor = db.get_db().cursor()
        cursor.execute(query, (gymId,))
        response = make_response(jsonify(cursor.fetchall()))
        response.status_code = 200
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@community.route('/gyms/<gymId>/records', methods=['POST'])
def add_record(gymId):
    try:
        data = request.get_json()
        userId = data.get('userId')
        name = data.get('name')
        record_type = data.get('type')
        weight = data.get('weight')
        reps = data.get('reps')

        query = '''
            INSERT INTO Records (userId, name, type, weight, reps, gymId)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''
        cursor = db.get_db().cursor()
        cursor.execute(query, (userId, name, record_type, weight, reps, gymId))
        db.get_db().commit()
        return jsonify(cursor.fetchall()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@community.route('/gyms/<gymId>/records', methods=['DELETE'])
def delete_record(gymId):
    try:
        data = request.get_json()
        userId = data.get('userId')
        name = data.get('name')

        query = '''
            DELETE FROM Records 
            WHERE gymId = %s AND userId = %s AND name = %s
        '''
        cursor = db.get_db().cursor()
        cursor.execute(query, (gymId, userId, name))
        db.get_db().commit()
        return jsonify(cursor.fetchall()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@community.route('/gyms/<gymId>/subscriptions', methods=['GET'])
def get_gym_subscriptions(gymId):
    try:
        query = '''
            SELECT subscriptionId, userId, tier, monthlyFee, length
            FROM Memberships
            WHERE gymId = %s
            '''

        cursor = db.get_db().cursor()
        cursor.execute(query, (gymId,))
        response = make_response(jsonify(cursor.fetchall()))
        response.status_code = 200
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@community.route('/gyms/<gymId>/subscriptions', methods=['DELETE'])
def delete_subscription(gymId):
    try:
        data = request.get_json()
        subscriptionId = data.get('subscriptionId')

        query = '''
            DELETE FROM Memberships
            WHERE gymId = %s AND subscriptionId = %s
        '''
        cursor = db.get_db().cursor()
        cursor.execute(query, (gymId, subscriptionId))
        db.get_db().commit()
        return jsonify(cursor.fetchall()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500