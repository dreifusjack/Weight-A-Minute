from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from backend.db_connection import db

gyms = Blueprint('gyms', __name__)

# routes go here

# Remove the gym with the given id from the db
@gyms.route('/gyms/<gymId>', methods=['DELETE'])
def remove_gym(gymId):
  try:
    query = '''
    DELETE FROM Gyms WHERE gymId = %s
    '''

    cursor = db.get_db().get_cursor()
    cursor.execute(query, (gymId,))

    if cursor.rowcount == 0: 
      return jsonify({'message': f'Gym with id: {gymId} not found'}), 404
    
    db.get_db().commit()
    response = make_response({'message': f'Gym with id: {gymId} successfully deleted'})
    response.status_code = 200

    return response
  except Exception as e: 
    return jsonify({'error': str(e)}), 500

# Get all gym request from the db
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

