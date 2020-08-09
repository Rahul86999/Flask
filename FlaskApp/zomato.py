def zomato_scrapper(location):

    from bs4 import BeautifulSoup
    import pandas as pd
    from urllib.request import Request, urlopen
    import sys
    import re
    from flask import Flask, escape, request, render_template,flash,redirect, make_response
    

    #importing module
    import logging
    
    #Create and configure logger
    logging.basicConfig(filename="zomato.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')

    #Creating an object
    logger=logging.getLogger()

    #Setting the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)



    search = location
    site = "https://www.zomato.com/"+search+"/restaurants?q=restaurant&page=1"

    href_list = []

    #site = "https://www.zomato.com/jamshedpur/restaurants?q=restaurant&page=10"
    #hdr = {'User-Agent': 'Mozilla/5.0'}

    headers = {
        'User-Agent': 'My User Agent 1.0',
        'From': 'youremail@domain.com'
    }
    import urllib.request, urllib.error
    try:
        req = Request(site,headers=headers)
        page = urllib.request.urlopen(req)
        soup = BeautifulSoup(page,features="html.parser")
    except urllib.error.HTTPError as e:
        # Return code error (e.g. 404, 501, ...)
        print('HTTPError: {}'.format(e.code))
    except urllib.error.URLError as e:
        print('URLError: {}'.format(e.reason))
    else:
        print('working')
    try:
        reg1 = '\d+'
        try:
            match = re.findall(reg1, soup.find("div", {"class":"col-l-4 mtop pagination-number"}).text)[-1]
        except:
            print("match",match)
    except:
        logger.debug("Plese enter a valid url")

    failcase=0

    try:            
        for i in range(1,len(match)):
            site = "https://www.zomato.com/"+search+"/restaurants?q=restaurant&page="+str(i)

            #site = "https://www.zomato.com/jamshedpur/restaurants?q=restaurant&page=10"
            #hdr = {'User-Agent': 'Mozilla/5.0'}

            headers = {
                'User-Agent': 'My User Agent 1.0',
                'From': 'youremail@domain.com'
            }

            req = Request(site,headers=headers)
            page = urlopen(req)
            soup = BeautifulSoup(page,features="html.parser")

            find_a = soup.findAll('a', {'class':'result-title hover_feedback zred bold ln24 fontsize0'})
           
            for i in range(len(find_a)):
                href_list.append(find_a[i]['href'])

        new_cdf =  pd.read_csv('cool.csv')
        column_name = list(new_cdf.columns)
        df = pd.DataFrame(columns = column_name)

        logger.debug(len(href_list))
        for k in range(len(href_list)):
            site = href_list[k]
            #hdr = {'User-Agent': 'Mozilla/5.0'}
            name = ""
            address = ''
            description = ''
            time = ''
            phone_list = []
            headers = {
                'User-Agent': 'My User Agent 1.0',
                'From': 'youremail@domain.com'
            }

            req = Request(site,headers=headers)
            page = urlopen(req)
            new_soup = BeautifulSoup(page)
            name =  new_soup.find('h1').text
            phone = new_soup.findAll('p', {'class':'sc-1hez2tp-0 kKemRh'})
            for i in range(len(phone)):
                    phone_list.append(phone[i].text)

            try:
                address = new_soup.find('p', {'class':'sc-1hez2tp-0 clKRrC'}).text
            except:
                logger.debug("address")
            try:
                description = new_soup.find('div', {'class':'sc-fQkuQJ iSMPWF'}).text
            except:
                logger.debug("description")
            try:
                time =  new_soup.find('span', {'class':"sc-hAXbOi cxBEnh"}).text.replace("(Today)", "")
            except:
                logger.debug("time")
            df = df.append({'name' : name , 'full_address' : address, 'phone_number' : phone_list, 'description' : description, 'monday_business_hours' : time,  'tuesday_business_hours' : time,  'wednesday_business_hours' : time,  'thursday_business_hours' : time,  'friday_business_hours' : time,  'saturday_business_hours' : time,  'sunday_business_hours' : time}, ignore_index=True)
            logger.debug(k)

            df.to_csv(search +".csv", encoding='utf-8', index=False)
    except:
        failcase+=1
        if failcase > 10:
            pass