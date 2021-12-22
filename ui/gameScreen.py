import requests, bs4, json, os
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.popup import Popup
from kivy.uix.button import Button

class GameScreen(Screen):
    def __init__(self,sm, name, page=0, autoSaveEnabled=None):
        super(GameScreen, self).__init__()
        self.sm = sm
        self.name = name
        self.page = page + 1901
        self.url = "https://www.mspaintadventures.ru/?s=6&p=00"
        #self.ids.page.text = str(self.page)
        self.loadGame(True)
        self.autoSaveEnabled = autoSaveEnabled
        self.loadPage()

    def loadPage(self):
        if self.autoSaveEnabled:
            self.saveGame()

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
        self.ids.center.clear_widgets()
        tr = soup.find('tr',class_="comic-images")
        imgs = tr.findAll('img')
        for img in imgs:
            self.ids.center.add_widget(AsyncImage(source=img['src'],anim_delay=0.3))

        return True

    def actionTextGet(self, soup):
        self.ids.actionText.clear_widgets()
        td = soup.find('td', attrs={"style":"font-weight: bold; font-family: Courier New, monospace;color:#000000;line-height: 1.35"})
        ps = td.findAll('p')
        ps.pop(0)
        for p in ps:
            self.ids.actionText.add_widget(Label(text=p.text,font_name="CourierNew",bold=True, halign="justify",color=[0,0,0,1]))

        print(self.ids.actionText.children)
        return True

    def buttonNext(self, soup):
        a = soup.find('a', class_="")
        self.ids.nextPageButton.text = a.get_text()

    def nextPage(self):
        self.page += 1
        self.loadPage()

    def previousPage(self):
        if self.page -1 == 1900:
            return
        else:
            self.page -= 1
            self.loadPage()

    def autoSave(self, initial=False):
        self.autoSaveEnabled = not self.autoSaveEnabled
        autosaved = self.checkAutoSave()
        self.saveGame(True)
        if initial == False:
            popup = Popup(title=autosaved,content=Label(text="Нажмите в любое место за уведомлением чтобы закрыть его"),size=(500,100),size_hint=(None,None))
            popup.open()

    def checkAutoSave(self):
        if self.autoSaveEnabled == True:
            return "Автосохранение включено"

        else:
            return "Автосохранение отключено"

    def saveGame(self, fromAutoSave=False):
        f = open('save.json','wt')
        data = {"page":self.page,"autoSave":self.autoSaveEnabled}
        json.dump(data,f)
        f.close()
        if fromAutoSave == False:
            popup = Popup(title='Игра сохранена!',
                          content=Label(text="Нажмите в любое место за уведомлением чтобы закрыть его"),size=(500,100),size_hint=(None,None))

            popup.open()

    def loadGame(self, initial=False):
        try:
            f = open('save.json','rt')
        except FileNotFoundError:
            return

        data = json.load(f)
        if initial == True:
            if data['autoSave'] == False:
                return

        self.page = data['page']
        self.autoSaveEnabled = data['autoSave']
        f.close()
        self.loadPage()
        if initial == False:
            popup = Popup(title='Игра загружена!!',
                          content=Label(text="Нажмите в любое место за уведомлением чтобы закрыть его"),size=(500,100),size_hint=(None,None))

            popup.open()

    def deleteGame(self):
        os.remove('save.json')
        popup = Popup(title='Игра удалена!',
                      content=Label(text="Нажмите в любое место за уведомлением чтобы закрыть его"),size=(500,100),size_hint=(None,None))

        popup.open()

    def nextPageButtonColor(self):
        return [0,1,0,1]

    def callbackFABSD(self,instance):
        icon = instance.icon
        funcs = {"content-save":self.saveGame,
                 "content-save-all":self.autoSave,
                 "upload":self.loadGame,
                 "delete":self.deleteGame,
                 "step-backward":self.previousPage}

        if icon in funcs:
            funcs[icon]()
        else:
            self.sm.current = "menu"

    def dataFABSD(self):
        return {
            "Сохранить игру":"content-save",
            "Автосохранение":"content-save-all",
            "Загрузить игру":"upload",
            "Удалить игру":"delete",
            "В главное меню":"menu",
            "На предыдущую страницу":"step-backward"
        }