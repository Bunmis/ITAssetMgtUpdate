from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from datetime import timedelta
import pyodbc, db, assetin, userbk, service, emailin, categoryservice, departmentservice


connectionString = db.GetConnection()

conn = pyodbc.connect(connectionString)

cursor = conn.cursor()

views = Blueprint(__name__, "views")
views.permanent_session_lifetime = timedelta(minutes=5)

@views.route("/")
def home():
    if 'userId' not in session:
        return render_template("login.html", Title="Login")
    else:
        service.BackgroundService()
        return redirect(url_for("views.dashboard"))


@views.route("/logintemplate")
def logintemplate():
    return render_template("logintemplate.html")


@views.route("/dashboard")
def dashboard():
    #run back service
    service.BackgroundDepreciate()
    service.BackgroundService()

    if 'userId' not in session:
        return render_template("login.html", Title="Login")
    else:
        totalcount = activecount = demagecount = usercount = categorycount = departmentcount=0

        cursor.execute("SELECT TOP 5 AssetId, AssetName, AssetModelNo, Price, ManufactureDate, DatePurchase, AssetStatusId FROM CompanyAsset ORDER BY CreatedDate desc")
        assetList = cursor.fetchall()
        #for item in assetList:
           # totalcount = count

        assetCount = cursor.execute("SELECT Count(*) FROM CompanyAsset")
        assetCount = cursor.fetchall()
        for count in assetCount:
            totalcount = count[0]

        cursor.execute("SELECT Count(*) FROM CompanyAsset WHERE AssetStatusId <> 6 AND AssetStatusId <> 7 AND AssetStatusId <> 9")
        assetCount = cursor.fetchall()
        for count in assetCount:
            activecount = count[0]       


        cursor.execute("SELECT Count(*) FROM CompanyAsset WHERE AssetStatusId = 7")
        assetCount = cursor.fetchall()
        for count in assetCount:
            demagecount = count[0]     


        cursor.execute("SELECT Count(*) FROM applicationusers")
        userCount = cursor.fetchall()
        for count in userCount:
            usercount = count[0]     

        cursor.execute("SELECT Count(*) FROM Department")
        departmentCount = cursor.fetchall()
        for count in departmentCount:
            departmentcount = count[0]     

        cursor.execute("SELECT Count(*) FROM Category")
        categoryCount = cursor.fetchall()
        for count in categoryCount:
            categorycount = count[0]     

        return render_template("dashboard.html", userId=session["userId"], AssetList =assetList, AssetCount=totalcount,
        ActiveAssetCount=activecount, DemagedAssetCount=demagecount, UserCount=usercount,
        DepartmentCount=departmentcount, CategoryCount=categorycount, Title="Dashboard")


@views.route("/login", methods=["POST","GET"])
def login():
    responseMsg= ''
    if request.method=="POST":
        session.permanent = True
        email = request.form["username"]
        password = request.form["password"]
        cursor.execute('''SELECT * FROM applicationusers WHERE Email=? AND Password=?''', email, password)
        record = cursor.fetchone()
        if record:
            session["userId"] = record[0]
            session["firstname"]= record[1]
            session["roleid"] = record.RoleId #.strip()
            flash("login success")
            return redirect(url_for("views.dashboard"))
        else:  
            responseMsg ="Username/ password incorrect"
    return render_template("login.html", Title="Login", Message=responseMsg)


@views.route("/logout")
def logout():
    session.pop("userId", None)
    session.pop("firstname", None)
    session.pop("roleid", None)
    return redirect(url_for("views.login"))

@views.route("/forgetpassword", methods=["POST","GET"])
def forgetpassword():
    if request.method=="POST":
        response = userbk.ResetPassword()
        if response == "Ok":
            reciever =  request.form['Username']
            message = "hey, your new password is password. Thank you"
            emailin.SendEmail(reciever, message)
            flash("password reset")
    return render_template("forgetpassword.html", Title="Forget Password")

@views.route("/changepassword")
def changepassword():
    if 'userId' not in session:
        return render_template("login.html", Title="Login")
    else:
        return render_template("changepassword.html", Title="Change Password")


@views.route("/asset", methods=["POST","GET"])
def asset():
        #run back service
    service.BackgroundService()
    service.BackgroundDepreciate()
    if 'userId' not in session:
        return render_template("login.html", Title="Login")
    else:
        oneasset = None
        assets = assetin.GetAllAsset(1)
        response = assetin.PostAsset()
        status = assetin.GetAssetStatus()
        departments = departmentservice.GetAllDepartments()
        categories = categoryservice.GetAllCategories()
        if response == 'success':
            flash(response)
            return redirect(url_for("views.asset"))  
        else: 
            if response != None:
                flash(response) 
            return render_template("asset.html", Title="Asset Managment", assetModel=assets, 
                                   post=oneasset, department=departments, category=categories,
                                   assetstatus=status)

@views.route("/editasset/<int:i>/<int:id>", methods=["POST","GET"])
def editasset(i, id):
    assets = None
    oneasset = None
    if id != None:
        oneasset = cursor.execute("SELECT * FROM CompanyAsset WHERE ID=?", id).fetchone()
        status = assetin.GetAssetStatus()
        departments = departmentservice.GetAllDepartments()
        categories = categoryservice.GetAllCategories()
               
    return render_template("editasset.html", Title="Asset Managment", 
                           page=i, assetModel=assets, post=oneasset, department=departments,
                             category=categories, assetstatus=status)

@views.route("/assetsearch", methods=["POST","GET"])
def assetsearch():
    try:
        if 'userId' not in session:
            return render_template("login.html", Title="Login")
        else:
            oneasset= None
            if request.method=="POST":
                session.permanent = True
                assetname = request.form["AssetName"]
                startdate = request.form["StartDate"]
                enddate = request.form["EndDate"]
                #assets = cursor.execute("SELECT * FROM CompanyAsset WHERE (AssetName=? OR ?='') ", assetname,assetname).fetchall()
                assets = cursor.execute("SELECT * FROM CompanyAsset WHERE (AssetName LIKE ? OR ?='')  and ((CreatedDate BETWEEN ? and ?) OR (? ='' OR ?='')) ", assetname,assetname, startdate, enddate, startdate, enddate).fetchall()
                #assets = cursor.fetchall()
                status = assetin.GetAssetStatus()
                departments = departmentservice.GetAllDepartments()
                categories = categoryservice.GetAllCategories()
                edittype = request.form["edittype"]
                if edittype == "1":
                    
                    return render_template("asset.html", Title="Asset Managment", assetModel=assets,
                                            post=oneasset, department=departments,
                             category=categories, assetstatus=status)
                    #return redirect(url_for("views.asset")) 
                elif edittype == "2":
                    #return redirect(url_for("views.assetdisposal")) 
                    return render_template("assetdisposal.html", Title="Asset Disposal Managment",
                                            assetModel=assets, post=oneasset, department=departments,
                             category=categories, assetstatus=status)
                
                elif edittype == "3":
                    #return redirect(url_for("views.processauthorize")) 
                    return render_template("processauthorize.html", Title="Asset Process Authorize", 
                                           assetModel=assets, post=oneasset, department=departments,
                                           category=categories, assetstatus=status)
    except:
        return redirect(url_for("views.asset"))       

@views.route("/bulk", methods=["POST","GET"])
def bulk():
    if 'userId' not in session:
        return render_template("login.html", Title="Login")
    else:
        oneasset = None
        assets=None
        filePath = assetin.uploadFiles()
        assetin.parseCSV(filePath)
        flash("success")
        return redirect(url_for("views.asset"))
       # return render_template("asset.html", Title="Asset Managment", assetModel=assets, post=oneasset)


@views.route("/assetdisposal")
def assetdisposal():
    if 'userId' not in session:
        return render_template("login.html", Title="Login")
    else:
        assets = assetin.GetAllAsset(2)
        return render_template("assetdisposal.html", Title="Asset Disposal", assetModel=assets)


@views.route("/assetreport", methods=["POST","GET"])
def assetreport():
    if 'userId' not in session:
        return render_template("login.html", Title="Login")
    else:
        assets = assetin.GetAllAsset(1)
        costs = assetin.GetActivityCost()
        activities = assetin.GetActivity()
        return render_template("assetreport.html", assetModel=assets,
                               cost=costs, activity=activities, Title="Asset History")

@views.route("/processauthorize")
def processauthorize():
    if 'userId' not in session:
        return render_template("login.html", Title="Login")
    else:
        assets = assetin.GetAllAsset(3)
        return render_template("processauthorize.html", assetModel=assets, Title="Process Authorize")

@views.route("/user", methods=["POST","GET"])
def user():
    if 'userId' not in session:
        return render_template("login.html", Title="Login")
    else:
        users = userbk.GetUsers()
        response = userbk.PostUser()
        if response == 'success':
            return redirect(url_for("views.user"))
        
        return render_template("user.html", Title="Employee Management", userModel=users)

@views.route("/category", methods=["POST","GET"])
def category():
    if 'userId' not in session:
        return render_template("login.html", Title="Login")
    else:
        categories = categoryservice.GetAllCategories()
        response = categoryservice.SaveCategory()
        if response == 'success':
            return redirect(url_for("views.category"))
        
        return render_template("category.html", Title="Category Management", model=categories)
    
@views.route("/department", methods=["POST","GET"])
def department():
    if 'userId' not in session:
        return render_template("login.html", Title="Login")
    else:
        departments = departmentservice.GetAllDepartments()
        response = departmentservice.SaveDepartment()
        if response == 'success':
            return redirect(url_for("views.department"))
        
        return render_template("department.html", Title="Department Management", model=departments)
    
@views.route("/editother/<int:i>/<int:id>", methods=["POST","GET"])
def editother(i, id):
    try:
        if id != None:
            title = ""
            departments = departmentservice.GetDepartmentById(id)
            categories = categoryservice.GetCategoryById(id)
            if i == 1:
                title = "Edit Department"
            else:
                title = "Edit Category"
        return render_template("editother.html", Title= title, 
                            page=i, department=departments,category=categories)
    except:
        return redirect(url_for("views.login"))
    

