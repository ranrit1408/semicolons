import numpy as np
import MySQLdb as my
def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):

    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

db = my.connect("130.211.157.189","root","root","kendb" )
cursor = db.cursor()

sqlLawVector = """select * from LAWS_VECTOR """
sqlPersonVector= """select * from PERSON_VECTOR"""
cursor.execute(sqlLawVector)
allLaws = cursor.fetchall()
cursor.execute(sqlPersonVector)
allPerson = cursor.fetchall()


for onePerson in allPerson:

    #print onePerson
    print "new person \n\n",onePerson[10]
    # for val in onePerson:
    #     print val
    for eachLaw in allLaws:
        relevencePercentage= (1 -angle_between(eachLaw, onePerson))*100
        #print eachLaw

        print(relevencePercentage)," Law id ",eachLaw[10]
        if(relevencePercentage > 40):
            sqlInsertRelevance = """Insert into USER_LAWS_STAGING(personId,lawId,lawRelevance,lawUseful,lawListened)
                 VALUES(%d,%d,%d,0,0) """ % (
                 onePerson[10],eachLaw[10],int(relevencePercentage))
            cursor.execute(sqlInsertRelevance)
            db.commit()


# result = (1 - angle_between((0,10,502,1,50,3,1,1), (0,20,3020,1,50,3,0,1)))*100
