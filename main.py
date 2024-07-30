from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   make_response,
                   flash,
                   session)
from config import conn, cursor
import hashlib
from datetime import datetime
import random
import string
from twilio.rest import Client
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

@app.route('/')
def index():
    if request.cookies:
        action = '/profile'
        username = request.cookies.get('username')

        cursor.execute("SELECT * FROM habbits WHERE username != %s AND partner = %s ORDER BY id DESC", (username, ''))
        all_habbits = cursor.fetchall()
        
        cursor.execute("SELECT active FROM users WHERE username = %s", (username,))
        active_true = cursor.fetchall()[0][0]
        
        cursor.execute("SELECT active FROM users WHERE username = %s", (username,))
        active_text = cursor.fetchall()[0][0]

        cursor.execute("SELECT * FROM habbits WHERE title = %s", (active_text,))
        isHabbit = cursor.fetchall()
        
        if str(isHabbit) == '()':
            cursor.execute("UPDATE users SET active = '' WHERE username = %s", (username,))
            conn.commit()

        return render_template('home.html',
                               action=action,
                               all_habbits=all_habbits,
                            #    title='' if len(all_habbits) > 0 else 'Наразі немає доступних зчичок',
                               active_true=active_true)
    else:
        action = '/login'
        return render_template('index.html', action=action)

@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/log', methods=['POST', 'GET'])
def log():
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')
        md5 = hashlib.md5(password.encode()).hexdigest()

        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, md5,))
        data = cursor.fetchall()

        if len(data) > 0:
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('username', username, max_age=2592000)
            return resp
        else:
            return render_template('login.html', error='Неправильний логін чи пароль')

@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/reg', methods=['POST', 'GET'])
def reg():
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        data = cursor.fetchall()

        if len(data) > 0:
            return render_template('register.html', error='exists')

        if len(username) == 0 or len(password) == 0 or len(password2) == 0:
            return render_template('register.html', error='Введи усі дані')
        elif len(username) < 5 or len(username) > 20:
            return render_template('register.html', error='Ім\'я користувача від 5 до 20 символів')
        elif len(password) < 8 or len(password) > 20:
            return render_template('register.html', error='Пароль від 8 до 20 символів')
        elif password != password2:
            return render_template('register.html', error='Паролі не збігаються')
        else:
            md5 = hashlib.md5(password.encode()).hexdigest()

            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, md5,))
            conn.commit()
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('username', username, max_age=2592000)
            return resp

@app.route('/about')
def about():
    if request.cookies:
        return make_response(redirect(url_for('about')))
    else:
        return make_response(redirect(url_for('login')))

@app.route('/profile')
def profile():
    if request.cookies:
        username=request.cookies.get('username')
        cursor.execute("SELECT active FROM users WHERE username = %s", (username,))
        activeBtn = cursor.fetchall()[0][0]
        
        active = request.args.get('active')

        if active:
            cursor.execute("UPDATE users SET active = %s WHERE username = %s", (active, username))
            conn.commit()

        cursor.execute("SELECT about FROM users WHERE username = %s", (username,))
        about = cursor.fetchall()[0][0]
        
        cursor.execute("SELECT active FROM users WHERE username = %s", (username,))
        active_text = cursor.fetchall()[0][0]

        cursor.execute("SELECT * FROM habbits WHERE title = %s", (active_text))
        mates = cursor.fetchall()

        photo = username[:1].lower()

        cursor.execute("SELECT note FROM users WHERE username = %s", (username))
        note = cursor.fetchall()[0][0]

        return render_template('profile.html', username=request.cookies.get('username'),
                                   about = '<span class="no-about">Ви ще не додали опис</span>' if about == '' else about,
                                   photo=photo,
                                #    habbit='<span class="no-about">Ви ще не вибрали поточну звичку</span>' if active_text == '' else active_text,
                                   habbit=active_text,
                                   btn='вибрати звичку' if activeBtn == '' else 'змінити звичку',
                                   mates=mates,
                                   note=note)
    else:
        return make_response(redirect(url_for('index')))

@app.route('/search', methods=['POST', 'GET'])
def search():
    return render_template('index.html')

@app.route('/new-habbit', methods=['POST', 'GET'])
def newHabbit():
    username = request.cookies.get('username')
    title = request.form.get('title')
    description = request.form.get('description')
    socialMedia = request.form.get('socialMedia')
    city = request.form.get('city')

    current_date = datetime.now()
    date = current_date.strftime('%Y-%m-%d %H:%M:%S')

    id_ = ''.join(random.choices(string.ascii_letters + string.digits, k=5)).lower()

    cursor.execute("INSERT INTO habbits (username, title, description, socialMedia, city, date, id_) VALUES (%s, %s, %s, %s, %s, %s, %s)", (username, title, description, socialMedia, city, date, id_))
    conn.commit()

    cursor.execute("SELECT active FROM users WHERE username = %s", (username,))
    isActive = cursor.fetchall()[0][0]
    
    if isActive == '':
        cursor.execute("UPDATE users SET active = %s WHERE username = %s", (title, username,))
        conn.commit()

    return make_response(redirect(url_for('index')))

@app.route('/settings')
def settings():
    username = request.cookies.get('username')
    cursor.execute("SELECT about FROM users WHERE username = %s", (username,))
    about = cursor.fetchall()[0][0]

    return render_template('settings.html',
                           username=username,
                           about=about)

@app.route('/settings-save', methods=['POST'])
def description():
    description = request.form.get('description')
    username = request.cookies.get('username')
    
    cursor.execute("UPDATE users SET about = %s WHERE username = %s", (description, username))
    conn.commit()

    return make_response(redirect(url_for('profile')))

@app.route('/history')
def history():
    username=request.cookies.get('username')
    page = request.args.get('page')

    cursor.execute("SELECT * FROM habbits WHERE username = %s ORDER BY id DESC", (username,))
    habbits = cursor.fetchall()

    return render_template('history.html',
                           habbits=habbits,
                           page=page)

@app.route('/detailed', methods=['POST', 'GET'])
def detailed():
    username=request.cookies.get('username')
    title = request.args.get('title')

    cursor.execute("SELECT * FROM habbits WHERE title = %s and username = %s", (title, username,))
    habbit = cursor.fetchall()[0]

    date_db = habbit[6]

    date = datetime.strptime(str(date_db), "%Y-%m-%d %H:%M:%S")

    return render_template('detailed.html',
                           habbit=habbit,
                           date=date)

@app.route('/choose', methods=['POST', 'GET'])
def choose():
    username=request.cookies.get('username')

    cursor.execute("SELECT * FROM habbits WHERE username = %s ORDER BY id DESC", (username,))
    habbits = cursor.fetchall()

    return render_template('choose.html',
                           habbits=habbits)

@app.route('/connect', methods=['POST', 'GET'])
def connect():
    username = request.cookies.get('username')
    id_ = request.args.get('id')
    title = request.args.get('title')

    cursor.execute("UPDATE habbits SET partner = %s WHERE id_ = %s", (username, id_))
    cursor.execute("UPDATE users SET active = %s WHERE username = %s", (title, username))
    conn.commit()

    return make_response(redirect(url_for('profile')))

@app.route('/notifications', methods=['POST', 'GET'])
def notifications():
    username=request.cookies.get('username')

    cursor.execute("SELECT * FROM habbits WHERE username = %s ORDER BY id DESC", (username,))
    habbits = cursor.fetchall()

    return render_template('notifications.html',
                           habbits=habbits)

@app.route('/delete', methods=['POST', 'GET'])
def delete():
    username=request.cookies.get('username')
    title = request.args.get('title')
    partner = request.args.get('partner')

    cursor.execute("DELETE FROM habbits where title = %s", (title,))
    cursor.execute("UPDATE users SET active = '' WHERE username = %s", (username,))
    cursor.execute("UPDATE users SET active = '' WHERE username = %s", (partner,))
    conn.commit()

    return make_response(redirect(url_for('profile')))

@app.route('/leave', methods=['POST', 'GET'])
def leave():
    username=request.cookies.get('username')
    title = request.args.get('title')
    # partner = request.args.get('partner')

    cursor.execute("UPDATE users SET active = '' WHERE username = %s", (username,))
    cursor.execute("UPDATE habbits SET partner = '' WHERE title = %s", (title,))
    conn.commit()

    return make_response(redirect(url_for('profile')))

@app.route('/contacts', methods=['POST', 'GET'])
def contacts():
    username=request.cookies.get('username')

    return render_template('contacts.html')

@app.route('/note', methods=['POST', 'GET'])
def note():
    username=request.cookies.get('username')
    note = request.form.get('note')

    cursor.execute("UPDATE users SET note = %s WHERE username = %s", (note, username,))
    conn.commit()

    return make_response(redirect(url_for('profile')))

@app.route('/del', methods=['POST', 'GET'])
def del_():
    username=request.cookies.get('username')
    id_ = request.args.get('id')

    cursor.execute("DELETE FROM habbits WHERE username = %s AND id_ = %s", (username, id_))
    conn.commit()

    return make_response(redirect(url_for('history')))

@app.route('/response', methods=['POST', 'GET'])
def response():

    return render_template('response.html')

@app.route('/resp', methods=['POST', 'GET'])
def resp():
    username = request.cookies.get('username')
    response_ = request.form.get('response')

    cursor.execute("INSERT INTO responses (username, response) VALUES (%s, %s)", (username, response_,))
    conn.commit()

    client = Client(os.getenv('account_sid'), os.getenv('auth_token'))

    message = client.messages.create(
        body=f'{username}\n\n{response_}',
        from_='+13256004952',
        to='+380632480311'
    )

    return make_response(redirect(url_for('thanks')))

@app.route('/thanks', methods=['POST', 'GET'])
def thanks():
    return render_template('thanks.html')

@app.route('/log-out')
def logOut():
    response = make_response(redirect(url_for('index')))

    response.delete_cookie('username')

    return response

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port='8080')
    app.run(debug=True, host= '10.12.36.39')
    # app.run(debug=True, host= '192.168.10.236')