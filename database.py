#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import psycopg2
import time
from psycopg2.extras import execute_values
import os

# Define your database connection details
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'air_quality'),
    'user': os.getenv('DB_USER', 'iyad'),
    'password': os.getenv('DB_PASSWORD', 'elmosworld')
}

# Defining API URL for each city and our token 
token = os.getenv('AQI_TOKEN', 'default_token')
urls = {
    'shanghai': f'http://api.waqi.info/feed/shanghai/?token={token}',
    'beijing': f'http://api.waqi.info/feed/beijing/?token={token}',
    'mumbai': f'http://api.waqi.info/feed/mumbai/?token={token}',
    'sao paolo': f'http://api.waqi.info/feed/sao-paolo/?token={token}',
    'shenzhen': f'http://api.waqi.info/feed/shenzhen/?token={token}',
    'tokyo': f'http://api.waqi.info/feed/tokyo/?token={token}',
    'new york': f'http://api.waqi.info/feed/new-york/?token={token}',
    'los angeles': f'http://api.waqi.info/feed/los-angeles/?token={token}',
    'chicago': f'http://api.waqi.info/feed/chicago/?token={token}',
    'london': f'http://api.waqi.info/feed/london/?token={token}',
}

for city, url in urls.items():
    print(city)
    try:
        # Establish the connection
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Fetch data from AQICN API
        response = requests.get(url)  # API URL and your token
        data = response.json()

        # Check if the data is present and in the expected format
        if 'data' not in data:
            raise ValueError("The response doesn't contain 'data'")
        
        # Extract data from the JSON
        aqi = data['data']['aqi']
        timestamp = data['data']['time']['s']
        city_name = data['data']['city']['name']
        city_url = data['data']['city']['url']
        latitude = float(data['data']['city']['geo'][0])
        longitude = float(data['data']['city']['geo'][1])
        pm25 = float(data['data']['iaqi']['pm25']['v'])

        # Insert data into the database
        execute_values(cur, """
            INSERT INTO measurements (aqi, timestamp, city_name, city_url, latitude, longitude, pm25) VALUES %s
        """, [(aqi, timestamp, city_name, city_url, latitude, longitude, pm25)])

         # Commit changes
        conn.commit()
        
        # Print the inserted data
        print(f"Inserted data: {aqi}, {timestamp}, {city_name}, {city_url}, {latitude}, {longitude}, {pm25}")

        # Close the connection
        conn.close()
        
    except (psycopg2.Error, requests.RequestException, ValueError) as e:
        print(f"Error occurred: {e}")
        # Handle the error appropriately
        print('An error occurred while retrieving measurements. Retrying...')
        continue
        
# Wait for a while before fetching data again
time.sleep(60 * 60)  # Wait for one hour

