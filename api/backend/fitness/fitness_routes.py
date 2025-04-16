from flask import Blueprint, request
from flask import jsonify
from flask import make_response
from backend.db_connection import db

fitness = Blueprint('fitness', __name__)

# routes go here

# create a new workout in db under a specic trainer
@fitness.route('/workouts/createdBy/<trainerId>', methods=['POST'])
def create_workout(trainerId):
    try:
        data = request.json
        workout_name = data['name']
        workout_time = data['time']
        times_per_week = data['times_per_week']

        cursor = db.get_db().cursor()
        cursor.execute("SELECT MAX(workoutId) as max_id FROM Workouts")
        result = cursor.fetchone()
        if result and 'max_id' in result and result['max_id'] is not None:
            new_id = result['max_id'] + 1
        else:
            new_id = 1

        query = '''
                INSERT INTO Workouts (workoutId, name, time, timesPerWeek, CreatedById)
                    VALUES(%s, %s, %s, %s, %s) 
                '''
        cursor.execute(query, (new_id, workout_name, workout_time, times_per_week, trainerId))
        db.get_db().commit()

        response = make_response(jsonify({'message': "Successfully added a new workout!"}))
        response.status_code = 200
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# get all the workouts made by a specific trainer
@fitness.route('/workouts/createdBy/<trainerId>', methods=['GET'])
def get_trainer_workouts(trainerId):
    try:
        query = '''
        SELECT *
        FROM Workouts w
        WHERE w.createdById = %s
        '''
        cursor = db.get_db().cursor()
        cursor.execute(query, (trainerId,))
        response = make_response(jsonify(cursor.fetchall()))
        response.status_code = 200

        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# addes an exercise to a workout witht the given sets and reps
@fitness.route('/workouts/<workoutId>/<exerciseId>', methods=['POST'])
def addExerciseToWorkout(workoutId, exerciseId):
    try:
        data = request.json
        sets = data['sets']
        reps = data['reps']

        query = '''
        INSERT INTO WorkoutExercises (exerciseId, workoutId, reps, sets)
            VALUES(%s, %s, %s, %s) 
        '''

        cursor = db.get_db().cursor()
        cursor.execute(query, (exerciseId, workoutId, reps, sets))

        db.get_db().commit()
        response = make_response(jsonify({'message': f'Exercise with id: {exerciseId} in workout with id {workoutId} successfully added'}))
        response.status_code = 200

        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# edit the sets and reps of an exercise in a workout
@fitness.route('/workouts/<workoutId>/<exerciseId>', methods=['PUT'])
def updateExerciseInWorkout(workoutId, exerciseId):
    try:
        data = request.json
        sets = data['sets']
        reps = data['reps']

        query = '''
        UPDATE WorkoutExercises 
        SET sets = %s,
            reps = %s 
        WHERE workoutId = %s AND exerciseId = %s
        '''

        cursor = db.get_db().cursor()
        cursor.execute(query, (sets, reps, workoutId, exerciseId))

        db.get_db().commit()
        response = make_response(jsonify({'message': f'Exercise with id: {exerciseId} in workout with id {workoutId} successfully updated'}))
        response.status_code = 200

        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# delete an exercise from a workout
@fitness.route('/workouts/<workoutId>/<exerciseId>', methods=['DELETE'])
def deleteExerciseFromWorkout(workoutId, exerciseId):
    try:
        query = '''
                DELETE FROM WorkoutExercises 
                WHERE workoutId = %s AND exerciseId = %s
                '''

        cursor = db.get_db().cursor()
        cursor.execute(query, (workoutId, exerciseId,))

        if cursor.rowcount == 0:
            return jsonify({'message': f'Workout with id: {workoutId} and exerciseId: {exerciseId} not found'}), 404

        db.get_db().commit()
        return jsonify({'message': f'Workout with id: {workoutId} and exerciseId: {exerciseId} successfully deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# get a specific workout
@fitness.route('/workouts/<workoutId>', methods=['GET'])
def get_workout(workoutId):
    try:
        query = '''
        SELECT * 
        FROM Workouts w JOIN WorkoutExercises we ON w.workoutId = we.workoutId
            JOIN Exercises e ON we.exerciseId = e.exerciseId
        WHERE w.workoutId = %s
        '''
        cursor = db.get_db().cursor()
        cursor.execute(query, (workoutId,))
        response = make_response(jsonify(cursor.fetchall()))
        response.status_code = 200

        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# get all the completed workouts for a specific user
@fitness.route('/completedWorkouts/<userId>', methods=['GET'])
def get_user_workouts(userId):
    try:
        query = '''
        SELECT w.workoutId, w.name, cw.completedAt, cw.notes
        FROM Users u NATURAL JOIN CompletedWorkouts cw
            NATURAL JOIN Workouts w 
        WHERE u.userId = %s
        '''

        cursor = db.get_db().cursor()
        cursor.execute(query, (userId,))
        response = make_response(jsonify(cursor.fetchall()))
        response.status_code = 200
        
        return response 
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# get completed workouts from a user in db
@fitness.route('/completedWorkouts/<user_id>', methods=['GET'])
def get_completed_workouts(user_id):
    try:
        query = '''
            SELECT cw.workoutId, cw.completedAt, cw.notes, w.name
            FROM CompletedWorkouts cw
            JOIN Workouts w ON cw.workoutId = w.workoutId
            WHERE cw.userId = %s
            ORDER BY cw.completedAt DESC
        '''

        cursor = db.get_db().cursor()
        cursor.execute(query, (user_id,))
        return jsonify(cursor.fetchall()), 200
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
