from bs4 import BeautifulSoup as bsoup
import requests as rq
import csv, simplejson, decimal, codecs
import pymongo 
import time
import pprint


nba_lst = ['atl', 'tor', 'chi', 'cle','wsh', 'mil','mia','bkn','cha','det',
           'ind','bos','orl','phi','ny','gs','mem','hou','por','dal','lac',
           'sa','okc','no','phx','utah','den','sac','lal','min']
           

def connect():
    connection = pymongo.MongoClient("mongodb://localhost")
    db=connection.sports
    nba = db.nba16
    return nba

def parse_espn(name):
    url = "http://espn.go.com/nba/team/schedule/_/name/" + name
    r = rq.get(url)
    soup = bsoup(r.content, 'lxml')
    ## Find all the rows that have classes. Remove the first one -- it's irrelevant.
    trs = soup.find_all("tr", class_=True)[1:]
    ## Main procedure.
    with open("nba_2016_csv/" + name + "_2016_schedule.csv", "wb") as ofile:
        f = csv.writer(ofile)
        ## Write the headers. 
        f.writerow( ["team","date","a/h","opponent","w/l","s","os"] )
        for tr in trs:
            team = name
            tds = tr.find_all("td")
            date = tds[0].get_text().encode("utf-8")
            opp = tds[1].find_all( "li", {"class": "team-name"} )
            for teams in opp:
                other_team = teams.get_text()
            opponent = tds[1].find_all( 'li',{'class':'game-status'} )
            for o in opponent:
                h_a = o.get_text()
                try:
                    win_loss = tds[2].find_all( 'li',{'class':'game-status win'} ) or tds[2].find_all( 'li',{'class':'game-status loss'} )
                    for a in win_loss:
                        w_l = a.get_text()

                    score = tds[2].find_all('a')
                    for s in score:
                        if w_l == 'W':
                            gs = s.get_text().split("-")[0]
                            gs = int(gs)
                            ogs = s.get_text().split("-")[1].split(" ")[0]
                            ogs = int(ogs)                            
                        elif w_l == 'L':
                            gs = s.get_text().split("-")[1].split(" ")[0]
                            gs = int(gs)
                            ogs = s.get_text().split("-")[0]
                            ogs = int(ogs)
                except:
                        h_a = ''
                        w_l = None
                        other_team = ''
                        gs = None
                        ogs = None
            ## write the result to the CSV file.
                finally:
                    f.writerow([team,date,h_a,other_team,w_l,gs,ogs])
                    g = dict(date=date, team=team,h_a=h_a,other_team=other_team, w_l=w_l,s=gs,os=ogs)
                    connect().save(g)
                    

def nba_teams(lst):
    i = 0
    while i < len(lst):
        parse_espn(str(lst[i]))
        time.sleep(2)
        i+=1
        
nba_teams(nba_lst)
    

# parse_espn('atl')
# parse_espn('tor')
# parse_espn('chi')
# parse_espn('cle')
# parse_espn('wsh')
# parse_espn('mil')
# parse_espn('mia')
# parse_espn('bkn')
# parse_espn('cha')
# parse_espn('det')
# parse_espn('ind')
# parse_espn('bos')
# parse_espn('orl')
# parse_espn('phi')
# parse_espn('ny')

# parse_espn('gs')
# parse_espn('mem')
# parse_espn('hou')
# parse_espn('por')
# parse_espn('dal')
# parse_espn('lac')
# parse_espn('sa')
# parse_espn('okc')
# parse_espn('no')
# parse_espn('phx')
# parse_espn('utah')
# parse_espn('den')
# parse_espn('sac')
# parse_espn('lal')
# parse_espn('min')


def make_json(name):
    data = open(name+"_2016_schedule.csv")
    reader = csv.DictReader(data, delimiter=",", quotechar='"')
    print reader
    with codecs.open(name+"_out.json", "w", encoding="utf-8") as out:
       for r in reader:
          
          for k, v in r.items(): 
             # make sure nulls are generated
             if not v:
                r[k] = None
             # parse and generate decimal arrays
             elif k == "s":
                r[k] = int(v)
             # generate a number
             elif k == "os":
                r[k] = int(v)
          out.write(simplejson.dumps(r, ensure_ascii=False, use_decimal=True)+"\n")


