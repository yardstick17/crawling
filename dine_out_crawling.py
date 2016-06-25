import urllib2
# import MySQLdb
import json
import os
from time import sleep
from bs4 import BeautifulSoup

home_link = 'https://www.eazydiner.com/bengaluru/dine-out?page='
page_number = 1
final_restaurant = []


def get_next_page_link():
    global page_number
    page_number += 1
    return home_link + str(page_number - 1)


def category_list_link():
    page = urllib2.urlopen(home_link)
    soup = BeautifulSoup(page)
    right_table = soup.find_all('ul', class_='clearfix')
    category_link = []
    for link in right_table:
        for l in link.find_all('a'):
            category_link.append(l.get('href'))
    return category_link


def get_sub_links(link):
    sub_category_link, vendor = [], []
    page = urllib2.urlopen(link)
    soup = BeautifulSoup(page)

    right_table = soup.find_all(
        'div', class_='online_offer offer-title get-title-code')

    for link in right_table:
        for l in link.find_all('a'):
            sub_category_link.append(l.get('href'))
    right_table = soup.find_all('div', class_='coupon-big coupon')
    for item in right_table:
        vendor.append(item.get('data-entity-name').encode('utf-8'))
    return sub_category_link, vendor


def get_sub_page_link(page_link):
    sub_page_link = []
    page = urllib2.urlopen(page_link)
    soup = BeautifulSoup(page)
    restaurant_section = soup.find_all('div', class_='details_left left')

    for link in restaurant_section:
        for sub_link in link.find_all('h2', {"class": "restro_title"}):
            for l in sub_link.find_all('a'):
                x = l.get('href')
                sub_page_link.append('https://www.eazydiner.com' + str(
                    x.encode('utf-8')))

    return sub_page_link


def get_deals_detail(current_page, sub_page_link):
    global final_restaurant
    total_scanned = 0
    count = 1
    for link in sub_page_link:
        if not os.path.isfile('bengaluru/' + str(current_page) + '_' + str(
                total_scanned) + '_Delhi_NCR.json'):
            try:
                print 'sub_page_link : ', count
                count += 1
                City, Address, Tele, Timing = [], [], [], []
                D = {}
                page = urllib2.urlopen(link)
                soup = BeautifulSoup(page)

                price_range = soup.find_all('div',
                                            class_='details_pline area price')
                for sec in price_range:
                    for price in sec.find_all('div',
                                              {"itemprop": "priceRange"}):
                        D['price_range'] = price.text.encode('utf-8').strip()

                restaurant_deatils = soup.find_all('div',
                                                   class_='details_line')
                for detail in restaurant_deatils:
                    for det in detail.find_all('span',
                                               {"itemprop": "addressRegion"}):
                        D['city'] = det.text.encode('utf-8').strip()

                    for det in detail.find_all('div',
                                               {"itemprop": "streetAddress"}):
                        D['address'] = det.text.encode('utf-8').strip()

                    for det in detail.find_all('span',
                                               {"itemprop": "telephone"}):
                        Tele.append(det.text.encode('utf-8').strip())

                    D['telephone_number'] = Tele

                for detail in restaurant_deatils:
                    for det in detail.find_all(
                            'div', {"class": "details_pline area"}):
                        D['timing'] = det.text.encode('utf-8').strip()

                restaurant_name = soup.find('div', class_='hotel_name')
                for name in restaurant_name.find_all('h1'):
                    D['res_name'] = name.get('title').encode('utf-8').strip()
                    break
                deal = soup.find('div', class_='eazydeal_text details')
                D['deal'] = deal.text.encode('utf-8').strip()
                deal_deatils = soup.find('div',
                                         class_='navs resturant_details')
                D['deal_deatils'] = deal_deatils.text.encode('utf-8').strip(
                ).split('\n')
                final_restaurant.append(D)

                print 'Res Details : ', D
                with open('bengaluru/' + str(current_page) + '_' +
                                  str(total_scanned) + '_bengaluru.json',
                          'w') as outfile:
                    json.dump(D, outfile)
            except:
                sleep(10)
                print 'Err...'
                pass
        else:
            print 'Already present...'
        total_scanned += 1


if __name__ == '__main__':
    current_page = 1
    max_page = 393
    time_ = 5
    while page_number < max_page:
        try:
            print 'PG : ', page_number
            sleep(time_)
            page_link = get_next_page_link()
            print 'Crawling ', page_link
            sub_page_link = get_sub_page_link(page_link)
            get_deals_detail(page_number, sub_page_link)
            time_ = 10
        except:
            time_ = 10
