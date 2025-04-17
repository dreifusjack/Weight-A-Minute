from flask import Blueprint, request
from flask import jsonify
from flask import make_response
from backend.db_connection import db

gyms = Blueprint('gyms', __name__)

# create a gym in db
@gyms.route('/gyms', methods=['POST'])
def create_gym():
  try:
    data = request.json 
    name = data['name']
    location = data['location']
    gym_type = data['gym_type']
    price = data['price']
    owner_id = data['owner_id']

     # auto incr not working :(
    cursor = db.get_db().cursor()
    cursor.execute("SELECT MAX(gymId) as max_id FROM Gyms")
    result = cursor.fetchone()
    
    if result and 'max_id' in result and result['max_id'] is not None:
        new_id = result['max_id'] + 1
    else:
        new_id = 1 

    query = '''
    INSERT INTO Gyms (gymId, name, location, type, monthlyPrice, ownerId) 
        VALUES (%s, %s, %s, %s, %s, %s)
    '''

    cursor.execute(query, (new_id, name, location, gym_type, price, owner_id))
    db.get_db().commit()

    response = make_response(jsonify({'message': f'Successfully created new gym!'}))
    response.status_code = 200

    return response 
  except Exception as e:
    return jsonify({'error': str(e)}), 500 

# Retrieve all gyms from the db
@gyms.route('/gyms', methods=['GET'])
def get_gyms():
  try:
    query = '''
    SELECT gymId, name, location, type, monthlyPrice, ownerId 
    FROM Gyms
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    return jsonify(cursor.fetchall()), 200
  except Exception as e: 
    return jsonify({'error': str(e)}), 500

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

@gyms.route('/gymRequests', methods=['POST'])
def make_gym_request():
  try: 
    data = request.json 
    details = data['details']

    cursor = db.get_db().cursor()
    cursor.execute("SELECT MAX(requestId) as max_id FROM GymRequests")
    result = cursor.fetchone()
    if result and 'max_id' in result and result['max_id'] is not None:
        new_id = result['max_id'] + 1
    else:
        new_id = 1

    query = '''
    INSERT INTO GymRequests (requestId, userId, gymDetails, requestDate)
    VALUES (%s, 5, %s, "4/17/2025")
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (new_id, details))
    db.get_db().commit()

    response = make_response(jsonify(cursor.fetchall()))
    response.status_code = 200

    return response
  except Exception as e: 
    return jsonify({'error': str(e)}), 500 

@gyms.route('/gymRequests/<gymRequestId>', methods=['DELETE'])
def delete_gym_request(gymRequestId):
  try:
    query = '''
    DELETE FROM GymRequests WHERE requestId = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (gymRequestId,))

    if cursor.rowcount == 0: # determines how many rows affected
      return jsonify({'message': f'Gym with id: {gymRequestId} not found'}), 404
    
    db.get_db().commit()
    response = make_response(jsonify({'message': f'Gym with id: {gymRequestId} successfully deleted'}))
    response.status_code = 200

    return response
  except Exception as e: 
    return jsonify({'error': str(e)}), 500

@gyms.route('/exercises', methods=['GET'])
def get_all_exercises():
  try:
    query = '''
    SELECT *
    FROM Exercises
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)

    response = make_response(jsonify(cursor.fetchall()))
    response.status_code = 200

    return response
  except Exception as e: 
    return jsonify({'error': str(e)}), 500 
