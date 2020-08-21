import json
import requests
import pandas as pd

key = ""


def regionSearch(area):

    query = area+"+resturants"
    URL = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+query+"&key="+key
    response = json.loads(requests.get(URL).text)
    response = response['results']
    IDlist = []
    for x in response:
        IDlist.append(x['place_id'])
    return IDlist


def resturantSearch(ID):
    fields = "name,formatted_address,type,formatted_phone_number,opening_hours,rating,user_ratings_total"
    URL = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + \
        ID+"&fields="+fields+"&key="+key
    response = json.loads(requests.get(URL).text)['result']

    name.append(response['name'])
    address.append(response['formatted_address'])
    res_type.append(response['types'])
    number.append(response['formatted_phone_number'])
    hours.append(response['opening_hours']['weekday_text'])
    rating.append(response['rating'])
    total_ratings.append(response['user_ratings_total'])


name = []
address = []
res_type = []
number = []
hours = []
rating = []
total_ratings = []

regionList = regionSearch("Valencia")
for x in regionList:
    resturantSearch(x)

df = pd.DataFrame({
    'Name': name,
    'Address': address,
    'Type': res_type,
    'Phone Number': number,
    'Hours': hours,
    'Ratings': rating,
    'Total Ratings': total_ratings
})
df.to_csv(r'MAPdata.csv', index=False, header=True)
