import np_parkCodes
import requests
import demjson


def trail_search(NP_name):

    url = "https://jonahtaylor-national-park-service-v1.p.rapidapi.com/places"

    if NP_name in np_parkCodes.np_codes:
        usr_search = np_parkCodes.np_codes[NP_name]
        parkCode = usr_search['parkCode']
        # print (type(parkCode))
        # print(NP_name)
        # print(usr_search['parkCode'])
    else:
        print("Please enter a valid search")
    
    querystring = {"parkCode":parkCode,"q":"hiking","fields":"title, url, listingDescription, images, relatedParks, latlong, bodyText"}

    headers = {
	    "X-Api-Key": ' < API Key Here >',
	    "X-RapidAPI-Host": "jonahtaylor-national-park-service-v1.p.rapidapi.com",
	    "X-RapidAPI-Key": "< API Key Here >"
    }
    
    NP_response = requests.request("GET", url, headers=headers, params=querystring)

    NP_Array = demjson.decode(NP_response.text)

    return NP_Array

# NP_Name=input('search: ')
# NP_Array = trail_search(NP_Name)

# print(NP_Array)

# Fields that we want included: "title", "url", "listingDescription", "images", "relatedParks", "latlong". "bodyText", 

