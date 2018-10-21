from urllib.request import urlopen
from ics import Calendar, timeline
import credentials
import arrow
from datetime import datetime

class gical():
    def get_Cal(self, days=+1):
        """[Get the next n days from a calender]
        
        Keyword Arguments:
            days {int} -- [how many days it will show] (default: {+1})
                
        Returns:
            [list in list] -- [return a list with list per event]
        """

        r = list()
        ical_data = Calendar(urlopen(credentials.ical_url).read().decode('iso-8859-1'))
        e = timeline.Timeline(ical_data)
        for i in e.included(arrow.now().replace(days=-1) ,arrow.now().replace(days=days)):
            r.append([i.name, datetime.fromtimestamp(i.begin.timestamp) ,datetime.fromtimestamp(i.end.timestamp)])
        return r

if __name__ == "__main__":
    print(gical().get_Cal())