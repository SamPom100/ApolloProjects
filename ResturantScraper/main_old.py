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

    def main_loop(self):
        list = []
        for x in range(0, 100, 10):
            sampleText = self.scrape(x)
            resturantNum = sampleText.count(
                'g-color-black g-color-primary--hover g-font-weight-600 g-text-underline--none--hover')
            for y in range(0, resturantNum, 1):
                begin_key = 'g-color-black g-color-primary--hover g-font-weight-600 g-text-underline--none--hover'
                end_key = '<\/a>'
                begin = sampleText.index(begin_key) + 84
                end = sampleText.index(end_key, begin)
                resturantName = sampleText[begin:end]
                cleaned_Name = self.secondKey(resturantName)
                if '\\' in cleaned_Name:
                    index = cleaned_Name.index('\\')
                    cleaned_Name = cleaned_Name[:index]
                list.append(cleaned_Name)
                sampleText = sampleText[begin:]
        return list


# Get all resturants returned as a list
print(InfiniteScraper().main_loop())
