import requests
import json
import jsonpickle
from json import JSONEncoder
from tqdm import tqdm
import pandas as pd


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

    def get_names(self, rng):
        list = []
        for x in tqdm(range(0, rng, 10)):
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
        nameList = []
        cuisineList = []
        ratingList = []
        reviewList = []
        mapList = []
        openList = []
        closeList = []
        paymentList = []
        bestDishList = []
        budgetList = []
        phoneList = []
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
            nameList.append(str(name))

            ####### cuisine #######
            try:
                beginCuis = source.index('3D">', source.index('servesCuisine'))
                endCuis = source.index('</a>', beginCuis)
                cuisine = source[beginCuis+4:endCuis]
                if cuisine == '<i class="dg-font">&#xf0f5;</i>Salir a comer':
                    cuisine = 'Salir a comer'
                cuisineList.append(str(cuisine))
            except:
                cuisineList.append("None")
            ####### ratings #######
            try:
                rating = self.search_and_return(source, 'Comida: ', ',')
                ratingList.append(str(rating))
            except:
                ratingList.append("None")
            ####### number of reviews #######
            try:
                reviews = self.search_and_return(
                    source, 'Leer todos los comentarios (', ')')
                reviewList.append(str(reviews))
            except:
                reviewList.append("None")
            ####### google coordinates #######
            try:
                beginMap = source.index('href="https://www.google.com/maps/')
                endMap = source.index('">', beginMap)
                mapLink = source[beginMap+6:endMap]
                mapList.append(str(mapLink))
            except:
                mapList.append("None")

            ####### schedule #######
            try:
                schedule = self.search_and_return(
                    source, 'style="display: block;">', '</span>')
                schedule = schedule.replace("Hoy", "")
                try:
                    a, b = schedule.split(" a", 1)
                    openList.append(a)
                    closeList.append(b)
                except:
                    openList.append(schedule)
                    closeList.append(schedule)
            except:
                openList.append("None")
                closeList.append("None")

            ####### payment methods #######
            try:
                payment = self.search_and_return(
                    source, '<li><i class="dg-sprite dg-', '-small')
                try:
                    source2 = source[source.index(payment)+6:]
                    payment2 = self.search_and_return(
                        source2, 'dg-sprite dg-', '-small')
                    paymentList.append(str(payment+" & "+payment2))
                except:
                    paymentList.append(str(payment))
            except:
                paymentList.append("None")

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

                bestDishList.append(str(bestDish1)+", " +
                                    str(bestDish2)+", "+str(bestDish3))
            except:
                bestDishList.append("None")

            ####### budget #######
            try:
                budget = self.search_and_return(
                    source, '<div class="col-3 g-font-size-20 dg-font-blue text-right g-line-height-1 g-font-weight-600 rest-price">', '</div>')
                try:
                    budget = budget.replace('.', "")
                    budget = int(budget) * 0.0000037
                except:
                    pass
                budgetList.append(str(budget))
            except:
                budgetList.append("None")

            ####### phone number #######
            try:
                phoneNum = self.search_and_return(source,
                                                  '<button class="btn btn-block btn-dg-white-outline-gray-soft g-font-size-16 btn-ver-telefono" data-main-phone="', '" data')
                phoneList.append(phoneNum)
            except:
                phoneList.append("None")

        df = pd.DataFrame(
            {'Name': nameList,
             'Cuisine': cuisineList,
             'Ratings': ratingList,
             'Review': reviewList,
             'Map': mapLink,
             'Open Time': openList,
             'Close Time': closeList,
             'Payment Methods': paymentList,
             'Best Dishes': bestDishList,
             'Budget in USD': budgetList,
             'Phone Number': phoneList
             })
        df.to_csv(r'data.csv', index=False, header=True)

    def main_loop(self):
        list = self.get_names(1700)
        details = self.get_details(list)


# Get all resturant names returned as a list
InfiniteScraper().main_loop()

# https://drive.google.com/drive/folders/1J9S-1rMSLngGv_uWANh6aYVPkvcqa3zI
