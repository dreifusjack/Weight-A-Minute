from flask import Blueprint
from flask import jsonify
from flask import make_response
from backend.db_connection import db

gyms = Blueprint('gyms', __name__)

# Remove the gym with the given id from the db
@gyms.route('/gyms/<gymId>', methods=['DELETE'])
def remove_gym(gymId):
  try:
    query = '''
    DELETE FROM Gyms WHERE gymId = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (gymId,))

    if cursor.rowcount == 0: # determines how many rows affected
      return jsonify({'message': f'Gym with id: {gymId} not found'}), 404
    
    db.get_db().commit()
    response = make_response(jsonify({'message': f'Gym with id: {gymId} successfully deleted'}))
    response.status_code = 200

    return response
  except Exception as e: 
    return jsonify({'error': str(e)}), 500
  
# Retrieve all gyms including the requests equipment name
@gyms.route('/gyms/equipmentAvailableAt/<equipmentId>', methods=['GET'])
def get_equipment_present_gyms(equipmentId):
  try:

    query = '''
    SELECT g.gymId, g.name, g.location, g.type, g.monthlyPrice, g.ownerId
    FROM Gyms g 
      JOIN GymEquipment ge ON g.gymId = ge.gymId
    WHERE ge.equipmentId = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (equipmentId,))
    response = make_response(jsonify(cursor.fetchall()))
    response.status_code = 200
    
    return response 
  except Exception as e: 
    return jsonify({'error': str(e)}), 500

# Get all gym request from the db
@gyms.route('/gymRequests', methods=['GET'])
def get_gym_request():
  try: 
    query = '''
    SELECT requestId, userId, gymDetails, requestDate 
    FROM GymRequests
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)

    response = make_response(jsonify(cursor.fetchall()))
    response.status_code = 200

    return response
  except Exception as e: 
    return jsonify({'error': str(e)}), 500 

