from app import app, db  # Import the app instance and db from the app module
from app.model import ValuesTable  # Import the ValuesTable model from the app.model module
import uuid  # Import the uuid module
from flask import jsonify  # Import the jsonify function from Flask


"""
This is a Flask route that adds 10 new values to a database table called `ValuesTable`. 
It generates a unique ID for each value using the `uuid` library. 
If the values are added successfully, it returns a JSON response with a success message. 
If there is an error, it returns a JSON response with the error message. 

@return a JSON response with either a success message or an error message.
"""
# Route for adding values
@app.route('/add')
def add_values():
    try:
        for _ in range(0, 10):
            value = ValuesTable(
                id=str(uuid.uuid4())  # Generate a unique ID using uuid.uuid4()
            )
            db.session.add(value)  # Add the value to the session
        db.session.commit()  # Commit the changes to the database
        return jsonify({
            'message': 'Value added successfully'
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        })


"""
This code defines a route `/clean` that cleans up the `ValuesTable` in the database. 
It sets the `current_worker` field to `None`, the `updated_ts` field to `None`, and the `value` field to `0` for all rows in the table. 
If the cleanup is successful, it returns a JSON response with a success message. 
If there is an error, it returns a JSON response with an error message.
"""
# Route for cleaning up values
@app.route('/clean')
def clean():
    try:
        rows = db.session.query(ValuesTable).filter()  # Query all rows from the ValuesTable
        for row in rows:
            row.current_worker = None  # Set the current_worker column to None
            row.updated_ts = None  # Set the updated_ts column to None
            row.value = 0  # Set the value column to 0
        db.session.commit()  # Commit the changes to the database
        return jsonify({
            'message': 'Value cleaned up successfully'
        })
    except Exception as e:
        return jsonify({
            'message': f'Error cleaning up values: {str(e)}'
        })


"""
This is a Flask route that returns a JSON response with a message "pong" when the root URL is accessed.
@return a JSON response with a message "pong"
"""
# Ping route
@app.route('/')
def ping():
    return jsonify({
        'message': 'pong'
    })

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=8081)
