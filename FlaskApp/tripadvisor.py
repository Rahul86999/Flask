def tripadvisor_scrapper(location):

    import pandas as pd
    from bs4 import BeautifulSoup
    from urllib.request import Request, urlopen
    import re
    import sys
    from selenium import webdriver
    import time
    #importing module
    import logging
    import os
    pws = os.getcwd()
    chromedriver = pws+'/chromedriver'
   
    #Create and configure logger
    logging.basicConfig(filename="tripadvisor.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')

    #Creating an object
    logger=logging.getLogger()

    #Setting the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)



    data = pd.read_csv("/home/rahul/Downloads/FlaskLogin/FlaskApp/cool.csv")
    cdf = pd.DataFrame(data)
    df = pd.DataFrame(columns =  cdf.columns)
    df.head()
    q = location

    link_list = []
    site = "https://www.tripadvisor.com/Search?q="+q+"&ssrc=e&rf=1"
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome(chromedriver, chrome_options=options)

    # get source code
    driver.get(site)
    html = driver.page_source
    time.sleep(2)
    #logger.debug(html)


    soup = BeautifulSoup(html)
    try:
        r = soup.find("div", {"class": "qustion-block"})
        logger.debug(r)

        total_page = []
        pages = soup.findAll("a", {"class":"pageNum cx_brand_refresh_phase2"})

        for j in range(len(pages)):
            total_page.append(pages[j]["data-offset"])
        total_page
        ends = int(total_page[-1])+1
    except:
        pass
    try:
        pg_lst = []
        for y in range(0, ends , 30):
            pg_lst.append(str(y))
    except:
        pass
    for k in range(len(pg_lst)):
        site = "https://www.tripadvisor.com/Search?q="+q+"&ssrc=e&o=" + pg_lst[k]
        logger.debug(site)
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome(chromedriver, chrome_options=options)

        driver.get(site)
        html = driver.page_source
        time.sleep(2)
        soup = BeautifulSoup(html)
        a = soup.findAll("div", {"class":"result-title"})

        for l in range(len(a)):
            x = a[l]["onclick"].split()
            for m in range(len(x)):
                if "/Restaurant_Review" in x[m]:
                    sub = x[m].replace("'", "")
                    link = "https://www.tripadvisor.com"+sub
            link_list.append(link)



    driver.close()
    refined_list = list(dict.fromkeys(link_list))
    len(refined_list)



    import json
    api_link = ""
    hours_link = ""
    website_link = ""

    hdr = {'User-Agent': 'Mozilla/5.0'}
    for i in range(len(refined_list)):
        str_op = refined_list[i]
        reg1 = 'd\d+'
        match1 = re.findall(reg1, str_op)
        reg2 = '\d+'
        match2 = re.findall(reg2, match1[0])
        #key.append(match2)
        api_link = "https://www.tripadvisor.com/data/1.0/restaurant/"+ str(match2[0]) +"/overview"
        hours_link = "https://www.tripadvisor.com/data/1.0/location/"+ str(match2[0]) +"/hours"
        website_link = "https://www.tripadvisor.com/data/1.0/location/"+ str(match2[0])


        site1 = api_link
        site2 = hours_link
        site3 = website_link

        try:
            req1 = Request(site1,headers=hdr)
            page1 = urlopen(req1)
            new_soup1 = BeautifulSoup(page1)
        except:
            logger.debug("Bad url")
        try:
            req2 = Request(site2,headers=hdr)
            page2 = urlopen(req2)
            new_soup2 = BeautifulSoup(page2)
        except:
            logger.debug("Bad url")
        try:
            req3 = Request(site3,headers=hdr)
            page3 = urlopen(req3)
            new_soup3 = BeautifulSoup(page3)
        except:
            logger.debug("Bad url")

        try:
            data1 = json.loads(new_soup1.text)
        except:
            data1 = ""
        try:
            data2 = json.loads(new_soup2.text)
        except:
            data2 = ""
        try:
            data3 = json.loads(new_soup3.text)
        
        except:
            data3 = ""

        try:
            name = data1["name"]
        except:
            name = ""
        try:
            address = data1["contact"]["address"]
        except:
            address = ""
        try:
            phone = data1["contact"]['phone']
        except:
            phone = ""
        try:
            email = data1['contact']['email']
        except:
            email = ""
        try:
            website = data3["website"]
            print("website = ",website)
        except:
            website = ""
        #logger.debug(name)
        #logger.debug(address)
        #logger.debug(phone)
        #logger.debug(email)
        #logger.debug(website)
        try:
            lat = data['location']['latitude']
        except:
            lat = ""
        try:
            lon = data['location']['longitude']
        except:
            lon = ""
        #logger.debug(lat)
        #logger.debug(lon)
        try:
            time = data2["allOpenHours"][0]['times'][0]
        except:
            time = ""

        df = df.append({'name' : name , 'full_address' : address, 'phone_number' : phone, "website" : website, "email":email,  'monday_business_hours' : time,  'tuesday_business_hours' : time,  'wednesday_business_hours' : time,
                        'lat':lat, 'long':lon, 'thursday_business_hours' : time,  'friday_business_hours' : time,  'saturday_business_hours' : time,  'sunday_business_hours' : time}, ignore_index=True)

        logger.debug(i)
        df.to_csv(q +".csv", encoding='utf-8', index=False)
