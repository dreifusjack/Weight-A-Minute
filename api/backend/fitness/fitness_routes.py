from flask import Blueprint, request
from flask import jsonify
from flask import make_response
from backend.db_connection import db

fitness = Blueprint('fitness', __name__)

# routes go here


# create a new workout in db
@fitness.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = request.json
        workout_name = data['name']
        workout_time = data['time']
        times_per_week = data['times_per_week']
        created_by_id = data['created_by_id']

        cursor = db.get_db().cursor()
        cursor.execute("SELECT MAX(workoutId) as max_id FROM Workouts")
        result = cursor.fetchone()
        if result and 'max_id' in result and result['max_id'] is not None:
            new_id = result['max_id'] + 1
        else:
            new_id = 1

        query = '''
                INSERT INTO Workouts (workoutId, name, time, TimesPerWeek, CreatedById)
                    VALUES(%s, %s, %s, %s, %s) 
                '''
        cursor.execute(query, (new_id, workout_name, workout_time, times_per_week, created_by_id))
        db.get_db().commit()

        response = make_response(jsonify({'message': "Successfully added a new workout!"}))
        response.status_code = 200
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# add a completed workout for a user in db
@fitness.route('/completedWorkouts/<userId>', methods=['POST'])
def add_workout(userId):
    try:
        data = request.json
        workout_id = data['workout_id']
        completed_at = data['completed_at']
        notes = data['notes']

        query = '''
                INSERT INTO CompletedWorkouts (workoutId, userId, completedAt, notes)
                    VALUES(%s, %s, %s, %s) 
                '''

        cursor = db.get_db().cursor()
        cursor.execute(query, (workout_id, userId, completed_at, notes))
        db.get_db().commit()

        response = make_response(jsonify({'message': "Successfully added a completed workout!"}))
        response.status_code = 200
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# delete a completed workout for a user in db
@fitness.route('/completedWorkouts/<userId>', methods=['DELETE'])
def delete_workout(userId):
    try:
        data = request.json
        workout_id = data['workout_id']

        query = '''
                DELETE FROM CompletedWorkouts 
                WHERE userId = %s AND workoutId = %s
                '''

        cursor = db.get_db().cursor()
        cursor.execute(query, (userId, workout_id,))

        if cursor.rowcount == 0:
            return jsonify({'message': f'Workout with id: {workout_id} for user: {userId} not found'}), 404

        db.get_db().commit()
        return jsonify({'message': f'Workout with id: {workout_id} for user: {userId} successfully deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
