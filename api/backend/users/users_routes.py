from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from backend.db_connection import db

users = Blueprint('users', __name__)

# retrieves all users in the db
@users.route('/users', methods=['GET'])
def get_users(): 
  try:
    query = '''
    SELECT userId, DOB, gender, email, firstName, lastName 
    FROM Users
    '''

    cursor = db.get_db().get_cursor()
    cursor.execute(query)

    response = make_response(jsonify(cursor.fetchall()))
    response.status_code = 200

    return response
  except Exception as e:
    return jsonify({'error': str(e)}), 500

# for admin use, deactivates a user from the app
@users.route('/users/<userId>', methods=['DELETE'])
def deactivate_user(userId): 
  try: 
    query = '''
    DELETE FROM users WHERE userID = %s
    '''

    cursor = db.get_db().get_cursor()
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

    query = '''
    INSERT INTO FAQs (question, answer) VALUES (%s, %s)
    ''' 

    cursor = db.get_db().get_cursor()
    cursor.execute(query, (question, answer))
    
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

    cursor = db.get_db().get_cursor()
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

    cursor = db.get_db().get_cursor()
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

    cursor = db.get_db().get_cursor()
    cursor.execute(query, (faqId,))

    if cursor.rowcount == 0: # determines how many rows affected
      return jsonify({'message': f'FAQ with id: {faqId} not found'}), 404
    
    db.get_db().commit()
    response = make_response(jsonify({'message': f'FAQ with id: {faqId} successfully deleted'}))
    response.status_code = 200

    return response
  except Exception as e:
    return jsonify({'error': str(e)}), 500