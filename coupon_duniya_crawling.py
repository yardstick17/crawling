import urllib2
from bs4 import BeautifulSoup
home_link = "http://www.coupondunia.in/?ref=nav_logo"

def category_list_link():
	page = urllib2.urlopen(home_link)
	print page
	soup = BeautifulSoup(page , "lxml")
	right_table = soup.find_all('ul' , class_ = 'clearfix') 
	category_link = []
	for link in right_table:
		for l in link.find_all('a'):
			category_link.append(l.get('href'))
	return category_link

def get_sub_links(link):
	sub_category_link , vendor = [] , []
	page = urllib2.urlopen(link)
	soup = BeautifulSoup(page  ,"lxml")
	
	right_table = soup.find_all('div' , class_ = 'online_offer offer-title get-title-code') 
	
	for link in right_table:
		for l in link.find_all('a'):
			sub_category_link.append(l.get('href'))
	right_table = soup.find_all('div' , class_ = 'coupon-big coupon')
	for item in right_table:
		vendor.append(item.get('data-entity-name').encode('utf-8'))
	return sub_category_link , vendor

def get_details_and_update(attached_links , vendors):
	for link , vendor in zip(attached_links , vendors):
		page = urllib2.urlopen(link)
		soup = BeautifulSoup(page)
		right_section = soup.find('div' , class_ = 'coupon-desc-section_new coupon-desc-section text-center')
		
		Offer = right_section.find('h3').text.encode('utf-8')
		Offer_Desc =  right_section.find('p').text.encode('utf-8')

		right_code = soup.find('div' , class_ = 'coupon-code-forward_new coupon-code-forward inline-block')
		try:
			code = right_code.text
		except:
			code = ''
		code = str(code.encode('utf-8')).strip()
		Offer_Code = code
		print(offer , Offer_Desc , vendor , Offer_Code)

if __name__ == '__main__':
	category_link = category_list_link()
	print category_link
	for link in category_link:
		attached_links , vendors = get_sub_links(link)
		get_details_and_update(attached_links , vendors)

