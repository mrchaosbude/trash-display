from bs4 import BeautifulSoup
import logging
import urllib.request as requests
import datetime
import re

logging.basicConfig(level=logging.DEBUG)

class ajldates():
    def __init__(self):
        pass

    def run(self, city, street=None):
        d = self.getCityUrl(city, street=None)
        return self.getDates(d)

    def getCityUrl(self, city, street=None):
        """Gets the url of the given city
        
        Arguments:
            city {[string]} -- [give the name of the city you want]
        
        Returns:
            [str] -- [gets the url]
        """
        logging.debug('[+] Start "getCityUrl" !')
        listofcitys = dict()
        data1 = requests.urlopen("https://www.ajl-mbh.de/abfallkalender/entsorgungstermine-ajl").read()        
        soup = BeautifulSoup(data1, "lxml")
        logging.debug('[+] Start Scrapyng Citys')
        for item in soup.find_all("a", {"class": "stadtbutton"}):
            listofcitys.update({item.text.casefold()[1:-1]: item.get('href')}) # füllt das dict entfernt die leer stellen am anfang und ende            
        logging.debug('[+] Finisch Scraping Citys')
        
        logging.debug('[+] Check for Street')
        listofstreets = dict()
        try:
            data2 = requests.urlopen(listofcitys[city.casefold()]).read()   
        except:
                for key, _ in listofcitys.items() :
                    print (key)
                raise Exception("Plese chose the right city")                 
        soup2 = BeautifulSoup(data2, "lxml")
        t = soup2.find(id="street")
        if t == None:
            logging.debug('[+] No Street needet')
            logging.debug('[+] the Url= '+ listofcitys[city.casefold()] + "&printview=1")
            return listofcitys[city.casefold()] + "&printview=1"            
        
        for item2 in t.find_all("option"):
            listofstreets.update({item2.text.casefold() : item2.get('value')})
        if street == None:
            print("[+] List Of Streets:")
            for key, _ in listofstreets.items() :
                print (key)
            raise Exception('You Need add a street name')
        logging.debug('[+] the Url= ' + listofcitys[city.casefold()] + "&street=" + listofstreets[street.casefold()] + "&printview=1")
        return listofcitys[city.casefold()] + "&street=" + listofstreets[street.casefold()] + "&printview=1"

    def getDates(self, url):
        logging.debug('[+] Start "getDates"')
        page = requests.urlopen(url).read()
        soup = BeautifulSoup(page, "lxml")
        logging.debug('[+] Scrape "Year"')
        global year
        year = soup.find("h2", {"class": "ajl-green"})
        year = re.search(r'\d{4}', year.text).group()

        def gettonnes(name ,bsoup, text=0): # dont want to do this 4 times for every 
            logging.debug('[+] Scrape "{}"'.format(name))
            datetimelist = []
            textlist = []
            #year = soup.find("h2", {"class": "ajl-green"})
            #year = re.search(r'\d{4}', year.text).group()
            tonne = bsoup.find("div", {"class": name})
            for item in tonne.find_all("div", {"class": "dayprint"}):                
                textlist.append(item.text[3:] + str(year))
                d = datetime.datetime.strptime(item.text[3:] + str(year), '%d.%m.%Y')
                datetimelist.append(d)
            if text == 1:
                return textlist
            return datetimelist

        gelbeT = gettonnes("cat cat-gelb", soup)
        papierT = gettonnes("cat cat-papier", soup)
        bioT = gettonnes("cat cat-bio", soup)
        SchwartzeT = gettonnes("cat cat-rest", soup)
        logging.debug('[+] Finisch  Return the dict')
        return {"Gelbe_Tonne" : gelbeT, "Papiertonne" : papierT, "Biotonne" : bioT, "Schwarze Tonne" : SchwartzeT}

    
if __name__ == "__main__":
    d = ajldates()
    #p = d.getCityUrl("mützel", street="gorkistrasse")
    p = d.run("mützel", street="gorkistrasse")
    #b = d.getDates("https://www.ajl-mbh.de/abfallkalender/entsorgungstermine-ajl?year=2018&town=154&street=265&printview=1")
    print(p)