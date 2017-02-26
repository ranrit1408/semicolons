import requests
import json
import logging

def updateProfile(access_token, conn):
    profile = requests.get("https://graph.facebook.com/me?fields=id,name,gender,email,about,birthday,education,hometown,likes,location,relationship_status,family,work&access_token=" + access_token)
    profile=profile.json()

    logging.info(profile)
  
    #interests = graph.get_connections(id="me", connection_name="likes")['data']
    formatted_profile = json.dumps(profile)
    profile_load = json.loads(formatted_profile)
    location = profile_load['location']['name']
    homeTown = profile_load['hometown']['name']
    school = profile_load['education']
    education = profile_load['education'][len(school)-1]['type']
    work = profile_load['work']
    if not (work is None):
        isProfessional = '1'
    likes = None

    for i in profile_load['likes']['data']:
      if (likes is None):
        likes = i['name']

      else:
        likes = likes + '/' + i['name'] 

    x = conn.cursor()
    result = None
    try:
        result = x.execute("SELECT facebookid from PERSONS where email=%s",profile_load['email'])

    except Exception as e:
        #print e
        conn.rollback()


    if (result is None):
        try:
           x.execute("""INSERT
           INTO
           `kendb`.
           `PERSONS`
           (
               `deviceid`,
               `number`,
               `dob`,
               `city`,
               `state`,
               `zipcode`,
               `education`,
               `gender`,
               `facebookid`,
               `civil`,
               `kids`,
               `email`,
               `isProfessional`,
               `hometown_state`,
               `interests`
               )
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                     ('1',
               '2241211212',
               profile_load['birthday'],
               location.split(',')[0],
               location.split(',')[1],
           '43016',
           education,
           profile_load['gender'],
           profile_load['id'],
            profile_load['relationship_status'],
           '1',
           profile_load['email'],
           isProfessional,
           homeTown.split(',')[1],
           likes))

           conn.commit()
        except Exception as e:
            #print e
            conn.rollback()
    else:
        try:
            result2 = x.execute("""UPDATE
                   `kendb`.
                   `PERSONS`
                   SET
                    `deviceid` = %s,
                    `number` = %s,
                    `dob` = %s,
                    `city` = %s,
                    `state` = %s,
                    `zipcode` = %s,
                    `education` = %s,
                    `gender` = %s,
                    `facebookid` = %s,
                    `civil` = %s,
                    `kids` = %s,
                    `email` = %s,
                    `isProfessional` = %s,
                    `hometown_state` = %s,
                    `interests` = %s
                    WHERE `facebookid` = %s""",
                               ('3',
                                '2241232323',
                                profile_load['birthday'],
                                location.split(',')[0],
                                location.split(',')[1],
                                '43016',
                                education,
                                profile_load['gender'],
                                profile_load['id'],
                                profile_load['relationship_status'],
                                '2',
                                profile_load['email'],
                                isProfessional,
                                homeTown.split(',')[1],
                                likes,
                                profile_load['id']))
            conn.commit()
        except Exception as e:
            #print e
            conn.rollback()

    return profile_load['id']
