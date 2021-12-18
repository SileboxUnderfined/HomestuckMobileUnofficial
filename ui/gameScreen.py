import requests, bs4
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

class GameScreen(Screen):
    def __init__(self, name, page):
        super(GameScreen, self).__init__()
        self.name = name
        self.page = page + 1901
        self.url = "https://www.mspaintadventures.ru/?s=6&p=00"
        self.ids.page.text = str(self.page)
        self.loadPage()

    def loadPage(self):
        r = requests.get(self.url + str(self.page))
        soup = bs4.BeautifulSoup(r.text,'html.parser')
        rh = self.headerText(soup)
        ri = self.centerImage(soup)
        ra = self.actionTextGet(soup)
        rb = self.buttonNext(soup)

    def headerText(self, soup):
        self.ids.header.text = soup.p.font.text
        return True

    def centerImage(self, soup):
        tr = soup.find('tr',class_="comic-images")
        print(tr.img['src'])
        self.ids.center.source = tr.img['src']
        return True

    def actionTextGet(self, soup):
        td = soup.find('td', attrs={"style":"font-weight: bold; font-family: Courier New, monospace;color:#000000;line-height: 1.35"})
        ps = td.findAll('p')
        for p in ps:
            self.ids.actionText.add_widget(Label(text=p.text))

        return True

    def buttonNext(self, soup):
        a = soup.find('a', class_="")
        self.ids.nextPageButton.text = a.get_text()

    def nextPage(self):
        self.page += 1
        self.loadPage()

    def previousPage(self):
        self.page -= 1
        self.loadPage()