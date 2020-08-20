import requests

key = ""
query = "toronto+resturants"
URL = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+query+"&key="+key

response = requests.get(URL)
source = response.text
print(source)
