# Backend
## General
The backend is built using the Python Flask framework. 
The app.py file is the main application and contains all API endpoints.
The db.py file contains all database requests and is intended to be called by the funtions in the app.py

## How to use (recommendation)
1. Download [pycharm](https://www.jetbrains.com/pycharm/) or a tool of your choice and open the folder as python project
2. Install the requirements using `pip install -r requirements.txt`
3. start the app in the app.py file to start your local server (in PyCharm, this is built in when the file is run)

## Configuration
All configuration parameters are set in the config.py file and can be changed there in development.
To have them available on a productive environment, it is intended that their values are taken out of the corresponding environment variables on the server.
