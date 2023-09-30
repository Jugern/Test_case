from datetime import datetime, timedelta
from requests import get
import json


class WorkRequest():

    def __init__(self, spisok_csv: list[str], *args, **kwargs):
        self.spisok_csv = spisok_csv
        self.return_slovar = dict()
        self.linux_time = datetime(year=1970, month=1, day=1, hour=0, minute=0, second=0)

    def start_requests(self, *args, **kwargs) -> dict:

        for i in self.spisok_csv:
            kent = i
            slovo = 'https://www.megaputer.ru/api/search-certificates?query_name={0}%20{1}%20{2}'.format(*kent)
            response = json.loads(get(slovo).text)
            if response['result']:
                for x in response['result'][0]['certificates']:
                    self.return_slovar.setdefault(' '.join(kent), []).append((x['name'],                                                             self.linux_time + timedelta(seconds=x['data_issue'])))
            else:
                self.return_slovar.setdefault(' '.join(kent), [])
        return self.return_slovar
