from urllib.request import urlopen,Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from datetime import datetime
import re

def get_indeces_by_region(url):
    q = Request(url)
    html = urlopen(q)        
    bsObj = BeautifulSoup(html.read(),'html.parser')
    tables = bsObj.findAll("div",{"class":re.compile("^data-tables.*")})
    for table in tables:
        region_div = table.find("div",{"class":"table-container__header"})        
        region_name = region_div.h2.get_text()        
        indices = get_index_for_region(table)
        if(len(indices)!=0):
            for index in indices:
                index['region'] = region_name
            print(indices)


def get_index_for_region(table):
    results =[]
    for table_row in table.tbody.children:
        try:
            name_div =  table_row.find("div",{"data-type":"full"})
            name = name_div.get_text()
            abbreviation = table_row.find("div",{"data-type":"abbreviation"}).get_text()          
            tds = [x.get_text() for x  in table_row.findAll("td")]
            value = tds[1]
            net_change = tds[2]
            pct_change = tds[3]
            pct_change_month = tds[4]
            pct_change_year = tds[5]
            curtime = tds[6]
            now = datetime.now()
            timestamp = datetime.strptime(str(now.year)+" "+ str(now.month)+" "+ str(now.day)+" "+curtime,"%Y %m %d %I:%M %p")
            result = {"name":name,"abbreviation":abbreviation,"value":value,"net_change":net_change,"pct_change":pct_change,"pct_change_month":pct_change_month,"pct_change_year":pct_change_year,"timestamp":timestamp}
            results.append(result)
            
        except Exception as e:
            #print(e)
            continue
    return results
            

  
get_indeces_by_region('https://www.bloomberg.com/markets/stocks/world-indexes/europe-africa-middle-east')