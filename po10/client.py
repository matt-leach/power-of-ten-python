import requests
from bs4 import BeautifulSoup
from models import Athlete


class Client(object):
    
    def get_athlete(self, id):
        r = requests.get("http://www.thepowerof10.info/athletes/profile.aspx", params={"athleteid": id})
        
        if r.status_code != 200:
            raise AttributeError("Unable to find athlete with id %s." % id)
        
        soup = BeautifulSoup(r.content)
        
        a = Athlete()
        
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