def GetConnection():
    driver = "{ODBC Driver 17 for SQL Server}"  # "{SQL Server Native Client 11.0}" 
    server = "dayo-project-db.database.windows.net"  #"DAYO-PC\SQLEXPRESS" 
    database = "ITAssetDB"
    username = "sa-dayo"
    password = "Password12>"  # "Password@12"
    connectionString ="DRIVER="+ driver +";Server="+ server +";Database="+ database +";UID="+ username +";PWD="+ password
    #connectionString ="Driver="+ driver +";Server="+ server +";Database="+ database +";UID="+ username +";PWD="+ password+";Trusted_Connection=yes"
    #pyodbc.connect('DRIVER={Devart ODBC Driver for SQL Server};Server=myserver;Database=mydatabase;Port=myport;User ID=myuserid;Password=mypassword')
    return connectionString
