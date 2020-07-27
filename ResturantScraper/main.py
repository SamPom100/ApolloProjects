import requests


class InfiniteScraper():
    def scrape(self, num):
        URL = 'https://www.degustavenezuela.com/caracas/services/search?filters=eyJmaWx0ZXJzIjp7fSwic2NvcmVfcmFuZ2UiOnt9LCJzb3J0IjoiZm9vZCJ9&offset='
        combinedURL = URL+str(num)
        response = requests.get(combinedURL)
        source = response.text
        return source

    def stringCleaner(self, s):
        return ''.join([i for i in s if not i.isdigit()])

    def firstKey(self, sampleText):
        begin_key = 'g-color-black g-color-primary--hover g-font-weight-600 g-text-underline--none--hover'
        end_key = '<\/a>'
        begin = sampleText.index(begin_key) + 84
        end = sampleText.index(end_key, begin)
        return sampleText[begin:end]

    def secondKey(self, sampleText):
        begin_key = 'html'
        begin = sampleText.index(begin_key) + 7
        return sampleText[begin:]

    def get_names(self):
        list = []
        for x in range(0, 100, 10):
            sampleText = self.scrape(x)
            resturantNum = sampleText.count(
                'g-color-black g-color-primary--hover g-font-weight-600 g-text-underline--none--hover')
            for y in range(0, resturantNum, 1):
                begin_key = 'g-color-black g-color-primary--hover g-font-weight-600 g-text-underline--none--hover'
                end_key = '\"'
                begin = sampleText.index(begin_key) + 84 + 34
                end = sampleText.index(end_key, begin) - 1
                resturantName = sampleText[begin:end]
                list.append(resturantName)
                sampleText = sampleText[begin:]
        return list

    def search_and_return(self, text, begin, end):
        begin_num = text.index(begin) + len(begin)
        end_num = text.index(end, begin_num)
        return text[begin_num:end_num]

    def get_details(self, list):
        for x in list:
            URL = 'https://www.degustavenezuela.com/caracas/restaurante/'
            combinedURL = URL+x
            response = requests.get(combinedURL)
            source = response.text
            ####### name #######
            name = self.search_and_return(
                source, 'data-restaurant-name="', 'data-plan-letter')
            print('\n'+"name: "+name[:-2])
            ####### cuisine #######
            beginCuis = source.index('3D">', source.index('servesCuisine'))
            endCuis = source.index('</a>', beginCuis)
            cuisine = source[beginCuis+4:endCuis]
            if cuisine == '<i class="dg-font">&#xf0f5;</i>Salir a comer':
                cuisine = 'Salir a comer'
            print("cuisine: "+cuisine)
            ####### ratings #######
            rating = self.search_and_return(source, 'Comida: ', ',')
            print("rating: "+rating)
            ####### number of reviews #######
            reviews = self.search_and_return(
                source, 'Leer todos los comentarios (', ')')
            print("reviews: "+reviews)
            ####### google coordinates #######
            beginMap = source.index('href="https://www.google.com/maps/')
            endMap = source.index('">', beginMap)
            mapLink = source[beginMap+6:endMap]
            print("map: "+mapLink)
            ####### schedule #######
            schedule = self.search_and_return(
                source, 'style="display: block;">', '</span>')
            print("schedule: "+schedule)
            ####### payment methods #######
            payment = self.search_and_return(
                source, '<li><i class="dg-sprite dg-', '-small')
            try:
                source2 = source[source.index(payment)+6:]
                payment2 = self.search_and_return(
                    source2, 'dg-sprite dg-', '-small')
                print("payments: "+payment+" & "+payment2)
            except:
                print("payment: "+payment)
            ####### best dishes #######
            try:
                bestDish = self.search_and_return(
                    source, '<div class="dish-name dg-font-gray-soft g-font-size-16 dg-text-ellipsis">', '</div>')
                print("best dish: "+bestDish)
            except:
                print("best dish: none")
            ####### budget #######
            budget = self.search_and_return(
                source, '<div class="col-3 g-font-size-20 dg-font-blue text-right g-line-height-1 g-font-weight-600 rest-price">', '</div>')
            print("budget: "+budget)

    def main_loop(self):
        list = self.get_names()
        details = self.get_details(list)


# Get all resturant names returned as a list
print(InfiniteScraper().main_loop())
