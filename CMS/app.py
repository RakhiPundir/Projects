from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import date

today = date.today()

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'rakhi'
app.config['MYSQL_PASSWORD'] = 'Rakhi@!234'
app.config['MYSQL_DB'] = 'Aalekh'

mysql = MySQL(app)

@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	print("Everything right till here..!!")
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		print("Username and password---", username, password)
		cursor = mysql.connection.cursor()
		print(cursor)
		cursor.execute('SELECT * FROM Users WHERE username = %s AND password = %s', (username, password))
		account = cursor.fetchone()
		print(account)
		if account:
			session['loggedin'] = True
			#session['id'] = account['id']
			session['username'] = account[0]
			print(session['username'])
			#login.username = username
			global tb_name
			user = username.split(' ')[0]
			print(user)
			tb_name = user + '_POSTS'

			return redirect(url_for('home'))
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)


@app.route('/home_page')
def home():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor()
		cursor.execute('SELECT * FROM POSTS')
		posts = cursor.fetchall()
		#print(posts)
		return render_template('after-login.html', username=session['username'], posts = posts)
	return redirect(url_for('login'))

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	#session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('index'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'psw-repeat' in request.form:
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		psw = request.form['psw-repeat']
		cursor = mysql.connection.cursor()
		#print(cursor)
		if(password == psw):
			cursor.execute('INSERT INTO Users(username, email, password) VALUES(%s, %s, %s)', (username, email, password,))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
			user = username.split(' ')[0]
			print(user)
			tb_name = user + '_POSTS'
			query = 'CREATE TABLE ' + tb_name + '(Sno INT, Title VARCHAR(255), Author VARCHAR(255), Tags TEXT, Content TEXT, Uploaded_On TEXT);'
			print(query)
			cursor.execute(query)
			sno = 1
			title = 'Welcome Post !!'
			author = 'Admin'
			content = 'Welcome to Aalekh! Thankyou for registration. This is your welcome post'
			tags = 'welcome'
			Uploaded_On = today.strftime("%B %d, %Y")
			query = 'INSERT INTO ' + tb_name + '(Sno, Title, Author, Tags, Content, Uploaded_On) VALUES(%s, %s, %s, %s, %s, %s)'
			print(query)
			cursor.execute(query, (sno, title, author, tags, content, Uploaded_On))
			query = 'ALTER TABLE '+ tb_name + ' CHANGE Sno Sno INT AUTO_INCREMENT PRIMARY KEY;'
			print(query)
			cursor.execute(query)
			cursor.close()
		else:
			msg = 'Passwords do not match..!!!'
		#cursor.execute('SELECT * FROM Users WHERE username = % s', (username))
		#account = cursor.fetchone()
		#if account:
		#	msg = 'Account already exists !'
		#elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
		#	msg = 'Invalid email address !'
		#elif not re.match(r'[A-Za-z0-9]+', username):
		#	msg = 'Username must contain only characters and numbers !'
		#elif not username or not password or not email:
		#	msg = 'Please fill out the form !'
		#else:
		
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

@app.route('/dashboard')
def dashboard():
	cursor = mysql.connection.cursor()
	query = "SELECT * FROM " + tb_name
	resultValue = cursor.execute(query)
	if resultValue > 0:
		userDetails = cursor.fetchall()
		num = len(userDetails)
		return render_template('profile.html', username=session['username'], userDetails = userDetails, num = num)
	
	cursor.close()
	
	return render_template('profile.html', username=session['username'])

@app.route('/post', methods =['GET', 'POST'])
def post():
	msg = ''
	if request.method == 'POST':
		title = request.form['title']
		author = request.form['author']
		content = request.form['content']
		tags = request.form['tags']
		Uploaded_On = today.strftime("%B %d, %Y")
		#sno = 1
		cursor = mysql.connection.cursor()
		query = 'INSERT INTO ' + tb_name +'(Title, Author, Tags, Content, Uploaded_On) VALUES(%s, %s, %s, %s, %s)'
		print(query)
		cursor.execute('INSERT INTO POSTS(Title, Author, Tags, Content, Uploaded_On) VALUES( %s, %s, %s, %s, %s)', (title, author, tags, content, Uploaded_On))
		cursor.execute(query, (title, author, tags, content, Uploaded_On))
		mysql.connection.commit()
		msg = 'Post Successfully Uploaded !'

	return render_template('post.html', msg = msg)

@app.route('/view/<int:sno>')
def view_post(sno):
	print(sno)
	cursor = mysql.connection.cursor()
	post_id = str(sno)
	query = 'SELECT * FROM ' + tb_name + ' WHERE sno = ' + post_id + ';'
	print(query)
	post = cursor.execute(query)
	print(post)
	cursor.close()
	return render_template('view-post.html', post=post)

@app.route('/<int:sno>')
def delete_post(sno):
	print(sno)
	cursor = mysql.connection.cursor()
	post_id = str(sno)
	query = 'DELETE FROM ' + tb_name + ' WHERE sno = ' + post_id + ';'
	print(query)
	post = cursor.execute(query)
	query = 'DELETE FROM POSTS WHERE sno = ' + post_id + ';'
	print(query)
	post = cursor.execute(query)
	mysql.connection.commit()
	cursor.close()
	return redirect(url_for('dashboard'))

if __name__ == '__main__':
	app.run(debug=True)
