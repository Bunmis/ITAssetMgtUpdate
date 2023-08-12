from flask import request, redirect, session, flash, url_for
import pyodbc, db
from datetime import date

connectionString = db.GetConnection()
conn = pyodbc.connect(connectionString)
cursor = conn.cursor()

def GetAllCategories():
    try:
        categories = cursor.execute("SELECT * FROM Category").fetchall()

        return categories
    except:
        return None
    
def GetCategoryById(id):
    try:
        if id > 0:
            category = cursor.execute("SELECT * FROM Category WHERE ID=?", id).fetchone()

            return category

        return
    except:
        return

def SaveCategory():
    try:
        if request.method=="POST":
            CreatedDate =  date.today()
        # IsActive = 1
            Name = request.form["Name"]
            ID = request.form["ID"]

            if ID == '':
                cursor.execute("""INSERT INTO dbo.Category(Name,CreatedDate) 
                VALUES(?,?)""", Name,CreatedDate)
                conn.commit()
            else:
                cursor.execute("""UPDATE Category SET Name=? WHERE ID=?
                        """, Name,ID)           
                conn.commit()

            return "success"
    except:
        return 
    