from flask import request, redirect, session, flash, url_for
from datetime import date
import pyodbc, db, os
import pandas as pd
from dateutil.relativedelta import relativedelta
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

connectionString = db.GetConnection()

conn = pyodbc.connect(connectionString)

cursor = conn.cursor()

def GetAssetStatus():
    try:
        status = cursor.execute("SELECT * FROM AssetStatus").fetchall()

        return status
    except:
        return None

def GetAssetStatusById(id):
    try:
        status = cursor.execute("SELECT * FROM AssetStatus WHERE Id=?",id).fetchone()

        return status.Status 
    except:
        return None 
              

def PostAsset():
    if request.method=="POST":
        #serviceDate
        AssetId = request.form["AssetId"]
        AssetModelNo = request.form["AssetModelNo"]
        AssetName = request.form["AssetName"]
        Description = request.form["Description"]
        Price = request.form["Price"]
        ManufactureDate= request.form["ManufactureDate"]
        DatePurchase= request.form["DatePurchase"]
        AssetStatus= request.form["AssetStatus"]
        CategoryId= request.form["CategoryId"]
        DepartmentId= request.form["DepartmentId"]
        Comment= request.form["Comment"]
        isLicenseUpdate= request.form["isLicenseUpdate"]
        LicenseUpdateDate=  date.today() # request.form["LicenseUpdateDate"]
        Warrant= request.form["Warrant"]
        Depreciation= request.form["Depreciation"]
        Service = int(request.form["Service"])
        isAvailable= 1 #request.form["isAvailable"]
        CreatedDate =  date.today()
        #IsActive = 1
        ID = request.form["ID"]
        UserId = request.form["UserId"]
        UserName = request.form["UserName"]
        Cost = request.form["Cost"]

        serviceDate = None

        if(CategoryId == '0' or DepartmentId == '0'):
            return "Catergory/ department cannot be empty"

        if ID == '':
            Url = "/static/files/noimage.png"
            f = request.files['file']
            if f.filename != '':
                #f.save(secure_filename(f.filename))
                filename = secure_filename(f.filename)
                f.save(os.path.join("static/files", filename))
                Url= "/static/files/"+filename

            if Service > 0:
                serviceDate = CreatedDate + relativedelta(months=+Service)

            cursor.execute("""INSERT INTO dbo.CompanyAsset(AssetId,AssetModelNo,AssetName,Description,Price,ManufactureDate,DatePurchase,AssetStatusId,CategoryId,DepartmentId,Comment,isLicenseUpdate,LicenseUpdateDate,Warrant,Depreciation,isAvailable,CreatedDate,Service, ServiceDate,CreatedBy, UrlFile) 
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", AssetId, AssetModelNo,AssetName,Description,Price,ManufactureDate,DatePurchase,AssetStatus,CategoryId,DepartmentId,Comment,isLicenseUpdate,LicenseUpdateDate,Warrant,Depreciation,isAvailable,CreatedDate,Service, serviceDate,UserId, Url)
            conn.commit()
            #Getting id of latest inserted record
            cursor.execute("SELECT @@IDENTITY AS ID;")
            ID = cursor.fetchone()[0]
           # print('Id of inserted record is:{}'.format(cursor.fetchone()[0]))

        else:
            #asset = cursor.execute("SELECT * FROM CompanyAsset WHERE AssetStatusId=? AND ID=? ",6, ID).fetchone()
            asset = cursor.execute("SELECT * FROM CompanyAsset WHERE ID=? ", ID).fetchone()
            if asset:
                if AssetStatus == '':
                    AssetStatus = asset.AssetStatusId
                    if AssetStatus == 9:
                        serviceDate = CreatedDate + relativedelta(months=+Service)

                    cursor.execute("""UPDATE CompanyAsset SET AssetId=?,AssetModelNo=?,AssetName=?,Description=?,Price=?,ManufactureDate=?,
                    DatePurchase=?,AssetStatusId=?,CategoryId=?,DepartmentId=?,Comment=?,isLicenseUpdate=?,LicenseUpdateDate=?,Service=?,
                    Warrant=?,Depreciation=?,isAvailable=?,LastModified=?, ServiceDate=? WHERE ID=?
                    """, AssetId, AssetModelNo,AssetName,Description,Price,ManufactureDate,DatePurchase,AssetStatus,CategoryId,DepartmentId,Comment,isLicenseUpdate,LicenseUpdateDate,Service,Warrant,Depreciation,isAvailable,CreatedDate,serviceDate,ID)
                    conn.commit()
                else:
                    if AssetStatus == '':
                        AssetStatus = asset.AssetStatusId

                    cursor.execute("""UPDATE CompanyAsset SET AssetId=?,AssetModelNo=?,AssetName=?,Description=?,Price=?,ManufactureDate=?,
                    DatePurchase=?,AssetStatusId=?,CategoryId=?,DepartmentId=?,Comment=?,isLicenseUpdate=?,LicenseUpdateDate=?,Service=?,
                    Warrant=?,Depreciation=?,isAvailable=?,LastModified=? WHERE ID=?
                    """, AssetId, AssetModelNo,AssetName,Description,Price,ManufactureDate,DatePurchase,AssetStatus,CategoryId,DepartmentId,Comment,isLicenseUpdate,LicenseUpdateDate,Service,Warrant,Depreciation,isAvailable,CreatedDate,ID)
                    conn.commit()
            else:

                if AssetStatus == '' or AssetStatus == None:
                    AssetStatus = asset.AssetStatusId

                cursor.execute("""UPDATE CompanyAsset SET AssetId=?,AssetModelNo=?,AssetName=?,Description=?,Price=?,ManufactureDate=?,
                    DatePurchase=?,AssetStatusId=?,CategoryId=?,DepartmentId=?,Comment=?,isLicenseUpdate=?,LicenseUpdateDate=?,Service=?,
                    Warrant=?,Depreciation=?,isAvailable=?,LastModified=? WHERE ID=?
                    """, AssetId, AssetModelNo,AssetName,Description,Price,ManufactureDate,DatePurchase,AssetStatus,CategoryId,DepartmentId,Comment,isLicenseUpdate,LicenseUpdateDate,Service,Warrant,Depreciation,isAvailable,CreatedDate,ID)
                conn.commit()


        # insert data into activity table
        # the statu name
        status = GetAssetStatusById(AssetStatus)
        cursor.execute("""INSERT INTO dbo.AssetActivity(AssetId,UserId,UserName,ActivityDescription,DateCreated) 
            VALUES(?,?,?,?,?)""", ID, UserId,UserName,status,CreatedDate)
        conn.commit()

        if AssetStatus == '':
            AssetStatus = asset.AssetStatusId
        #insert into the activity cost table
        if AssetStatus == '9' and float(Cost) > 0.0:
            cursor.execute("""INSERT INTO dbo.AssetActivityCost(AssetId,Cost,ActivityDescription) 
            VALUES(?,?,?)""", ID, Cost,status)
            conn.commit()  

        return "success"
    
        
    


def GetAllAsset(type):
    try:
        if type == 1:
            assets = cursor.execute("SELECT * FROM CompanyAsset").fetchall()
        elif type == 2: 
            assets = cursor.execute("SELECT * FROM CompanyAsset WHERE AssetStatusId='4' OR AssetStatusId='6' OR AssetStatusId='7'").fetchall()
        elif type == 3:
            assets = cursor.execute("SELECT * FROM CompanyAsset WHERE AssetStatusId='6' OR AssetStatusId='7'").fetchall()
        
        return assets
    except:
        return None
def uploadFiles():
    try:
      # get the uploaded file
      file_path = None
      if request.method=="POST":
           uploaded_file = request.files['file']
           if uploaded_file.filename != '':
               file_path = os.path.join("static/files", uploaded_file.filename)
                 # set the file path
               uploaded_file.save(file_path)
               return file_path
          # save the file
    except:
        return None


def parseCSV(filePath):
    try:
        img = "/static/files/noimage.png"
        col_names = ['AssetId','AssetModelNo','AssetName','Description','Price','ManufactureDate','DatePurchase','Service','AssetStatus','CategoryId','DepartmentId','Comment','isLicenseUpdate','LicenseUpdateDate','Warrant','Depreciation','isAvailable']
        # Use Pandas to parse the CSV file
        csvData = pd.read_csv(filePath,names=col_names, skiprows=[0])# header=None)
        # Loop through the Rows
        for i,row in csvData.iterrows():
            cursor.execute("""INSERT INTO dbo.CompanyAsset(AssetId,AssetModelNo,AssetName,Description,Price,ManufactureDate,DatePurchase,Service,AssetStatusId,CategoryId,DepartmentId,Comment,isLicenseUpdate,LicenseUpdateDate,Warrant,Depreciation,isAvailable,CreatedDate,UrlFile) 
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", row['AssetId'],row['AssetModelNo'],row['AssetName'],row['Description'],row['Price'],row['ManufactureDate'],row['DatePurchase'],row['Service'],row['AssetStatus'],row['CategoryId'],row['DepartmentId'],row['Comment'],row['isLicenseUpdate'],row['LicenseUpdateDate'],row['Warrant'],row['Depreciation'],row['isAvailable'],date.today(),img)
            conn.commit()
        return "Success" 
            #print(i,row['AssetId'],row['AssetModelNo'],row['AssetName'],row['Description'],row['Price'],row['ManufactureDate'],row['DatePurchase'],row['AssetStatus'],row['CategoryId'],row['DepartmentId'],row['Comment'],row['isLicenseUpdate'],row['LicenseUpdateDate'],row['Warrant'],row['Depreciation'],row['isAvailable'],row['CreatedDate'],)
    except:
        return "Failed"

def GetActivityByAssetId(assetId):
    try:
        activities = cursor.execute("SELECT * FROM AssetActivity WHERE AssetId=?", assetId).fetchall()
        return activities
    except:
        return None
    
def GetActivityCostByAssetId(assetId):
    try:
        activities = cursor.execute("SELECT * FROM AssetActivityCost WHERE AssetId=?", assetId).fetchall()
        return activities
    except:
        return None


def GetActivity():
    try:
        activities = cursor.execute("SELECT * FROM AssetActivity").fetchall()
        return activities
    except:
        return None
    
def GetActivityCost():
    try:
        activities = cursor.execute("SELECT * FROM AssetActivityCost").fetchall()
        return activities
    except:
        return None
