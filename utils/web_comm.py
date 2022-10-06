import requests
from selenium import webdriver
import datetime
import logging
import time

logger = logging.getLogger(__name__)

logging.basicConfig(filename='web_comm.log', encoding='utf-8', level=logging.DEBUG)

class Web_Driver:

    def __init__(self, origin: str, destination: str, start: str, end: str, quantity: int = 1):
        
        assert origin != destination, "Can't fly to same airport"
        this_century = str(int(datetime.date.today().year / 100))
        self._in = {
            'orig': origin.lower(),
            'dest': destination.lower(),
            'start': {'yy': int(this_century + start[0:2]), 'mm': int(start[2:4]), 'dd': int(start[4:6]), 'fmt': start},
            'end': {'yy': int(this_century + end[0:2]), 'mm': int(end[2:4]), 'dd': int(end[4:6]), 'fmt': end},
            'qty': str(quantity) 
        }
        self.check_dates(self._in)
    
    # Main Utils
    def generate_urls(self):
        '''
            URL requirements:
                -> (SkyScanner):
                    orig - 'rdu', 'RDU' (Raleigh-Durham)
                    dest - 'ams', 'AMS' (Amsterdam)
                    start - '221029' (October 29th 2022)
                    end - '221112' (November 12th 2022)
        '''

        # TODO: Add cabin class options in future ;)
        # TODO: Trim URL
        # TODO: Add more URLs
        self.site_lib = {'skyscanner': f"https://www.skyscanner.com/transport/flights/{self._in['orig']}/{self._in['dest']}/{self._in['start']['fmt']}/{self._in['end']['fmt']}/?adultsv2={self._in['qty']}&cabinclass=economy&childrenv2=&inboundaltsenabled=false&outboundaltsenabled=false&preferdirects=false&rtn=1",
                        'kayak': f"https://www.kayak.com/flights/RDU,IAD-BDQ,AMD/2022-10-27/2022-11-11?sort=price_a"}
    
    # Helpers
    def test_response_code(self, site: str, retry: int = 1):
        '''
            This method is to get the response code and make sure everything is working as expected.
            Note we are looking for a 200 response code. 
            # TODO: Implement a retry
        '''
        self.generate_urls()
        responses = []
        for _ in range(retry):
            test_request = requests.get(self.site_lib.get(site))
            logger.debug(test_request.status_code)
            if test_request.status_code < 199:
                logger.info("Informational response")
            elif test_request.status_code < 299 and test_request.status_code > 200:
                logger.info("Successful response!")
            elif test_request.status_code < 399 and test_request.status_code > 300:
                logger.info("Redirection response")
            elif test_request.status_code < 499 and test_request.status_code > 400:
                logger.info("Client error response")
            else:
                logger.info("Server error response")
            responses.append(test_request.status_code)
            time.sleep(10)


    @staticmethod
    def check_dates(data: dict):
        s_date = datetime.date(data['start']['yy'], data['start']['mm'], data['start']['dd'])
        e_date = datetime.date(data['end']['yy'], data['end']['mm'], data['end']['dd'])
        assert (e_date - s_date).days > 0, "Start date is after End date!"

    def add_new_site(self, url: str, name: str):
        '''
            Simple dictionary update. Add url to site library. 
        '''
        self.site_lib.update({name: url})

