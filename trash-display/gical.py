from urllib.request import urlopen
from ics import Calendar, timeline
import credentials

class gical():
    def get_Cal(self):
        ical_data = Calendar(urlopen(credentials.ical_url).read().decode('iso-8859-1'))        
        print(ical_data)

if __name__ == "__main__":
    ical_data = Calendar(urlopen(credentials.ical_url).read().decode('iso-8859-1'))
    e = timeline.Timeline(ical_data)
    for i in e.today():
        print(i.begin)