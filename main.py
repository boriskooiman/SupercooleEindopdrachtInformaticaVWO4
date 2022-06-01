from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

conn = sql.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE IF NOT EXISTS students (name TEXT, addr TEXT, city TEXT, pin TEXT, test TEXT)')
print ("Table created successfully")
conn.execute('CREATE TABLE IF NOT EXISTS newtable (int INTEGER, float REAL, text TEXT)')
conn.close()

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def new_student():
   return render_template('student.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         test = request.form['test']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO students (name, addr, city, pin, test) VALUES(?, ?, ?, ?, ?)",(nm,addr,city,pin,test) )

            cur.execute("INSERT INTO newtable (int, float, text) VALUES(?, ?, ?)", (4, 0.2569, 'Hello world'))
           
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from newtable")
   
   rowsNewtable = cur.fetchall();

   cur.execute("select * from students")
   rowsStudents = cur.fetchall();

   return render_template("list.html",rowss = rowsStudents, rowsn = rowsNewtable)

if __name__ == '__main__':
   app.run(debug = True, host = '0.0.0.0', port = 81)