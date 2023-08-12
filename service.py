from flask import request, redirect, session, flash, url_for
from datetime import date
import pyodbc, db, os
import pandas as pd
import emailin as emailservice
import userbk as userservice

connectionString = db.GetConnection()
conn = pyodbc.connect(connectionString)
cursor = conn.cursor()

def BackgroundService():
    try:
        assets = cursor.execute("SELECT * FROM CompanyAsset WHERE (AssetStatusId <> '10' AND AssetStatusId <> '7' AND AssetStatusId <> '4') AND ServiceDate <=? ", date.today()).fetchall()
        if assets:
            users = userservice.GetUsers()
            for asset in assets:
                cursor.execute("UPDATE CompanyAsset SET AssetStatusId=? WHERE ID=?", "10", asset.ID)
                conn.commit()
                message = "Hey, asset {} is due to service. Thank you".format(asset.AssetName)
                if len(users) > 0:
                    for user in users:
                        user
                        #emailservice.SendEmail(user.Email, message)
    except:
        return 'Error occured'
                   
def BackgroundDepreciate():
    try:
        assets = cursor.execute("SELECT * FROM CompanyAsset WHERE (AssetStatusId <> 7 AND AssetStatusId <> 6) AND DATEADD(year, CAST(Depreciation as int), isnull(cast(CreatedDate as date), getdate()))  <=? ", date.today()).fetchall()
        if assets:
            users = userservice.GetUsers()
            for asset in assets:
                cursor.execute("UPDATE CompanyAsset SET AssetStatusId=? WHERE ID=?", "4", asset.ID)
                conn.commit()
                message = "Hey, asset- {} has got to depreciate cycle in state. Thank you".format(asset.AssetName)
                if len(users) > 0:
                    for user in users:
                        user
                        #emailservice.SendEmail(user.Email, message)           
    except:
        return 'Error occurred'