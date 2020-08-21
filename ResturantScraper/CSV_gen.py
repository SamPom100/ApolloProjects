import requests
import json
import jsonpickle
from json import JSONEncoder
from tqdm import tqdm
import pandas as pd


class InfiniteScraper():
    def scrape(self, num, URL):
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

    def get_names(self, rng, URL):
        list = []
        for x in tqdm(range(0, rng, 10)):
            sampleText = self.scrape(x, URL)
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

    def get_details(self, list, filename):
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
        df.to_csv(filename+'.csv', index=False, header=True)

    def main_loop(self):
        URL = 'https://www.degustavenezuela.com/caracas/services/search?filters=eyJmaWx0ZXJzIjp7fSwic2NvcmVfcmFuZ2UiOnt9LCJzb3J0IjoiZm9vZCJ9&offset='
        # 660
        URL2 = 'https://www.degustavenezuela.com/caracas/services/search?filters=eyJmaWx0ZXJzIjp7fSwic2NvcmVfcmFuZ2UiOnt9LCJuZWlnaGJvcmhvb2QiOlsiQWx0YSBGbG9yaWRhIiwiQWx0YW1pcmEiLCJBbHRvIEhhdGlsbG8iLCJBbHRvIFByYWRvIiwiQXYuIFZpY3RvcmlhIiwiQXZlbmlkYSBCYXJhbHQiLCJBdmlsYSBN4WdpY2EiLCJCYXJ1dGEiLCJCZWxsYXMgQXJ0ZXMiLCJCZWxsbyBDYW1wbyIsIkJlbGxvIE1vbnRlIiwiQm9sZWl0YSIsIkJvbGVpdGEgTm9ydGUiLCJCb2xl7XRhIFN1ciIsIkNhbXBvIEFsZWdyZSIsIkNhcGl0b2xpbyIsIkNhdGlhIiwiQ2F1cmltYXJlIiwiQ2Vycm8gVmVyZGUiLCJDaGFjYW8iLCJDaGFjYe10byIsIkNodWFvIiwiQ29saW5hIGRlIGxvcyBDYW9ib3MiLCJDb2xpbmFzIGRlIEJlbGxvIE1vbnRlIiwiQ29saW5hcyBkZSBTYW50YSBNb25pY2EiLCJDb2xpbmFzIGRlIFZhbGxlIEFycmliYSIsIkNvbGluYXMgZGUgbGEgVHJpbmlkYWQiLCJFbCBCb3NxdWUiLCJFbCBDYWZldGFsIiwiRWwgSGF0aWxsbyIsIkVsIEp1bnF1aXRvIiwiRWwgTWFycXXpcyIsIkVsIFBhcmFpc28iLCJFbCBQbGFjZXIiLCJFbCBSZWNyZW8iLCJFbCBSb3NhbCJdLCJzb3J0IjoiZm9vZCJ9&offset='
        # 600
        URL3 = 'https://www.degustavenezuela.com/caracas/services/search?filters=eyJmaWx0ZXJzIjp7fSwic2NvcmVfcmFuZ2UiOnt9LCJuZWlnaGJvcmhvb2QiOlsiR2FsaXDhbiIsIkd1YXJlbmFzIiwiR3VhdGlyZSIsIkhvcml6b250ZSIsIkxhIEJveWVyYSIsIkxhIENhbGlmb3JuaWEgTm9ydGUiLCJMYSBDYW1wafFhIiwiTGEgQ2FuZGVsYXJpYSIsIkxhIENhcmxvdGEiLCJMYSBDYXN0ZWxsYW5hIiwiTGEgRmxvcmVzdGEiLCJMYSBGbG9yaWRhIiwiTGEgTGFndW5pdGEiLCJMYSBQYXoiLCJMYSBUYWhvbmEiLCJMYSBUcmluaWRhZCIsIkxhIFVuaW9uIiwiTGEgVXJiaW5hIiwiTGFzIEFjYWNpYXMiLCJMYXMgTWVyY2VkZXMiLCJMYXMgUGFsbWFzIiwiTG9tYXMgZGUgU2FuIFJvbWFuIiwiTG9tYXMgZGUgbGEgTGFndW5pdGEiLCJMb21hcyBkZSBsYSBUcmluaWRhZCIsIkxvcyBDYW9ib3MiLCJMb3MgQ2hhZ3VhcmFtb3MiLCJMb3MgQ2hvcnJvcyIsIkxvcyBDb3J0aWpvcyBkZSBMb3VyZGVzIiwiTG9zIERvcyBDYW1pbm9zIiwiTG9zIE5hcmFuam9zIGRlbCBDYWZldGFsIiwiTG9zIE5hcmFuam9zIGRlIGxhcyBNZXJjZWRlcyIsIkxvcyBQYWxvcyBHcmFuZGVzIiwiTG9zIFJ1aWNlcyIsIkxvcyBTYW1hbmVzIiwiTG9zIFRlcXVlcyJdLCJzb3J0IjoiZm9vZCJ9&offset='
        # 470
        URL4 = 'https://www.degustavenezuela.com/caracas/services/search?filters=eyJmaWx0ZXJzIjp7fSwic2NvcmVfcmFuZ2UiOnt9LCJuZWlnaGJvcmhvb2QiOlsiTWFjYXJhY3VheSIsIk1haXF1ZXRpYSIsIk1hbnphbmFyZXMiLCJNYXJpcGVyZXoiLCJNb250YWxiYW4iLCJNb250ZWNyaXN0byIsIlBhcnF1ZSBDYXJhYm9ibyIsIlBhcnF1ZSBDZW50cmFsIiwiUGxhemEgVmVuZXp1ZWxhIiwiUHJhZG9zIGRlbCBFc3RlIiwiU2FiYW5hIEdyYW5kZSIsIlNhbiBBbnRvbmlvIiwiU2FuIEJlcm5hcmRpbm8iLCJTYW4gSm9z6SBkZSBsb3MgQWx0b3MiLCJTYW4gTHVpcyIsIlNhbiBNYXJ07W4iLCJTYW50YSBFZHV2aWdpcyIsIlNhbnRhIEZlIiwiU2FudGEgSW7pcyIsIlNhbnRhIE3zbmljYSIsIlNhbnRhIFBhdWxhIiwiU2FudGEgUm9zYSBkZSBMaW1hIiwiU2FudGEgUm9zYWxpYSIsIlNhbnRhIFNvZu1hIiwiU2VidWNhbiIsIlRlcnJhemFzIGRlbCBBdmlsYSIsIlZhbGxlIEFycmliYSIsIlZhcmdhcyIsIlZpc3RhIEFsZWdyZSIsIlZpemNheWEiXSwic29ydCI6ImZvb2QifQ==&offset='
        URLlist = [URL2, URL3, URL4]
        LengthList = [10, 20, 30]
        for x in range(len(URLlist)):
            list = self.get_names(LengthList[x], URLlist[x])
            details = self.get_details(list, str(LengthList[x]))


# Get all resturant names returned as a list
InfiniteScraper().main_loop()

# https://drive.google.com/drive/folders/1J9S-1rMSLngGv_uWANh6aYVPkvcqa3zI
