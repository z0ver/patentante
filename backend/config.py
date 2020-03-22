import os
#The keys need to be set on the server as environment variable
secret_key = ['SECRET_KEY']
db_host = "localhost"
db_user = os.environ['DB_USER']
db_passwd = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']
db_name = "test"
db_session_timeout = 10