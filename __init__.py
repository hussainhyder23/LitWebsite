import os
import gc
from flask import Flask, render_template, url_for, send_file,  redirect, url_for, request, flash, session
import pymysql as psq
from flask_mail import Mail, Message
from threading import Thread

app = Flask(__name__, template_folder='static')
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'noreplycommunicando@gmail.com',
	MAIL_PASSWORD = '##################',
	)

mail = Mail(app)

def async_send_mail(app, msg):
	with app.app_context():
		mail.send(msg)

#msg = Message("TEST EMAIL", sender="noreplycommmunicando@gmail.com", recipients=['noreplycommunicando@gmail.com'])

def connect(): 
	db = psq.connect("localhost", "ccdAdmin", "hello123", "ccd")
	cursor = db.cursor()

	return db, cursor


@app.route('/')
def index():
	#mail.send(msg)
	# return render_template(url_for('static', filename='index.html'))
	return render_template('index.html')


@app.route('/about/')
def about():
    # return render_template(url_for('static', filename='about.html'))
	return render_template('about.html')

@app.route('/events/')
def events():
    # return render_template(url_for('static', filename='events.html'))
	return render_template('events.html')

@app.route('/contact/')
def contact():
    # return render_template(url_for('static', filename='contact.html'))
	return render_template('contact.html')


@app.route('/contact/', methods=['POST'])
def confirmContact():
	if request.method == "POST":
		name = request.form.get("name")
		email = request.form.get("email")
		message = request.form.get("msg")
		secEmail = request.form.get("sec-email")

		if secEmail != "":
			flash("Thank you for contacting us")
			return redirect(url_for('confirmContact'))

		db, cursor = connect()
        	#newMessage = Message(name, email, msg)
		sql = "INSERT INTO messages(name, email, message) \
			VALUES ('%s', '%s', '%s'); " % (name, email, message)
		try:
			cursor.execute(sql)
			db.commit()
			flash('Thank you for contacting us! Give us some time to get back to you.')
		except:  # Exception as e:
        	    # flash(e)
			db.rollback()
			flash('An error has occured. Please try again later or get in touch with us to fix it.')
            		# redirect(url_for('index'))

		msg = Message("Message from website", sender="noreplycommunicando@gmail.com", recipients=['cbitcommunicando@gmail.com'])
		msg.body = "%s has contacted us.\n\nTheir email is : %s\n\nTheir message is: \n%s\n" % (name, email, message)
		Thread(target=async_send_mail, args=(app,msg)).start()

		db.close()
		cursor.close()
		gc.collect()

		return redirect(url_for('confirmContact'))

	else:
		return redirect(url_for('index'))


#@app.route('/download/')
#def download():
#	try:
#		return send_file('/var/www/CCD/communicando/registrations.csv', attachment_filename='registrations.csv')
#	except Exception as e:
#		return str(e)


@app.route('/register/')
def register():
    # return render_template(url_for('static', filename='register.html'))
	return render_template('register.html')


@app.route('/register/', methods=['POST'])
def finishRegistration():
	if request.method =="POST":
		fname = request.form.get("FName")
		lname = request.form.get("LName")
		email = request.form.get("email")
		number = request.form.get("number")
		college = request.form.get("college")
		branch = request.form.get("branch")
		year = request.form.get("year")
		events = request.form.getlist("events")
		events = ", ".join(events)

		db, cursor = connect()
        	#participant = Participant(fname, lname, email, number, college, branch, year, events)
		sql = "INSERT INTO registrations(firstname, lastname, email, phone_no, college, year, branch, events) \
                	VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" % (fname, lname, email, number, college, year, branch, events)

		try:
			cursor.execute(sql)
			db.commit()
			flash('Record was successfully added.')
		except: #  Exception as e:
			db.rollback()
			flash('An error has occured. Please try again later or get in touch with us to fix it.')
			# redirect(url_for('index'))

		sql2 = "SELECT register_id FROM registrations WHERE firstname='%s' AND lastname='%s';" % (fname, lname)

		try:
			cursor.execute(sql2)
			result = cursor.fetchone()
			regnum = result[0]

		except: #  Exception as e:
                        db.rollback()
                        flash('An error has occured. Please try again later or get in touch with us to fix it.')
			redirect(url_for('index'))

		msg = Message("Confirmation Email for Literati 9.0", sender="noreplycommunicando@gmail.com", recipients=[email])
		msg.body = "Welcome, %s\n\nThank you for registering for Literati 9.0. You have applied for %s.\n\nYour registration number is: %s\n\n\nAlso note that the Registration fee for a individual event is Rs.30 per head and Rs.50 per head for a team-based event. For the workshop, the registration fee is Rs.70 per head. The aforementioned amount has to be paid on arrival at the Registration desk.\n\n" % (fname, events, str(regnum))
		msg.html = render_template("mail.html", name=fname, events=events, regnum=regnum)
		Thread(target=async_send_mail, args=(app,msg)).start()

		db.close()
		cursor.close()
		gc.collect()

		return redirect(url_for('finishRegistration'))
	else:
        	return redirect(url_for('index'))


@app.route('/team/')
def team():
	return render_template('team.html')

@app.errorhandler(404)
def handle404(e):
	return "Oops! Looks like this webpage does not exist. Click <a href=\"../\">here</a> to go back."

@app.errorhandler(500)
def handle500(e):
	return "Ooops! something is wrong. Give us sometime to fix this issue. Click here <a href=\"../\">here</a> to go back."

if __name__ == "__main__":
	app.run()
