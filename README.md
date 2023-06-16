# la_botte
Air Quality Index (AQI) - GDP Dashboard
Welcome to the Air Quality Index (AQI) Dashboard. This Dash application provides an interactive interface for visualizing AQI data from cities around the globe. Our system fetches the data from the World Air Quality Index, processes it, and stores it in a PostgreSQL database. We've also developed a Flask web server for data retrieval and query handling.
In this README, you'll find step-by-step instructions on how to setup and run this application.

Prerequisites
Before you get started, please ensure you have the following installed on your machine:
* Python 3.7 or newer
* pip (Python's package installer)

Setup
Follow these steps to setup the application on your machine:
  1. Clone this repository to your local machine:
  git clone https://github.com/fillobissi/la_botte

  2. Navigate into the directory of the cloned repository:
  cd la_botte
  
  3. Install the required Python packages:
  pip install -r requirements.txt

------------------
FOR database.py

  Configuration
  Before running the scripts, you need to set several environment variables. These are used to configure the connection to the database   and to authenticate with the AQI API. The environment variables you need to set are:
  * DB_HOST: The hostname of your PostgreSQL server. If you're running the server on your own computer, this will be localhost.
  * DB_NAME: The name of your PostgreSQL database.
  * DB_USER: The username for your PostgreSQL database.
  * DB_PASSWORD: The password for your PostgreSQL database.
  * AQI_TOKEN: The token for the AQI API.


  Here's how you can set these environment variables:

  On Linux or macOS, you can use the export command in your terminal:
  * export DB_HOST=your_db_host
  * export DB_NAME=your_db_name
  * export DB_USER=your_db_user
  * export DB_PASSWORD=your_db_password
  * export AQI_TOKEN=your_aqi_token
  
  On Windows, you can use the set command in Command Prompt:
  * set DB_HOST=your_db_host
  * set DB_NAME=your_db_name
  * set DB_USER=your_db_user
  * set DB_PASSWORD=your_db_password
  * set AQI_TOKEN=your_aqi_token
  Replace your_db_host, your_db_name, your_db_user, your_db_password, and your_aqi_token with your actual values.

------------------
FOR flask.py

  Environment Variables
  Before running the application, make sure to set the following environment variables:
  * DB_HOST: The hostname of your PostgreSQL database server. (e.g., localhost)
  * DB_NAME: The name of your PostgreSQL database. (e.g., air_quality)
  * DB_USER: The username to use when connecting to your PostgreSQL database. (e.g., iyad)
  * DB_PASSWORD: The password to use when connecting to your PostgreSQL database.

  You can set these variables in your environment by using the following commands in your terminal:

  For Unix-based systems (like MacOS and Linux):

  export DB_HOST=your_host_here
  export DB_NAME=your_database_name_here
  export DB_USER=your_username_here
  export DB_PASSWORD=your_password_here


  For Windows:

  set DB_HOST=your_host_here
  set DB_NAME=your_database_name_here
  set DB_USER=your_username_here
  set DB_PASSWORD=your_password_here

  Remember to replace your_host_here, your_database_name_here, your_username_here, and your_password_here with your actual PostgreSQL host, database name, username, and password.
  
------------------
FOR dashboard.py
 
Setting up the Mapbox Access Token
Our application leverages Mapbox for certain features. To ensure these features work correctly, you need to have a Mapbox access token. Here's how to set it up:
1. Visit Mapbox, create an account or sign in to your existing account.
2. Navigate to your account dashboard, and either use the default public token or create a new one.
Replace your_actual_token_here with your Mapbox access token.

For Windows Users
Open Command Prompt and run:
set MAPBOX_TOKEN=your_actual_token_here

For Linux/Mac Users
Open a terminal and run:
export MAPBOX_TOKEN=your_actual_token_here

Note: If you're deploying this app, remember to set this environment variable on your server.

Running the App
You're all set! Now, you can run the app with the following command:

python app.py

The app should be running at localhost:8050 or 127.0.0.1:8050 in your web browser.

------------------
License:
This project is licensed under the MIT License.

Acknowledgements:
Created by Iyad Abdi, Filippo Bissi, and Valerio Paoloni. 
This project is a result of the course "Software Engineering for Geoinformatics" 
taken in the Spring semester of 2023 (A.Y. 2022-2023) at Politecnico di Milano 
under Professors Giovanni Quattrocchi & Daniele Oxoli.
 
 
