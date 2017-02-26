# -*- coding: utf-8 -*-

import NewRK
import re
import operator
#rake = NewRK.Rake("stoppath.txt");
import pymysql
import requests
import urllib2
import json


def NlptagsGen(text):
    sentenceList = NewRK.split_sentences(text)
    stopwordpattern = NewRK.build_stop_word_regex("stoppath.txt")
    phraseList = NewRK.generate_candidate_keywords(sentenceList, stopwordpattern)

    wordscores = NewRK.calculate_word_scores(phraseList)
    keywordcandidates = NewRK.generate_candidate_keyword_scores(phraseList, wordscores)

    sortedKeywords = sorted(keywordcandidates.iteritems(), key=operator.itemgetter(1), reverse=True)
    totalKeywords = len(sortedKeywords)
    if (totalKeywords > 4):
        totalKeywords = 4
    nlps = ""
    for keyword in sortedKeywords[0:totalKeywords]:
        # print "Keyword: ", keyword[0], ", score: ", keyword[1]
        nlps = nlps + keyword[0]+"; "
    return nlps


#DB
con= pymysql.connect(host='130.211.157.189', port=3306, user='root',password='root',db='kendb',charset='utf8')



cursor= con.cursor()
url="https://www.federalregister.gov/api/v1/documents.json?per_page=1000&order=relevance&conditions%5Bpublication_date%5D%5Bgte%5D=2016-01-01"
response=urllib2.urlopen(url).read()
json_obj = json.loads(response)

cn=0



for key in json_obj:
        value = json_obj[key]

       # print("The key and value are ({}) = ({})".format(key, value))
        print 'The key and value are',key
        if(key=="results"):
            for obj in json_obj[key]:
              #  print "\n", obj["title_without_number"]
                title=obj["title"]
                abstract=obj["abstract"]
                publication_date=obj["publication_date"]
                if(abstract !=None and title != None):
                            nlpTags = NlptagsGen(abstract)
                            if("Immigration" in abstract or "USCIS" in abstract or "H1-B" in abstract):
                                nlpTags ="Immigration; USCIS; "+ nlpTags
                            #nlpTags=""
                            # session = requests.Session()
                            # session.headers.update({'api-key': 'c8160c40-fb37-11e6-b22d-93a4ae922ff1'})
                            # bodyData = {'body': json.dumps(abstract),
                            #            'api-key': 'c8160c40-fb37-11e6-b22d-93a4ae922ff1'}
                            # outputTags = session.post("http://api.cortical.io:80/rest/text/keywords?retina_name=en_associative", data=bodyData).json()
                            # for idx, item in enumerate(outputTags):
                            #     nlpTags=nlpTags + item +", "
                            cn = cn + 1
                            api_source = "www.federalregister.gov"
                            #print "\n\n",title,"\n",abstract,"\n",publication_date,"\n",nlpTags,"\n",api_source,"\n",cn
                            #tags="H1-B,H-1B,h1-b,h-1b "
                            cursor.execute(
                               "insert into LAWS(source, extractionDate, summary, title, nlpTags) values(%s, %s, %s,%s,%s)",
                                (api_source, publication_date, abstract, title, nlpTags))
                            title=None
                            abstract=None
                            publication_date=None
                            nlpTags=None
                            #billsDesc=None

               # print "titils: ",obj["titles"]
cursor.close()
con.commit()
con.close()
print 'Inserted successfully!!!'


#text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility "





