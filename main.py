import kivy
kivy.require('2.0.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from lxml import html
import webbrowser

class MyApp(App):
    def build(self):

        baseUrl = 'https://www.blixten.se'
        url = baseUrl + '/artister-och-evenemang/sarah-dawn-finer/'
        root = AnchorLayout(anchor_x='center', anchor_y='center')

        def openWeb(url):
             webbrowser.open(url)

        def scrapeSite(req, result):
            tree = html.fromstring(req.result)
            events = tree.xpath('//div[@class="c-event"]')
            anchors = tree.xpath('//div[@class="c-event"]//a[contains(@class,"event__col")]')

            elements = []
            for e,a in zip(events, anchors):
                elements.append({**e.attrib, **a.attrib})
            
            backgroundImgSrcFull = tree.xpath('//img[@class=" image__default"]')[0].attrib['src']
            backgroundImgSrc = baseUrl + backgroundImgSrcFull[:backgroundImgSrcFull.find('?')]                        

            backgroundImage = AsyncImage(
                source= backgroundImgSrc,
                size_hint = [1,1]
            )
            
            root.add_widget(backgroundImage)
            
            box = BoxLayout(
                orientation='vertical',
                spacing = -2
            )
            root.add_widget(box)

            box.add_widget(
                Label(
                    text = 'The Sarah Dawn Finder',
                    bold = True,
                    font_size = '32sp'
                )
            )

            for item in elements[:5]:
                btn = Button(
                    background_color = [0, 0, 0, 0.5],
                    color = [1,1,1,1],
                    font_size = '17sp',
                    bold = True,
                    text = item['data-dom-filter-name'] 
                        + ': ' + item['data-dom-filter-city'] 
                        + ' - ' + item['data-dom-filter-date'] 
                )
                btn.bind(on_press = lambda x, item=item: openWeb(baseUrl + item['href']))
                box.add_widget(btn)

        def refreshData(dt):
            UrlRequest(url,scrapeSite).wait()

        refreshData(0)
        Clock.schedule_interval(refreshData, 3600)
        
        return root

if __name__ == '__main__':
    MyApp().run()