from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from backend.utils.email_utils import send_email
from backend.db_connection import db

users = Blueprint('users', __name__)

# helper function to get all users 
def fetch_all_users():
    query = '''
    SELECT userId, DOB, gender, email, firstName, lastName 
    FROM Users
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    return cursor.fetchall()

# retrieves all users in the db
@users.route('/users', methods=['GET'])
def get_users(): 
  try:
    users = fetch_all_users()
    response = make_response(jsonify(users))
    response.status_code = 200

    return response
  except Exception as e:
    return jsonify({'error': str(e)}), 500
  
# retrieves a single user by the given id
@users.route('/users/<userId>', methods=['GET'])
def get_single_user(userId):
  try:
    query = '''
    SELECT firstName, lastName, email, gender, DOB 
    FROM Users 
    WHERE userId = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (userId,))
    response = make_response(jsonify(cursor.fetchall()))
    response.status_code = 200
    
    return response 
  except Exception as e:
    return jsonify({'error': str(e)}), 500

@users.route('/trainer/clients/<trainerId>', methods=['Get'])
def get_trainers_clients(trainerId):
  try:
    query = '''
    SELECT *
    FROM Users u JOIN UsersTrainedBy utb ON u.userId = utb.userId
      JOIN Trainers t ON utb.trainerId = t.trainerId
    WHERE t.trainerId = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (trainerId,))
    response = make_response(jsonify(cursor.fetchall()))
    response.status_code = 200
    
    return response 
  except Exception as e:
    return jsonify({'error': str(e)}), 500

# for admin use, sends an email notifcation to all users 
@users.route('/users/notification', methods=['POST'])
def send_notification():
  try:
    data = request.json
    subject = data['subject']
    body = data['body']

    users = fetch_all_users()
    emails = []
    for user in users:
        emails.append(user['email'])
    
    send_email(emails, subject, body)

    return jsonify({'message': 'Notification sent successfully.'}), 200
  except Exception as e:
    return jsonify({'error': {str(e)}}), 500
  
# for admin use, deactivates a user from the app
@users.route('/users/<userId>', methods=['DELETE'])
def deactivate_user(userId): 
  try: 
    query = '''
    DELETE FROM Users WHERE userID = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (userId,))

    if cursor.rowcount == 0: # determines how many rows affected
      return jsonify({'message': f'User with id: {userId} not found'}), 404

    db.get_db().commit()
    response = make_response(jsonify({'message': f'User with id: {userId} successfully deleted'}))
    response.status_code = 200

    return response 
  except Exception as e:
    return jsonify({'error': str(e)}), 500

# creates a FAQ in the db
@users.route('/faqs', methods=['POST'])
def create_faq():
  try:
    data = request.json 
    question = data['question']
    answer = data['answer']

    # auto incr not working :(
    cursor = db.get_db().cursor()
    cursor.execute("SELECT MAX(faqId) as max_id FROM FAQs")
    result = cursor.fetchone()
    
    if result and 'max_id' in result and result['max_id'] is not None:
        new_id = result['max_id'] + 1
    else:
        new_id = 1 

    query = '''
    INSERT INTO FAQs (faqId, question, answer) VALUES (%s, %s, %s)
    ''' 

    cursor.execute(query, (new_id, question, answer))
    
    db.get_db().commit()
    response = make_response(jsonify({'message': f'Successfully created FAQ with question: {question}, answer: {answer}'}))
    response.status_code = 200

    return response 
  except Exception as e:
    return jsonify({'error': str(e)}), 500 


# retrieves all FAQs from the db
@users.route('/faqs', methods=['GET'])
def get_faqs():
  try: 
    query = '''
    SELECT question, answer, faqId, dateUpdated 
    FROM FAQs
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)

    response = make_response(jsonify(cursor.fetchall()))
    response.status_code = 200

    return response
  except Exception as e:
    return jsonify({'error': str(e)}), 500


# updates the given FAQ 
@users.route('/faqs/<faqId>', methods=['PUT'])
def update_faq(faqId):
  try:
    data = request.json
    question = data['question']
    answer = data['answer']

    query = '''
    UPDATE FAQs 
    SET question = %s,
        answer = %s 
    WHERE faqId = %s'''

    cursor = db.get_db().cursor()
    cursor.execute(query, (question, answer, faqId))

    db.get_db().commit()
    response = make_response(jsonify({'message': f'FAQ with id: {faqId} successfully updated'}))
    response.status_code = 200

    return response
  except Exception as e:
    return jsonify({'error': str(e)}), 500
  
# removes the given FAQ from the db
@users.route('/faqs/<faqId>', methods=['DELETE'])
def delete_faq(faqId):
  try:
    query = '''
    DELETE FROM FAQs WHERE faqId = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (faqId,))

    if cursor.rowcount == 0: # determines how many rows affected
      return jsonify({'message': f'FAQ with id: {faqId} not found'}), 404
    
    db.get_db().commit()
    response = make_response(jsonify({'message': f'FAQ with id: {faqId} successfully deleted'}))
    response.status_code = 200

    return response
  except Exception as e:
    return jsonify({'error': str(e)}), 500

# get information for a specific trainer
@users.route('/trainer/<trainerId>', methods=['GET'])
def getTrainerInfo(trainerId):
  try: 
    query = '''
    SELECT *
    FROM Trainers
    WHERE trainerId = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (trainerId,))

    response = make_response(jsonify(cursor.fetchall()))
    response.status_code = 200

    return response
  except Exception as e:
    return jsonify({'error': str(e)}), 500
  
# set information for a specific trainer
@users.route('/trainer/<trainerId>', methods=['PUT'])
def setTrainerInfo(trainerId):
  try: 
    data = request.json
    type = data['type']
    yoe = data['YOE']
    description = data['description']
    query = '''
    UPDATE Trainers
    SET type = %s,
        YOE = %s,
        description = %s
    WHERE trainerId = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (type, yoe, description, trainerId))

    db.get_db().commit()
    response = make_response(jsonify({'message': f'FAQ with id: {faqId} successfully updated'}))
    response.status_code = 200

    return response
  except Exception as e:
    return jsonify({'error': str(e)}), 500
  