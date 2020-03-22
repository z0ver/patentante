#!C:/xampp/htdocs/backend/.env/Scripts/python.exe
from wsgiref.handlers import CGIHandler
from app import app
CGIHandler().run(app)