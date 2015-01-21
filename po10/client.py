import requests
from bs4 import BeautifulSoup
from models import Athlete, Ranking


class Client(object):
    
    def get_athlete(self, id):
        r = requests.get("http://www.thepowerof10.info/athletes/profile.aspx", params={"athleteid": id})
        
        if r.status_code != 200:
            raise AttributeError("Unable to find athlete with id %s." % id)
        
        soup = BeautifulSoup(r.content)
        
        a = Athlete({"id": id})
        
        name = soup.find_all(class_="athleteprofilesubheader")[0].h2.string.strip()
        a.name = name
        
        info = soup.find(id="ctl00_cphBody_pnlAthleteDetails").find_all('table')[2]    
        
        extra_details = {row.find_all("td")[0].string: row.find_all("td")[1].string for row in info.find_all("tr")}
        
        a.import_data(extra_details)
           
        try: 
            coach = soup.find(id="ctl00_cphBody_pnlAthleteDetails").find_all('table')[3].find("a").string
            coach_url = soup.find(id="ctl00_cphBody_pnlAthleteDetails").find_all('table')[3].find("a").get('href')
            
            a.coach = coach
        except:
            pass
    
        return a
    
    
    def get_ranking(self, event="10K", sex="M", year="2014", agegroup="ALL"):
        
        r = requests.get("http://www.thepowerof10.info/rankings/rankinglist.aspx", params={"event": event, "agegroup": agegroup, "sex": sex, "year": 2014})
        
        soup = BeautifulSoup(r.content)
        rankings_table = soup.find(id="ctl00_cphBody_lblCachedRankingList").find_all('table')[0]
        
        ranking_rows = [row for row in rankings_table.find_all("tr") if row["class"][0] not in ["rankinglisttitle", "rankinglistheadings", "rankinglistsubheader"]]
        
        rankings = []
        for row in ranking_rows:
            if row.find_all("td")[0].string is None:
                continue
            r = Ranking({"athlete": Athlete()})
            r.rank = int(row.find_all("td")[0].string)
            r.time = row.find_all("td")[1].string
            r.athlete.name = row.find_all("td")[6].string
            r.venue = row.find_all("td")[11].string
            r.date = row.find_all("td")[12].string
            
            rankings.append(r)
            
        return rankings
            