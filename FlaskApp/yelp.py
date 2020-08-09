def yelp_scrapper(location):

    from bs4 import BeautifulSoup
    import pandas as pd
    from urllib.request import Request, urlopen
    import re
    import time
    import sys


    #importing module
    import logging

    #Create and configure logger
    logging.basicConfig(filename="yelp.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')

    #Creating an object
    logger=logging.getLogger()

    #Setting the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)



    refined_list = []

    import requests
    import random
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]

    for i in range(0, 990, 30):
        time.sleep(5)
        try:
            site = "https://www.yelp.com/search?find_desc=Restaurants&find_loc="+ location+"&ns1000&start="+str(i)
            logger.debug(site)


            user_agent = random.choice(user_agent_list)
            hdr = {'User-Agent': user_agent}

            #hdr = {'User-Agent': 'Mozilla/5.0'}
            req = Request(site,headers=hdr)
            page = urlopen(req)
            soup = BeautifulSoup(page)

            if soup.find("h3").text == "We're sorry, the page of results you requested is unavailable.":
                break

            href = soup.findAll('link')
            href_list = []
            for link in href:
                a = link['href']
                href_list.append(a)


            rest_list = []
            href = soup.findAll('a')
            for i in range(len(href)):
                try:
                    x = href[i]['href']
                    rest_list.append(x)
                except:
                    logger.debug("hi")
                    #rest_list.append(x)

            rest_list = list(dict.fromkeys(rest_list))
            for i in range(len(rest_list)):
                if ("/biz/") in rest_list[i] and ("?osq") in rest_list[i]:
                    rest_list[i] = "https://www.yelp.com"+rest_list[i]
                    refined_list.append(rest_list[i])
        except:
            logger.debug("hello")

    rerefined_list = list(dict.fromkeys(refined_list))
    logger.debug(len(rerefined_list))



    new_cdf =  pd.read_csv('cool.csv')
    column_name = list(new_cdf.columns)
    df = pd.DataFrame(columns = column_name)



    import re

    import time
    import random
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]
    for k in range(len(rerefined_list)):

        site = rerefined_list[k]
        
        user_agent = random.choice(user_agent_list)
        hdr = {'User-Agent': user_agent}
        req = Request(site,headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page)
        phone = []
        website = []
        ph = ""
        web = ""
        types = ""
        address = ""
        name = ""


        container = soup.findAll("div", {"class":"lemon--div__373c0__1mboc padding-t3__373c0__1gw9E padding-r3__373c0__57InZ padding-b3__373c0__342DA padding-l3__373c0__1scQ0 border--top__373c0__3gXLy border--right__373c0__1n3Iv border--bottom__373c0__3qNtD border--left__373c0__d1B7K border-radius--regular__373c0__3KbYS background-color--white__373c0__2uyKj"})
        l = container[0].findAll("p", {"class": "lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-"})
        #l = ["hello", "abrar.com", "", ""]
        for i in range(len(l)):
            m = l[i].get_text()
            #m = l[i]
            if "." in m:
                website.append(m)
                web = "www." +m

            check = m.replace("+", "").replace("-", '').replace("(", "").replace(")", "")
            if re.match("^[0-9 ]+$", check):
                ph = m




        tags =  soup.findAll('div', {"class" : "lemon--div__373c0__1mboc arrange__373c0__2C9bH gutter-4__373c0__3s8bL border-color--default__373c0__3-ifU"})
        tag = tags[0].findAll('a')

        for i in range(len(tag)-1):
            types = types + tag[i].text +', '



        new_container = soup.findAll("div", {"class":"lemon--div__373c0__1mboc padding-t2__373c0__11Iek padding-r2__373c0__28zpp padding-b2__373c0__34gV1 padding-l2__373c0__1Dr82 border-color--default__373c0__3-ifU"})
        m = new_container[0].findAll('p')
        for i in range(len(m)):
            address = address+ m[i].text +', '

        name = soup.findAll('h1')
        name = name[0].get_text()


        hours = []

        times = tags[1].findAll("div", {"class":"lemon--div__373c0__1mboc border-color--default__373c0__3-ifU"})
        time = times[1].findAll('p')
        for i in range(1, len(time)-1, 2):
            hours.append(time[i].text)
        #logger.debug(i)

        if(len(hours)<7):
            hours = ["", "", "", "", "", "", ""]

        #df = df.append({'Name' : name , 'Address' : address, 'Phone_Number' : ph, "Website" : web, 'types' : types, 'Mon' : hours[0],  'Tue' : hours[1],  'Wed' : hours[2],  'Thu' : hours[3],  'Fri' : hours[4],  'Sat' : hours[5],  'Sun' : hours[6]}, ignore_index=True)
        df = df.append({'name' : name , 'full_address' : address, 'phone_number' : ph, "website" : web, 'description' : types, 'monday_business_hours' : hours[0],  'tuesday_business_hours' : hours[1],  'wednesday_business_hours' : hours[2],  'thursday_business_hours' : hours[3],  'friday_business_hours' : hours[4],  'saturday_business_hours' : hours[5],  'sunday_business_hours' : hours[6]}, ignore_index=True)

        logger.debug(k)
        #time.sleep(5)
        df.to_csv(location +".csv", encoding='utf-8', index=False)
