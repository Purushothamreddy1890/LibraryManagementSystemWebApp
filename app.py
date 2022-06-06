from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os


app = Flask(__name__)



# database connection info
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "librarymanagementsystem"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def home():
    return redirect("/index.html")

@app.route("/index.html")
def index():
	return render_template("/index.j2")

@app.route("/students.html", methods= ["GET", "POST"])
def students():
	if request.method == "GET":
		query = "SELECT * FROM Students"
		cur = mysql.connection.cursor()
		cur.execute(query)
		res = cur.fetchall()
		return render_template("/students.j2", results=res)

	if request.method == "POST":
		if request.form.get("add"):
			fname = request.form["fname"]
			lname = request.form["lname"]
			email = request.form["email"]
			ph = request.form["phone_number"]
			addr = request.form["address"]
			query = "INSERT INTO Students (first_name,last_name, email, phone_no, address) VALUES ('%s', '%s', '%s', '%s', '%s')" % (fname, lname, email, ph, addr)
			cur = mysql.connection.cursor()
			a = cur.execute(query)
			mysql.connection.commit()
			return redirect("/students.html")
		if request.form.get("search"):
			id = request.form["student_id"]
			query = "SELECT * FROM Students WHERE student_id = %s" % (id)
			cur = mysql.connection.cursor()
			cur.execute(query)
			res = cur.fetchall()
			return render_template("/students.j2", results=res)
		
@app.route("/update_student/<int:id>", methods=["GET", "POST"])
def update_student(id):
	if request.method == "GET":
		query = "SELECT * FROM Students WHERE student_id = %d" % (id)
		cur = mysql.connection.cursor()
		cur.execute(query)
		res = list(cur.fetchall()[0].values())
		return render_template("/update_student.j2", fname = res[1], lname= res[2], email=res[3], ph=res[4], address = res[5])

	if request.method == "POST":
		if request.form.get("edit_student"):
			fname = request.form["fname"]
			lname = request.form["lname"]
			email = request.form["email"]
			ph = request.form["ph"]
			address = request.form["address"]
			query = "UPDATE Students SET first_name = '%s' , last_name = '%s', email='%s', phone_no='%s', address='%s' WHERE student_id = %d" % (fname,lname,email,ph,address,id)
			cur = mysql.connection.cursor()
			a = cur.execute(query)
			mysql.connection.commit()
		return redirect("/students.html")

@app.route("/delete_student/<int:id>")
def delete_student(id):
	query = "DELETE FROM Students WHERE student_id = %s" % (id)
	cur = mysql.connection.cursor()
	cur.execute(query)
	mysql.connection.commit()
	return redirect("/students.html")

@app.route("/authors.html", methods=["POST", "GET"])
def authors():
	
	if request.method == "GET":
		query = "SELECT * FROM Authors"
		cur = mysql.connection.cursor()
		cur.execute(query)
		res = cur.fetchall()
		return render_template("/authors.j2", results=res)

	if request.method == "POST":
		if request.form.get("add"):
			fname = request.form["fname"]
			lname = request.form["lname"]
			query = "INSERT INTO Authors (author_firstname,author_lastname) VALUES ('%s', '%s')" % (fname, lname)
			cur = mysql.connection.cursor()
			a = cur.execute(query)
			mysql.connection.commit()
		return redirect("/authors.html")

@app.route("/update_author/<int:id>", methods=["GET", "POST"])
def update_author(id):
	if request.method == "GET":
		query = "SELECT * FROM Authors WHERE author_id = %d" % (id)
		cur = mysql.connection.cursor()
		cur.execute(query)
		res = cur.fetchall()
		return render_template("update_author.j2", fname = res[0]["author_firstname"], lname= res[0]["author_lastname"])

	if request.method == "POST":
		if request.form.get("edit_author"):
			fname = request.form["fname"]
			lname = request.form["lname"]
			query = "UPDATE Authors SET author_firstname = '%s' , author_lastname = '%s' WHERE author_id = %d" % (fname,lname,id)
			cur = mysql.connection.cursor()
			a = cur.execute(query)
			mysql.connection.commit()
			
		return redirect("/authors.html")



@app.route("/delete_author/<int:id>")
def delete_author(id):
	query = "DELETE FROM Authors WHERE author_id = %s" % (id)
	cur = mysql.connection.cursor()
	cur.execute(query)
	mysql.connection.commit()
	return redirect("/authors.html")

@app.route("/publishers.html", methods=["POST", "GET"])
def publishers():
	if request.method == "GET":
		query = "SELECT * FROM Publishers"
		cur = mysql.connection.cursor()
		cur.execute(query)
		res = cur.fetchall()
		return render_template("/publishers.j2", results=res)

	if request.method == "POST":
		if request.form.get("add"):
			name = request.form["publisherName"]
			email = request.form["publisherEmail"]
			query = "INSERT INTO Publishers (publisher_name,publisher_email) VALUES ('%s', '%s')" % (name, email)
			cur = mysql.connection.cursor()
			a = cur.execute(query)
			mysql.connection.commit()
		return redirect("/publishers.html")

@app.route("/update_publisher/<int:id>", methods=["GET", "POST"])
def update_publisher(id):
	if request.method == "GET":
		query = "SELECT * FROM Publishers WHERE publisher_id = %d" % (id)
		cur = mysql.connection.cursor()
		cur.execute(query)
		res = list(cur.fetchall()[0].values())
		return render_template("/update_publisher.j2", name = res[1], email= res[2])

	if request.method == "POST":
		if request.form.get("edit_publisher"):
			name = request.form["name"]
			email = request.form["email"]
			query = "UPDATE Publishers SET publisher_name = '%s' , publisher_email = '%s' WHERE publisher_id = %d" % (name,email,id)
			cur = mysql.connection.cursor()
			a = cur.execute(query)
			mysql.connection.commit()
		return redirect("/publishers.html")

@app.route("/delete_publisher/<int:id>")
def delete_publisher(id):
	query = "DELETE FROM Publishers WHERE publisher_id = %s" % (id)
	cur = mysql.connection.cursor()
	cur.execute(query)
	mysql.connection.commit()
	return redirect("/publishers.html")

@app.route("/books.html", methods=["POST", "GET"])
def books():
	if request.method == "GET":
		query = '''SELECT book_id,title,CONCAT(author_firstname," ",author_lastname) AS author_name, 
					publisher_name, price, no_of_copy,genre FROM Books B,Authors A,Publishers P WHERE 
					B.author_id = A.author_id AND B.publisher_id = P.publisher_id'''
		cur = mysql.connection.cursor()
		cur.execute(query)
		res = cur.fetchall()
		return render_template("/books.j2", results=res)

	if request.method == "POST":
		if request.form.get("add"):
			title = request.form["title"]
			author = request.form["author_id"]
			publish = request.form["publisher_id"]
			price = request.form["price"]
			copies = request.form["copies"]
			genre = request.form["genre"]
			 
			query = "INSERT INTO Books (title, author_id, publisher_id, price, no_of_copy, genre) VALUES ('%s', '%s','%s',%s,%s,'%s')" % (title, author, publish,price,copies,genre)
			cur = mysql.connection.cursor()
			a = cur.execute(query)
			mysql.connection.commit()
		return redirect("/books.html")

@app.route("/update_book/<int:id>", methods=["GET", "POST"])
def update_book(id):
	if request.method == "GET":
		query = "SELECT * FROM Books WHERE book_id = %d" % (id)
		cur = mysql.connection.cursor()
		cur.execute(query)
		res = list(cur.fetchall()[0].values())
		return render_template("/update_book.j2", title = res[1], author= res[2], publisher=res[3], price=res[4], copies = res[5], genre= res[6])

	if request.method == "POST":
		if request.form.get("edit_book"):
			title = request.form["title"]
			author = request.form["author"]
			publisher = request.form["publisher"]
			price = request.form["price"]
			copies = request.form["copies"]
			genre = request.form["genre"]
			
			query = "UPDATE Books SET title = '%s' , author_id = %s, publisher_id=%s, price=%s, no_of_copy=%s, genre='%s' WHERE book_id = %d" % (title,author,publisher,price,copies,genre,id)
			cur = mysql.connection.cursor()
			a = cur.execute(query)
			mysql.connection.commit()
		return redirect("/books.html")

@app.route("/delete_book/<int:id>")
def delete_book(id):
	query = "DELETE FROM Books WHERE book_id = %s" % (id)
	cur = mysql.connection.cursor()
	cur.execute(query)
	mysql.connection.commit()
	return redirect("/books.html")

@app.route("/borrowers.html", methods=["GET", "POST"])
def borrowers():
	if request.method == "GET":
		query = '''SELECT borrowing_id,CONCAT(first_name," ",last_name) AS student, 
					title, borrow_date, due_date,due_amount,book_status FROM Books B,Borrow_reports br,Students S WHERE 
					B.book_id = br.book_id AND S.student_id = br.student_id'''
		cur = mysql.connection.cursor()
		cur.execute(query)
		res = cur.fetchall()
		return render_template("/borrowers.j2", results=res)

	if request.method == "POST":
		if request.form.get("add"):
			print("Inserting")
			student = request.form["student"]
			book = request.form["book"]
			borrow = request.form["borrow_date"]
			due_date = request.form["due_date"]
			due = request.form["due_amount"]
			status = request.form["status"]
			 
			query = "INSERT INTO Borrow_reportsx (student_id, book_id, borrow_date, due_date, due_amount, book_status) VALUES (%s, %s,'%s','%s',%s,'%s')" % (student, book, borrow,due_date,due,status)
			cur = mysql.connection.cursor()
			a = cur.execute(query)
			mysql.connection.commit()
		return redirect("/borrowers.html")

@app.route("/update_borrower/<int:id>", methods=["GET", "POST"])
def update_borrower(id):
	if request.method == "GET":
		query = "SELECT * FROM Borrow_reports WHERE borrowing_id = %d" % (id)
		cur = mysql.connection.cursor()
		cur.execute(query)
		res = list(cur.fetchall()[0].values())
		return render_template("/update_borrower.j2", student = res[2], book= res[1], borrow=res[3], due=res[4], amount = res[5])

	if request.method == "POST":
		if request.form.get("edit_borrower"):
			student = request.form["student"]
			book = request.form["book"]
			borrow = request.form["borrow"]
			due = request.form["due"]
			amount = request.form["amount"]
			status = request.form["status"]
			
			query = "UPDATE Borrow_reports SET  student_id = %s, book_id = %s, borrow_date = '%s', due_date='%s', due_amount=%s, book_status='%s' WHERE borrowing_id = %d" % (student,book,borrow,due,amount,status,id)
			cur = mysql.connection.cursor()
			a = cur.execute(query)
			mysql.connection.commit()
		return redirect("/borrowers.html")

@app.route("/delete_borrower/<int:id>")
def delete_borrower(id):
	query = "DELETE FROM Borrow_reports WHERE borrowing_id = %s" % (id)
	cur = mysql.connection.cursor()
	cur.execute(query)
	mysql.connection.commit()
	return redirect("/borrowers.html")

# Listener
# change the port number if deploying on the flip servers
if __name__ == "__main__":
    app.run(port=8904, debug=True)
