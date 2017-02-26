import datetime
import MySQLdb as my


db = my.connect("130.211.157.189","root","root","kendb" )
cursor = db.cursor()
sqlSelectAllLaws="""select * from LAWS"""
cursor.execute(sqlSelectAllLaws)
# Get ALL LAWS
allLaws = cursor.fetchall()
for eachLaw in allLaws:
    categoryName=eachLaw[8]
    agencyName=eachLaw[9]
    # Get IDS from Lookup Table for Catgeory and Agency
    sqlCategoryID = """select ID from CATEGORIES where CATEGORIES_VALUE='%s'"""%(categoryName)
    sqlAgencyID = """select ID from AGENCIES where AGENCIES_VALUE='%s'""" %(agencyName)
    cursor.execute(sqlCategoryID)
    categoryID=cursor.fetchone()
    cursor.execute(sqlAgencyID)
    agencyID = cursor.fetchone()
    if(categoryID is not None):
        categoryID=categoryID[0]
    else:categoryID=-1
    if (agencyID is not None):
        agencyID = agencyID[0]
    else:agencyID=-1
    # Get ALL LAWS
    allLaws = cursor.fetchall()
    # Get ditinct field and value from Laws KDB table for agencyID and categoryID
    sqlSelectFieldFieldValueFromKDB = """select distinct field, value from LAWS_KDB WHERE categoryid=%d or agenciesid=%d""" % (categoryID,agencyID)
    #print(sqlSelectFieldFieldValueFromKDB)
    cursor.execute(sqlSelectFieldFieldValueFromKDB)
    fieldFieldValueList = cursor.fetchall()
    column={"professional":0,"bachelor":0,"civil_status":0, "parent":0,"age_range":0 }
    colVal = []
    for row in fieldFieldValueList:
       # print row[0],"value    ",row[1]
        #colVal.append(row[1])
        if(row[0]=="professional"):
            column["professional"]=row[1]
        elif(row[0]=="bachelor"):
            column["bachelor"] = row[1]
        elif (row[0] == "civil_status"):
            column["civil_status"] = row[1]
        elif (row[0] == "parent"):
            column["parent"] = row[1]
        elif (row[0] == "age_range"):
            column["age_range"] = row[1]
    sqlInsertLawVector = """Insert into LAWS_VECTOR(federal,location_state,location_county,profesional,nationality,civil_status,bachelor,parent,age_range,lawId)
     VALUES(%d,%d,%d,%d,%d,%d,%d,%d,%d,%d) """%(1,1,1, column["professional"],1,column["civil_status"],column["bachelor"], column["parent"],column["age_range"],eachLaw[0])
    cursor.execute(sqlInsertLawVector)
    db.commit()
    print(column)
