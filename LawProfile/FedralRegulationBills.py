import pymysql
import requests
import urllib2
import json
from datetime import datetime

con= pymysql.connect(host='localhost',user='root',password='',db='usabills',charset='utf8')



cursor= con.cursor()
search="h1-b"
url="https://api.data.gov/regulations/v3/documents.json?api_key=ogZxNBIq7DyU0uqxWYUmUJwNh91TrStpDJnDpdLr&s=h1&dct=PS&rpp=1000&pd=11%2F06%2F13-02%2F20%2F17"
response=urllib2.urlopen(url).read()
json_obj = json.loads(response)

cn=0



for key in json_obj:
        value = json_obj[key]

       # print("The key and value are ({}) = ({})".format(key, value))
        print 'The key and value are',key
        if(key=="documents"):
            for obj in json_obj[key]:
              #  print "\n", obj["title_without_number"]
              if(obj["agencyAcronym"]=="USCIS"):
                titleDesc=obj["docketTitle"]
                currDt= obj["postedDate"].split("T")
                intDt=obj["commentStartDate"].split("T")
                currStatusDt = currDt[0]
                introducedDt = intDt[0]
                # currStatusDt=datetime.strptime(currStatusDt, '%Y-%m-%d').date()
                # introducedDt = datetime.strptime(introducedDt, '%Y-%m-%d').date()
                billsDesc=obj["commentText"]
                relatedBills="NA"
                if(billsDesc !=None):
                            cn = cn + 1
                            #print "\n\n",titleDesc,"\n",currStatusDt,"\n",introducedDt,"\n",relatedBills,"\n",billsDesc,"\n",cn
                            tags="H1-B,H-1B,h1-b,h-1b "
                            api_source="https://api.data.gov"
                            cursor.execute(
                                "insert into usbill_details(tags, title, description, introduced_date, current_status_date, realted_bills, api_source) values(%s, %s, %s,%s,%s, %s,%s)",
                                (tags, titleDesc, billsDesc, introducedDt, currStatusDt, relatedBills, api_source))
                            titleDesc=None
                            currStatusDt=None
                            introducedDt=None
                            relatedBills=None
                            billsDesc=None

               # print "titils: ",obj["titles"]
cursor.close()
con.commit()
con.close()
print 'Inserted successfully!!!'