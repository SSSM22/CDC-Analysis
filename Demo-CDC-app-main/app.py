from flask import *
import requests
from bs4 import BeautifulSoup
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '7951'
app.config['MYSQL_DB'] = 'cdc'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
def coderate(chefu):
    url = f"https://www.codechef.com/users/{chefu}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        rank_element = soup.find(class_="rating-data-section problems-solved")
        if rank_element:
            rank = rank_element.get_text().strip().split()
            
            return int(rank[4][1:len(rank[4])-1])
        else:
            return "Ranking not found."
    else:
        return "Unable to connect to CodeChef."


def leetrate(leetu):
    url = f"https://leetcode.com/{leetu}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        rank_element = soup.find(
            class_="text-[24px] font-medium text-label-1 dark:text-dark-label-1")
        if rank_element:
            rank = rank_element.get_text().strip()
            return int(rank)
        else:
            return "Ranking not found."
    else:
        return "Unable to connect to LeetCode."

def get_details():
    cur = mysql.connection.cursor()
    cur.execute(''' call get_det''')
    student = cur.fetchall()
    
    
    cur.close()

    return student

def getDetails_Branch(branch):
    try :
        cur = mysql.connection.cursor()
        cur.callproc('get_branch',[branch])
        student=cur.fetchall()
        #print(student)
        cur.close()
        return student
    except mysql.connection.Error as err:
            return f"Error: {err}" 

@app.route("/details",methods=['POST','GET'])
def main():
    if request.method=="POST":
        roll=request.form.get("roll")
        branch=request.form.get("branch")
        print(branch)
        if branch=="select":
            student=get_details()
            return render_template("students.html",students=student)
        else:
            
            student=getDetails_Branch(branch)
            return render_template("students.html",students=student)

@app.route("/update")
def update():
    try:
        cur = mysql.connection.cursor()
        cur.execute(''' call get_det''')
        student = cur.fetchall()
        cur.close()
        for i in student:
            cur = mysql.connection.cursor()
            roll=i['Roll_Number']
            id=i['CodeChef_CC']
            print(id,END=" ")
            probs=coderate(id)
            print(probs)
            
            cur.callproc('update_codechef',(roll,probs))
            
            cur.close()
        mysql.connection.commit()    
        return "ALL UPDATED"    
    



    except mysql.connection.Error as err:
            return f"Error: {err}" 
@app.route("/")
def index():
    return render_template("index.html")
'''
@app.route('/', methods=['POST', 'GET'])
def check():
    if request.method == 'POST':
        name = request.form['name']
        chefu = request.form['chefu']
        leetu = request.form['leetu']
        chefr = coderate(chefu)
        leetr = leetrate(leetu)
        return render_template('ranking.html', name=name, chefr=chefr, leetr=leetr)
    else:
        return render_template('index.html')


@app.route('/ranking')
def result():
    return render_template('ranking.html')

'''






if __name__ == '__main__':
    app.run(debug=True)
