# Patentante
## About
This project is the result of a [hackathon](https://devpost.com/software/pay-now-enjoy-later-n59swk) with the goal to solve issues caused by the 2020 Corona crisis.
The long term description of the project is given on the provided link (German).

The goal of this project is that local shop owners can be supported financially by their customers, even if they had to close their shop.
Our intent is that shops with few digital experience and money can register and provide their offers so customers can buy something and use it later.
The goal for our team is that with this project, customers can become a general sponsor of their local shops and can also support them on the long-term.

## More detailed info
The details to frontend and backend are in a separate README.md in the corresponding folder.

## Setup local dev environment for your improvements
### Backend

1. Install a MySQL database on your machine. One possibility to have this running fast is to download [XAMPP](https://www.apachefriends.org/index.html)
1. Start the mySQL server as well as the ApacheWeb-Server, over the "Admin" button within XAMPP you get to PHPMyAdmin
1. Within PHPMyAdmin create a new Database and import the DatabaseSchema.sql file to setup the database (Import Button)
1. Edit the config.py in the backend folder to match you database settings
1. Download [python 3](https://www.python.org/downloads/)
1. Install and create a virtual pyhton environment with "pip install virtualenv and python3 -m venv env
1. To activate the virtual environment execute the activate.bat file within env/bin/activate
1. Install the requirements using `pip install -r requirements.txt`
1. modify the config values in the config.py file
1. Run the app.py class within the backend directory
1. For testing API calls a good tool is POSTMAN (https://www.postman.com/)
1. For Post Requests choose the setting "raw" and "json" and type your json-statement into the box e.g.
{
	"offerId":"1",
	"profileId":"1",
	"value":20,
	"price":20,
	"status":"ACTIVATE"
}
1. For GET Requests you maybe need to add "Params" e.g. if you want to get all shops with a certain zipcode
#### Use Pycharm to host the Flask app
1. Download [pycharm](https://www.jetbrains.com/pycharm/) or a tool of your choice and open the folder as python project
1. start the app in the app.py file to start your local server (in PyCharm, this is built in when the file is run)

#### Use Apache to host the Flask app
1. if not already done, download [XAMPP](https://www.apachefriends.org/index.html) or an Apache server
1. be sure that the httpd.conf file of the Apache server contains `AddHandler cgi-script .cgi .py`
1. put the path to your local python installation in the first line of the application.cgi file: `#!/path/to/python`

After starting the Flask app, make sure it runs on port 5000 to match the specification of the frontend (or configure the port in /frontend/src/app/service/api.service.ts)

### Frontend
Recommendation for Windows: Download [GIT Bash](https://git-scm.com/downloads)
1. Install [Node.js](https://nodejs.org/en/)
1. Run `npm install @angular/cli -g`
1. In the terminal, navigate to the frontend folder and run `npm i` to install the requirements
1. Run ng serve to start the frontend

At the end of those steps, a frontend should be available that communicates with the backend APIs
