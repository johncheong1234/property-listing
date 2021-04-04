from flask import Flask, render_template, request, redirect, url_for, session
import json
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

import requests

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sell')
def sell():
    return render_template('sell.html')

@app.route('/register', methods=['post', 'get'])
def register():
    email = ''
    name = ''
    password = ''
    person_dict = ''

    if request.method == 'POST':
        email = request.form.get('email')  # access the data inside 
        name = request.form.get('name')
        password = request.form.get('password')

        create_user_url = 'http://127.0.0.1:8001/create'
        
        myobj = {'name': name, 'email': email, 'password': password}
        x = requests.post(create_user_url, json = myobj)

        person_dict = json.loads(x.content)
        
        if (person_dict['message'] != "Successful"):
            return render_template('register.html', message=person_dict['message'])

        else:
            session['name'] = name
            return redirect(url_for('home'))
            
    
    return render_template('register.html')

@app.route('/login', methods=['post','get'])
def login():
    email = ''
    password = ''

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        login_url = 'http://127.0.0.1:8001/login'
        myobj = {'email':email, 'password':password}
        x = requests.post(login_url,json=myobj)

        person_dict = json.loads(x.content)

        if(person_dict['message'] == 'login_successful'):
            session['name'] = person_dict['name']
            return redirect(url_for('home'))
        else:
            return render_template('login.html', message=person_dict['message'])
    
    return render_template('login.html')

app.run(debug=True, port=8000)
