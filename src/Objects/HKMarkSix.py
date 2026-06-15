from bs4 import BeautifulSoup

from src.Helpers import WebHelper as wh


# "https://lottery.hk/en/mark-six/results/2025"

class HKMarkSix():
    def __init__(self):
        self.location = "HK"
        self.sourceurl = "https://lottery.hk/en/mark-six/results/"
        return

    def extractLotteries(self, table):

        lotteries = []
        for t in table:
            body = t.select('tbody')

            for b in body:
                rows = b.select('tr')

            for r in range(len(rows)): # row in rows:
                if len(rows) - (r + 1) < 0:
                    break

                details = rows[len(rows) - (r + 1)].select('td')
                if len(details) <= 0:
                    continue

                lottery = {}
                for i in range(len(details)):
                    tdsoup = BeautifulSoup(str(details[i]), 'html.parser')

                    if i == 0:
                        lottery['no'] = tdsoup.get_text()
                    elif i == 1:
                        lottery['date'] = tdsoup.get_text()
                    elif i == 2:
                        balls = tdsoup.get_text()

                        draw_balls = []
                        for b in balls.split('\n'):
                            if b.isnumeric():
                                draw_balls.append(int(b))

                        lottery['balls']=draw_balls

                lotteries.append(lottery)

        return lotteries

    def getLotteries(self, year):

        url = self.sourceurl + str(year)
        content = wh.get_urlcontent(url)

        tab = content.find_all('table', {'class': "-center _results"})
        if tab is None:
            return None

        Lotteries = self.extractLotteries(tab)
        # print(table)

        return Lotteries