from flask import request, redirect, session, flash, url_for
from datetime import date
import pyodbc, db, os
import pandas as pd
import emailin

connectionString = db.GetConnection()

conn = pyodbc.connect(connectionString)

cursor = conn.cursor()


def GetUsers():
    try:
        users = cursor.execute("SELECT * FROM applicationusers").fetchall()
        if len(users) > 0:
            for user in users:
                user.RoleId = user.RoleId  #.strip()
        
        return users
    except:
        return None
    
def PostUser():
    try:
        if request.method=="POST":
            FirstName = request.form["FirstName"]
            LastName = request.form["LastName"]
            RoleId = request.form["RoleId"] 
            Email = request.form["EmailAddress"]
            DateCreated = date.today()
            Id = request.form["Id"]
            if Id.isdigit():
                cursor.execute("""UPDATE applicationusers SET FirstName=?,LastName=?,RoleId=?,Email=? WHERE Id=?""",FirstName, LastName, RoleId, Email,Id)
                conn.commit()
                return "success"

            else:
                record = cursor.execute("SELECT * FROM applicationusers WHERE Email=?",Email).fetchall()
                if len(record) > 0:
                    return "failed"
                else:
                    message = "hey, Your account have been created. Kindly login with your email and use default password as password. Thank you"
                    emailin.SendEmail(Email, message)
                    cursor.execute("""INSERT INTO applicationusers (FirstName, LastName, RoleId, Email, DateCreated,Password)
                        VALUES(?,?,?,?,?,?)""", FirstName, LastName, RoleId.strip(), Email, DateCreated,'password')
                    conn.commit()  
                    return "success"
    except:
        return None

def ResetPassword():
    try:
        email = request.form["Username"]
        password = "password"

        user = cursor.execute("SELECT * FROM applicationusers WHERE Email=?", email).fetchone()
        if user:
            cursor.execute("""UPDATE applicationusers SET Password=? WHERE Email=?""", password, email)
            conn.commit()
            return "Ok"
        else:
            return "Bad"
    except:
        return "Bad"

def GetUserById(userId):
    try:
        user = cursor.execute("SELECT * FROM applicationusers WHERE Id=?", userId).fetchone() 

        return user
    except:
        return None