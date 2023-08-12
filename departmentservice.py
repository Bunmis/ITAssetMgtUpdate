from flask import request, redirect, session, flash, url_for
import pyodbc, db
from datetime import date

connectionString = db.GetConnection()
conn = pyodbc.connect(connectionString)
cursor = conn.cursor()

def GetAllDepartments():
    try:
        departments = cursor.execute("SELECT * FROM Department").fetchall()

        return departments
    except:
        return
    

def GetDepartmentById(id):
    try: 
        if id > 0:
            department = cursor.execute("SELECT * FROM Department WHERE ID=?", id).fetchone()

            return department

        return
    except:
        return
    
def SaveDepartment():
    try:
        if request.method=="POST":
            CreatedDate =  date.today()
            #IsActive = 1
            Name = request.form["Name"]
            ID = request.form["ID"]

            if ID == '':
                cursor.execute("""INSERT INTO dbo.Department(Name,CreatedDate) 
                VALUES(?,?)""", Name,CreatedDate)
                conn.commit()
            else:
                cursor.execute("""UPDATE Department SET Name=? WHERE ID=?
                        """, Name,ID)           
                conn.commit()

            return "success"
    except:
        return         

   