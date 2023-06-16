#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, jsonify
import psycopg2
import pickle
import os  # Import os module

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

# Define your database connection details
db_config = {
    'host': os.getenv('DB_HOST'),  # Get value from environment variable
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

@app.route('/')
def get_data():
    with open('data.pkl', 'rb') as f:
        data = pickle.load(f)
    return jsonify(data)

@app.route('/measurements')
def get_measurements():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM measurements")
        rows = cursor.fetchall()
        measurements = []
        for row in rows:
            measurement = {
                'id': row[0],
                'aqi': row[1],
                'timestamp': row[2],
                'city_name': row[3],
                'city_url': row[4],
                'latitude': row[5],
                'longitude': row[6],
                'pm25': row[7]
            }
            measurements.append(measurement)
        return jsonify(measurements)
    except Exception as e:
        return 'An error occurred while processing measurements.', 500
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    app.run(port=5001)

