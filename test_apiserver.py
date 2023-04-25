from flask import Flask
from datetime import datetime, date

app = Flask(__name__)

@app.route('/time')
def get_time():
    print('API Server: Getting a time request')
    current_time = datetime.now()
    print("Current time:", current_time)
    return str(current_time)

@app.route('/date')
def get_date():
    print('API Server: Getting a client request')
    current_date = date.today()
    # Print the current date
    print("Current date:", current_date)
    return str(current_date)

@app.route('/hello')
def hello():
    print('API Server: Getting a hello request')
    return 'Hello Omar'

if __name__ == '__main__':
    print('Starting server...')
    app.run()