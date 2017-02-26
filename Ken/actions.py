from random import randint
import logging

def LawFind(parameters, fbid, db):
	logging.info("LawFind")

	#from dict of lawa fetched from DB 
	cursor = db.cursor()

	logging.info("cursor built in LawFind")

	logging.info("fbid : "+str(fbid))

	cursor.execute("SELECT lawId, title, personid  FROM STAGING_VIEW WHERE facebookid = '%s' AND lawListened = 0 ORDER BY lawRelevance DESC" % (str(fbid)) )

	count = cursor.rowcount

	if count > 0:
		
		row = cursor.fetchone()
	
		LawId = int(row[0])

		try :
			cursor.execute("UPDATE USER_LAWS_STAGING SET LawListened = 1 WHERE lawId='%d' AND personId = '%d'" %( int(LawId), int(row[2]) ))
			db.commit()
		except:
			db.rollback()

		response = str(row[1])
		
		logging.info("response from LawFind: "+response)
		return {"response":response+". Do you want more information about this law?", "contextOut":[{"name":"UserAnswer","lifespan":10, "parameters":{"LawId" : LawId , "PersonId" : row[2]}}]}

	else:
		response = "There are no relevant laws for you."
		logging.info("response from LawFind: "+response)
		return {"response":response, "contextOut":[]}
		
	
def LawMoreInformation(parameters, fbid, db):
	logging.info("inside LawMoreInformation")
	cursor = db.cursor()
	logging.info("Cursor bulit in LawMoreInformation")

	if parameters["MoreInfo"] == "yes":
		#fetch more info

		cursor.execute("SELECT summary from LAWS WHERE lawId = '%d'" %(int(parameters['LawId'])))

		row = cursor.fetchone()

		response = row[0]

		try :
			cursor.execute("UPDATE USER_LAWS_STAGING SET lawUseful = 1 WHERE lawId='%d' AND personId = '%d'" %( int(parameters['LawId']), int(parameters["PersonId"]) ))
			db.commit()
		except:
			db.rollback()

	else:
		response = "Ok."

	#check DB for more laws 

	cursor.execute("SELECT lawId  FROM STAGING_VIEW WHERE facebookid = '%s' AND lawListened = 0 ORDER BY lawRelevance DESC" % (str(fbid)) )

	count = cursor.rowcount

	if count > 0:#laws exists:
		response = response + ". Do you want to see some more laws?" 
		contextOut = [{"name":"MoreLaw", "lifespan" : 1, "parameters" : {} }]
	else:
		response = response + " There are no more relevant laws for you."#stop conversation
		contextOut = []

	logging.info("response from LawMoreInformation: "+response)

	return {"response":response, "contextOut":contextOut}


def MoreLaw(parameters, fbid, db):
	logging.info("inside NextLaw")

	cursor = db.cursor()
	logging.info("Cursor bulit in MoreLaw")

	cursor.execute("SELECT lawId, title, personid FROM STAGING_VIEW WHERE facebookid = '%s' AND lawListened = 0 ORDER BY lawRelevance DESC" % (str(fbid)) )

	count = cursor.rowcount

	row = cursor.fetchone()

	LawId = int(row[0])

	try :
		cursor.execute("UPDATE USER_LAWS_STAGING SET LawListened = 1 WHERE lawId='%d' AND personId = '%d'" %( int(LawId), int(row[2]) ))
		db.commit()
	except:
		db.rollback()

	response = str(row[1])

	logging.info("response from MoreLaw: "+response)	

	return {"response":response+". Do you want more information about this law?", "contextOut":[{"name":"UserAnswer","lifespan":1, "parameters":{"LawId":LawId}}]}

	
handler = {
	"LawFind" : LawFind,
	"LawMoreInformation" : LawMoreInformation,
	"MoreLaw" : MoreLaw
}
