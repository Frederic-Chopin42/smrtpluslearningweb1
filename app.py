from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

newitem = []
newpost = []
postcontent = []

app = Flask(__name__, template_folder='templates')
app.secret_key = 'aAwehetfgRGqjgrQHQRJLRJQQQRGrq37'


@app.route('/')
def home():
    if 'isloggedin' in session:
        if session["isloggedin"] == True:
            logout = True
            return render_template('home.html', isloggedout=logout)
        else:
            logout = False
            return render_template('home.html', isloggedout=logout)
    else:
        logout = False
        return render_template('home.html', isloggedout=logout)

@app.route('/posts')
def posts():
    if 'isloggedin' in session:
        if session["isloggedin"] == True:
            logout = True
            return render_template('posts.html', isloggedout=logout, content=newpost)
        else:
            logout = False
            return render_template('login.html', isloggedout=logout)
    else:
        return redirect(url_for('login'))
    
@app.route('/addnewpost', methods=['POST'])
def addpost():
    logout = True
    title = request.form['posttitle']
    posttitle = title
    contentpost = request.form['postcontent']
    postcontent.append(contentpost)
    newpost.append(posttitle)
    global numbertitle
    numbertitle = newpost.index(posttitle)
    return render_template('posts.html', content=newpost, isloggedout=logout)

@app.route('/viewpost')
def viewpost():
    postcontentpost = postcontent[numbertitle]
    logout = True
    return render_template('viewpost.html', content=postcontentpost, isloggedout=logout)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup-action', methods=['POST'])
def signupaction():
    email = request.form['email']
    useridname = email
    password = request.form['pwd']
    connection = sqlite3.connect("smrtpluslearning.db")
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Users WHERE Username = '" + email + "'")
    rowcount = cursor.fetchone()[0]
    if rowcount == 0:
        cursor.execute("INSERT INTO Users VALUES " + "('" + email + "', '" + password + "')")
        connection.commit()
        connection.close()
        return render_template('signupsuccess.html', nameofuser=useridname)
    else:
        return render_template('signupfailure.html')

@app.route('/login-action', methods=['POST'])
def loginaction():
    email = request.form['email']
    useridname = email
    password = request.form['pwd']
    connection = sqlite3.connect("smrtpluslearning.db")
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Users WHERE Username = '" + email + "' AND Pwd = '" + password + "'")
    rowcount = cursor.fetchone()[0]
    connection.close()
    if rowcount > 0:
        session["isloggedin"] = True
        return render_template('loginsuccess.html', nameofuser=useridname)
    else:
        session["isloggedin"] = False
        return render_template('loginfail.html')

@app.route('/terms')
def terms():
    if 'isloggedin' in session:
        if session["isloggedin"] == True:
            logout = True
            return render_template('terms.html', isloggedout=logout)
        else:
            logout = False
            return render_template('terms.html', isloggedout=logout)
    else:
        logout = False
        return render_template('terms.html', isloggedout=logout)

@app.route('/logout')
def logout():
    session["isloggedin"] = False
    return redirect(url_for('home'))

@app.route('/todo')
def todo():
    if 'isloggedin' in session:
        if session["isloggedin"] == True:
            logout = True
            return render_template('todo.html', isloggedout=logout)
        else:
            logout = False
            return render_template('login.html', isloggedout=logout)
    else:
        logout = False
        return render_template('login.html', isloggedout=logout, content=newitem)

@app.route('/addnewitem', methods=['POST'])
def addnewitem():
    logout = True
    content = request.form['itemcontent']
    itemcontent = content
    newitem.append(itemcontent)
    connection = sqlite3.connect("smrtpluslearning.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Todolist VALUES ('" + content + "')")
    connection.close()
    return render_template('todo.html', content=newitem, isloggedout=logout)

@app.route('/viewlist', methods=['POST'])
def viewlist():
    logout = True
    return render_template('todo.html', content=newitem, isloggedout=logout)

@app.route('/deleteitemold')
def deleteitemold():
    newitem.remove(newitem[0])
    return redirect(url_for('todo'))
    
@app.route('/deleteitemnew')
def deleteitemnew():
    newitem.remove(newitem[len(newitem) - 1])
    return redirect(url_for('todo'))

@app.route('/shortcuts')
def shortcuts():
        if 'isloggedin' in session:
            if session["isloggedin"] == True:
                logout = True
                return render_template('shortcuts.html', isloggedout=logout)
            else:
                logout = False
                return render_template('shortcuts.html', isloggedout=logout)
        else:
            logout = False
            return render_template('shortcuts.html', isloggedout=logout)

if __name__ == '__main__':
    app.run(debug=True)