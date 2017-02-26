import datetime
import MySQLdb as my
db = my.connect("130.211.157.189","root","root","kendb" )
cursor = db.cursor()
sqlSelectAllPersonids="""select personid from PERSONS"""
cursor.execute(sqlSelectAllPersonids)
personIDs = cursor.fetchall()
for eachPersonid in personIDs:
    sqlSelectFromPersons = """select * from PERSONS where personid=%d""" %(eachPersonid)
    # Execute the SQL command
    cursor.execute(sqlSelectFromPersons)
    personsResult=cursor.fetchone()
    # Get stateID
    def getUserStateID():
        stateName=personsResult[5].strip()
        # Get stateID from State
        sqlSelectFromStateLkUp="""select STATE_ID from STATES where STATE='%s'"""%(stateName)
        cursor.execute(sqlSelectFromStateLkUp)
        stateID = cursor.fetchone()[0]
        # print(stateID)
        return stateID
    # Get Professional
    def getProfessional():
        professional=personsResult[13].strip()
        # print(professional)
        return professional
    # Get Nationality
    def getNationality():
        homeTownState=personsResult[14].strip()
        sqlSelectCountHomeState = """select COUNT(*) from STATES where UPPER(STATE)='%s'""" % (homeTownState.upper())
        cursor.execute(sqlSelectCountHomeState)
        countHomeState = cursor.fetchone()[0]
        # print(countHomeState)
        if(countHomeState==0):
            return 0
        else: return 1
    # Get civilStatusID
    def getCivilStatusID():
        civilStatus=personsResult[10].strip()
        sqlSelectFromCivilStatusLkUp = """select ID from CIVIL_STATUS where UPPER(STATUS)='%s'""" % (civilStatus.upper())
        cursor.execute(sqlSelectFromCivilStatusLkUp)
        civilStatusID = cursor.fetchone()[0]
        # print(civilStatusID)
        return civilStatusID
    # Get Bachelor
    def getBachelor():
        education = personsResult[7].strip()
        if(education.upper()=="COLLEGE"):
            bachelor=1
        elif(education.upper()=="HIGH SCHOOL"):
            bachelor=0
        # print(bachelor)
        return bachelor
    # Get Parent
    def getParent():
        kids=personsResult[11].strip()
        if(kids>0):
            parent=1
        else: parent=0
        #print(parent)
        return parent
    # Get ageRangeID
    def getAgeRange():
        dob=personsResult[3].strip()
        dobYear=int(dob[6:])
        currentYear=int(datetime.date.today().strftime("%Y"))
        age=currentYear-dobYear
        sqlSelectAgeRangeID = """select ID from AGE_RANGE where LOWER_AGE<=%d AND UPPER_AGE>=%d""" % (age,age)
        cursor.execute(sqlSelectAgeRangeID)
        ageRangeID = cursor.fetchone()[0]
        # print(ageRangeID)
        return ageRangeID
    personID=personsResult[0]
    federal=1
    locationState=getUserStateID()
    locationCounty=1
    professional=int(getProfessional())
    nationality=int(getNationality())
    civilStatusID=int(getCivilStatusID())
    bachelor=int(getBachelor())
    parent=int(getParent())
    age_range=getAgeRange()

    # countRecordinPersonVector
    sqlSelectPersonVector="""select COUNT(*) from PERSON_VECTOR where personid=%d """%int((personID))
    cursor.execute(sqlSelectPersonVector)
    countRecordinPersonVector = cursor.fetchone()[0]
    # Insert into Person_Vector if Count is 0
    if(countRecordinPersonVector==0):
        sqlInsertPersonVector="""Insert into PERSON_VECTOR(federal,location_state,location_county,profesional,nationality,civil_status,bachelor,parent,age_range,personid)
    VALUES(%d,%d,%d,%d,%d,%d,%d,%d,%d,%d) """%(federal,locationState,locationCounty,professional,nationality,civilStatusID,bachelor,parent,age_range,personID)
        cursor.execute(sqlInsertPersonVector)
        db.commit()
    else:
        sqlUpdatePersonVector="""Update PERSON_VECTOR set federal=%d,location_state=%d,location_county=%d,profesional=%d,nationality=%d,civil_status=%d,bachelor=%d,parent=%d,age_range=%d,personid=%d
    """%(federal,locationState,locationCounty,professional,nationality,civilStatusID,bachelor,parent,age_range,personID)
        cursor.execute(sqlUpdatePersonVector)
        db.commit()