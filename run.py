from flask import Flask , render_template , url_for , request , redirect
import sqlite3 as sql
from flask_mail import Mail, Message
app = Flask(__name__)
mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'youremailID@gmail.com'
app.config['MAIL_PASSWORD'] = 'yourPassword'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



@app.route("/")
@app.route("/home")
def home():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("select * from products")
   rows = cur.fetchall(); 
   return render_template("home.html" , rows = rows , pro='')

@app.route('/newproduct')
def new_student():
   return render_template('newproduct.html')


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         name = request.form['name']
         content = request.form['content']
         price = request.form['price']
         weight = request.form['weight']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO products(name,content,price,weight) VALUES (?,?,?,?)",(name,content,price,weight))
            con.commit()
            # print("hurra")
            # msg = "Record successfully added"
      except:
         con.rollback()
         # print("hmuhhhaaa")
         # msg = "error in insert operation"
      
      finally:
         return redirect(url_for('home'))
         con.close()

@app.route("/list", methods=['POST'])
def list():
    text = request.form['text']
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from products where name like ?", ('%'+text+'%',))
    rows = cur.fetchall();
    return render_template('home.html' , pro = text ,rows=rows)

@app.route("/sendemail", methods=['POST'])
def sendemail():
    if request.method == "POST":
        selected = request.form.getlist("checkboxes")
    l = selected
    text = request.form['text']
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    rows = []
    for i in l:
        cur.execute("select * from products where name like ?", ('%'+i+'%',))
        row = cur.fetchone();
        rows.append("name = "+row["name"]+", content = "+ row["content"]+", price = " + row["price"]+", weigth = " + row["weight"])
    msg = Message('Data from Flask - app', sender = 'youremailID@gmail.com', recipients = [text])
    str1 = ''.join(rows)
    msg.body = str1
    mail.send(msg)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True) 