from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from datetime import timedelta
import pyodbc
import db

connectionString = db.GetConnection()

conn = pyodbc.connect(connectionString)

cursor = conn.cursor()


def dashboard():
    if 'userId' not in session:
        return render_template("login.html", Title="Login")
    else:
        totalcount = activecount = demagecount = usercount = categorycount = departmentcount=0

        cursor.execute("SELECT * FROM CompanyAsset")
        assetList = cursor.fetchall()
        #for item in assetList:
           # totalcount = count

        cursor.execute("SELECT Count(*) FROM CompanyAsset")
        assetCount = cursor.fetchall()
        for count in assetCount:
            totalcount = count

        cursor.execute("SELECT Count(*) FROM CompanyAsset")
        assetCount = cursor.fetchall()
        for count in assetCount:
            activecount = count       


        cursor.execute("SELECT Count(*) FROM CompanyAsset")
        assetCount = cursor.fetchall()
        for count in assetCount:
            demagecount = count     


        cursor.execute("SELECT Count(*) FROM applicationusers")
        userCount = cursor.fetchall()
        for count in userCount:
            usercount = count     

        cursor.execute("SELECT Count(*) FROM Department")
        departmentCount = cursor.fetchall()
        for count in departmentCount:
            departmentcount = count     

        cursor.execute("SELECT Count(*) FROM Category")
        categoryCount = cursor.fetchall()
        for count in categoryCount:
            categorycount = count     

        return render_template("dashboard.html", userId=session["userId"], AssetCount=totalcount,
        ActiveAssetCount=activecount, DemagedAssetCount=demagecount, UserCount=usercount,
        DepartmentCount=departmentcount, CategoryCount=categorycount, Title="Dashboard")