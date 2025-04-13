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
