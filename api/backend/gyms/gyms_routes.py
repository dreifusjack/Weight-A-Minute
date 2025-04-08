from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from backend.db_connection import db

gyms = Blueprint('gyms', __name__)

# routes go here

# route to get all gym requests 
@gyms.route('/gymRequests', methods=['GET'])
def get_gym_request():
  try: 
    query = '''
    SELECT userId, gymDetails, requestDate 
    FROM GymRequests
    '''

    cursor = db.get_db().get_cursor()
    cursor.execute(query)

    response = make_response(jsonify(cursor.fetchall()))
    response.status_code = 200

    return response
  except Exception as e: 
    return jsonify({'error': str(e)}), 500 

