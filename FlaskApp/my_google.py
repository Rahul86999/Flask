def google_scrapper(location):

    from serpwow.google_search_results import GoogleSearchResults
    import json
    import pandas as pd




    #importing module
    import logging

    #Create and configure logger
    logging.basicConfig(filename="google.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')

    #Creating an object
    logger=logging.getLogger()

    #Setting the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)



    ref_csv = pd.read_csv('cool.csv')
    cdf = pd.DataFrame(ref_csv)
    df = pd.DataFrame(columns = cdf.columns)

    import sys
    search = location
    logger.debug(search)
    #search = input("Enter your search: \n")
    page = 50

    # create the serpwow object, passing in our API key
    serpwow = GoogleSearchResults("9F234651FA4E458697C8227C42A090B0")

    for m in range(page):
        x = str(m+1)
        params = {
        "q" : "Restaurant",
        "search_type" : "places",
        "page" : x,
        "gl" : "us",
        "hl" : "en",
        "location" : search,
        "google_domain" : "google.com",
        "device" : "desktop",
        "num" : "20"
        }

        # retrieve the search results as JSON
        result = serpwow.get_json(params)
        info = json.dumps(result, indent=2, sort_keys=True)
        data = json.loads(info)
        if len(data["places_results"]) < 5:
            break

        for i in range(len(data["places_results"])):
            try:
                name = data["places_results"][i]["title"]
            except:
                name = ""
            try:
                address =data["places_results"][i]["address"]
            except:
                address = ""
            try:
                phone = data["places_results"][i]["phone"]
            except:
                phone = ""
            try:
                lat = data["places_results"][i]["gps_coordinates"]["latitude"]
            except:
                lat = ""
            try:
                lon = data["places_results"][i]["gps_coordinates"]["longitude"]
            except:
                lon = ""
            try:
                category = data["places_results"][i]["category"]
            except:
                category = ""
            try:
                descriptions = data["places_results"][i]["extensions"]
            except:
                descriptions = ""
            try:
                sat = data["places_results"][i]["opening_hours"]["per_day"][3]["value"]
            except:
                sat = ""
            try:
                sun = data["places_results"][i]["opening_hours"]["per_day"][4]["value"]
            except:
                sun = ""
            try:
                mon = data["places_results"][i]["opening_hours"]["per_day"][5]["value"]
            except:
                mon = ""
            try:
                tue = data["places_results"][i]["opening_hours"]["per_day"][6]["value"]
            except:
                tue = ""
            try:
                wed = data["places_results"][i]["opening_hours"]["per_day"][0]["value"]
            except:
                wed = ""
            try:
                thu = data["places_results"][i]["opening_hours"]["per_day"][1]["value"]
            except:
                thu = ""
            try:
                fri = data["places_results"][i]["opening_hours"]["per_day"][2]["value"]
            except:
                fri = ""
            try:
                website = data["places_results"][i]["link"]
            except:
                website = ""


            df = df.append({'name' : name , 'full_address' : address, 'phone_number' : phone, "website" : website,  'monday_business_hours' : mon,  'tuesday_business_hours' : tue,  'wednesday_business_hours' : wed,
                            'amenities':descriptions,    'thursday_business_hours' : thu, 'lat':lat, 'long': lon,  'friday_business_hours' : fri,  'saturday_business_hours' : sat,  'sunday_business_hours' : sun}, ignore_index=True)

            df.to_csv(search +".csv", encoding='utf-8', index=False)
