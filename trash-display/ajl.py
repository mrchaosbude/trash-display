import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.DEBUG)

class ajldates():
    def __init__(self):
        pass
    
    def getCityUrl(self, city, street=None):
        """Gets the url of the given city
        
        Arguments:
            city {[string]} -- [give the name of the city you want]
        
        Returns:
            [str] -- [gets the url]
        """

        listofcitys = dict()
        data1 = requests.get("https://www.ajl-mbh.de/abfallkalender/entsorgungstermine-ajl").text        
        soup = BeautifulSoup(data1, "lxml")
        logging.debug('[+] Start Scrapyng Citys')
        for item in soup.find_all("a", {"class": "stadtbutton"}):
            listofcitys.update({item.text.casefold()[1:-1]: item.get('href')}) # füllt das dict entfernt die leer stellen am anfang und ende            
        logging.debug('[+] Finisch Scraping Citys')
        
        logging.debug('[+] Check for Street')
        listofstreets = dict()
        try:
            data2 = requests.get(listofcitys[city.casefold()]).text   
        except:
                for key, _ in listofcitys.items() :
                    print (key)
                raise Exception("Plese chose a city")                 
        soup2 = BeautifulSoup(data2, "lxml")
        t = soup2.find(id="street")
        if t == None:
            logging.debug('[+] No Street needet')
            return listofcitys[city.casefold()] + "&printview=1"            
        
        for item2 in t.find_all("option"):
            listofstreets.update({item2.text.casefold() : item2.get('value')})
        if street == None:
            print("[+] List Of Streets:")
            for key, _ in listofstreets.items() :
                print (key)
            raise Exception('You Need add a street name')
        return listofcitys[city.casefold()] + "&street=" + listofstreets[street.casefold()] + "&printview=1"

        
        
    
    
if __name__ == "__main__":
    d = ajldates()
    p = d.getCityUrl("müzel", street="gorkistrasse")
    print (p)
