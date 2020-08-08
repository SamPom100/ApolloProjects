import requests
import json
import jsonpickle
from json import JSONEncoder
from tqdm import tqdm


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
        data = {}
        list = list[:5]
        for x in tqdm(list):
            URL = 'https://www.degustavenezuela.com/caracas/restaurante/'
            combinedURL = URL+x
            response = requests.get(combinedURL)
            source = response.text

            ####### name #######
            name = self.search_and_return(
                source, 'data-restaurant-name="', 'data-plan-letter')
            # print('\n'+"name: "+name[:-2])
            name = name[:-2]
            data[name] = []

            ####### cuisine #######
            beginCuis = source.index('3D">', source.index('servesCuisine'))
            endCuis = source.index('</a>', beginCuis)
            cuisine = source[beginCuis+4:endCuis]
            if cuisine == '<i class="dg-font">&#xf0f5;</i>Salir a comer':
                cuisine = 'Salir a comer'
            data[name].append({"cuisine": str(cuisine)})

            ####### ratings #######
            rating = self.search_and_return(source, 'Comida: ', ',')
            data[name].append({"rating": str(rating)})

            ####### number of reviews #######
            reviews = self.search_and_return(
                source, 'Leer todos los comentarios (', ')')
            data[name].append({"reviews": str(reviews)})

            ####### google coordinates #######
            beginMap = source.index('href="https://www.google.com/maps/')
            endMap = source.index('">', beginMap)
            mapLink = source[beginMap+6:endMap]
            data[name].append({"map": str(mapLink)})

            ####### schedule #######
            schedule = self.search_and_return(
                source, 'style="display: block;">', '</span>')
            schedule = schedule.replace("Hoy", "")
            a, b = schedule.split(" a", 1)
            data[name].append({"openHour": str(a)})
            data[name].append({"closeHour": str(b)})

            ####### payment methods #######
            payment = self.search_and_return(
                source, '<li><i class="dg-sprite dg-', '-small')
            try:
                source2 = source[source.index(payment)+6:]
                payment2 = self.search_and_return(
                    source2, 'dg-sprite dg-', '-small')
                data[name].append({"payments": str(payment+" & "+payment2)})
            except:
                data[name].append({"payment": str(payment)})

            ####### best dishes #######
            tempSource = (source + '.')[:-1]
            try:
                bestDish1 = self.search_and_return(
                    tempSource, '<div class="dish-name dg-font-gray-soft g-font-size-16 dg-text-ellipsis">', '</div>')

                begin1 = tempSource.index(bestDish1) + len(bestDish1)
                tempSource = tempSource[begin1:]

                bestDish2 = self.search_and_return(
                    tempSource, '<div class="dish-name dg-font-gray-soft g-font-size-16 dg-text-ellipsis">', '</div>')

                begin2 = tempSource.index(bestDish2) + len(bestDish2)
                tempSource = tempSource[begin2:]

                bestDish3 = self.search_and_return(
                    tempSource, '<div class="dish-name dg-font-gray-soft g-font-size-16 dg-text-ellipsis">', '</div>')

                begin3 = tempSource.index(bestDish3) + len(bestDish3)
                tempSource = tempSource[begin3:]

                data[name].append(
                    {"best dish": str(bestDish1)+", "+str(bestDish2)+", "+str(bestDish3)})
            except:
                data[name].append({"best dish": "none"})

            ####### budget #######
            budget = self.search_and_return(
                source, '<div class="col-3 g-font-size-20 dg-font-blue text-right g-line-height-1 g-font-weight-600 rest-price">', '</div>')
            try:
                budget = budget.replace('.', "")
                budget = int(budget) * 0.0000037
            except:
                pass
            data[name].append({"budget in USD": str(budget)})

            ####### phone number #######
            phoneNum = self.search_and_return(source,
                                              '<button class="btn btn-block btn-dg-white-outline-gray-soft g-font-size-16 btn-ver-telefono" data-main-phone="', '" data')
            data[name].append({"phone": str(phoneNum)})
        return data

    def json_export(self, data):
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)

    def main_loop(self):
        list = self.get_names()
        details = self.get_details(list)
        self.json_export(details)


# Get all resturant names returned as a list
InfiniteScraper().main_loop()
