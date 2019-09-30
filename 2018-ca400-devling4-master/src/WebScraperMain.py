'''
@author: Glen Devlin

    Web Scraper
        Enter make and model number of car
        Creates Table in none exists in database
        Constructs First page of listing use make and model
        Get total Number of listings pages
        Get url from every add on each of these pages
        Get urls that are already in the database to prevent duplicates
        Loop through urls:
            Get car details
                get url, id, county and all other attributes
            Add car to database
            sleep for 1 second
        Close connection to database
        
        Also method to test single url
        
        Car Make and Model Number:
        Audi: 7         A4: 43
        BMW: 10         3 Series: 86
                        5 Series: 87
        Ford: 26        Focus: 253
        Opel: 63        Astra: 868
        
        Nissan: 61      Qashqai: 1145
        Skoda: 80       Octavia: 682
        Volkswagen: 93  Passat: 817
                        Golf: 812
'''


from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from DBHandler import add_scraped_car, get_scraped_urls
from DBHandler import create_scraped_data_table
from DBHandler import close_cursor
import time

#Get response from URL, return response content
def get_url(url):
    try:
        with closing(get(url, stream = True)) as resp:
            if good_response(resp):
                return resp.content
            else:
                return None
            
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

#Check is response is good
def good_response(resp):
    content_type = resp.headers['Content-type'].lower()
    return(resp.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)
 
#log if issue
def log_error(e):
    print(e)

#Get car features from page
def get_car_details(url):
    response = get_url(url)
    car_id = get_car_id(url)
    
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        
        car_details = []
        car_details.append(url)
        car_details.append(car_id)
        
        for td in html.select('td'):
            for detail in td.text.split('\n'):
                car_details.append(detail.strip())
                            
    return car_details[:18]

#Same as above, except now retrieves more features including county
def improved_get_car_details(url):
    response = get_url(url)
    car_id = get_car_id(url)
    
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        
        car_details = []
        car_details.append(url)
        car_details.append(car_id)
        
        county = 'Not Available'
        counties = ['antrim', 'armagh', 'carlow', 'cavan', 'clare', 'cork', 'derry', 'donegal',
                    'down', 'dublin', 'fermanagh', 'galway', 'kerry', 'kildare', 'kilkenny', 'laois', 
                    'leitrim', 'limerick', 'longford', 'louth', 'mayo', 'meath', 'monaghan', 'offaly',
                    'roscommon', 'sligo', 'tipperary', 'tyrone', 'waterford', 'westmeath', 'wexford', 'wicklow']
        
        address = str(html.select('address')).lower()
        for count in counties:
            if count in address:
                county = count
                
        for td in html.select('tr'):
            for detail in td.text.split('\n'):
                if not detail == '':
                    car_details.append(detail.strip())
    
    sorted_car_details = sort_car_details(car_details)
    sorted_car_details.append(county)
    sorted_car_details.append('Active')#If car was just scraped it is assumed active
    return sorted_car_details

#Makes sure car feautres are in the right column
def sort_car_details(car_details):
    sorted_details = []
    sorted_details.extend(car_details[0: 2])
    
    attributes = ['Make:', 'Model:', 'Year:', 'Price:', 'Odometer:', 'Fuel type:', 'Engine size:', 'Colour:', 
                  'Body:', 'Owners:', 'Transmission:', 'NCT due date:', 'Tax due date:', 'Seats:',
                  'Annual road tax:', 'Fuel economy:', 'Max speed:', '0-62 mph:', 'Engine power:',
                  'SIMI dealer:', 'Last update:']
    
    for attr in attributes:
        if attr in car_details:
            sorted_details.append(car_details[car_details.index(attr) + 1])
        else:
            sorted_details.append('')
        
    return sorted_details
        
#Gets car id from the url
def get_car_id(url):
    car_id = []
    curr_char = 44
    while(url[curr_char].isdigit()):
        car_id.append(url[curr_char])
        curr_char += 1
    
    return ''.join(car_id)
       
def get_num_of_page_listings(url):
    print("Get the number of listings pages")
    page_response = get_url(url)
    
    num_page_listings = 0
    if page_response is not None:
        page_html = BeautifulSoup(page_response, 'html.parser')
        for a in page_html.findAll('a', href = True):
            if a['href'][:15] == "/search-results" and a.text.isdigit():
                if int(a.text) > num_page_listings:
                    num_page_listings = int(a.text)
    
    return num_page_listings


def construct_listing_page(make, model, page):
    return ('https://www.carsireland.ie/search-results.php?make_id=' 
            + make + '&model_id='
            + model + '&page=' + str(page) + '#listings-top')
        
        
#Get all car urls on page
def get_car_urls(listing_url):
    page_response = get_url(listing_url)
    
    car_urls = set()
    if page_response is not None:
        page_html = BeautifulSoup(page_response, 'html.parser')
        for a in page_html.find_all('a', href=True):
            if a['href'][:17] == "/detail.php?ad_id":
                car_urls.add('https://www.carsireland.ie' + a['href'])
        
    return list(car_urls)

def get_mult_car_urls(listing_url, num_listing_pages):
    mult_car_urls = set()
    index = 0
    while(index < num_listing_pages):
        car_urls_list = get_car_urls(listing_url)
        for row in car_urls_list:
            mult_car_urls.add(row)
            
        time.sleep(1)
        index += 1
        print("Getting listings for urls: ", index)
        listing_url = construct_listing_page(make, model, index) #Uncommented#
            
    return list(mult_car_urls)
   
#Test a single url for return features
def test_single_url(): 
    url = 'https://www.carsireland.ie/detail.php?ad_id=1940999&r=s.php%3Fm%3D10%26o%3D87%26g%3D2'
    car_details = improved_get_car_details(url)
    print(car_details)
    
    for c in car_details:
        if ':' in c:
            print(c)
    
if __name__ == '__main__':
    print('Enter make and model nummber')
    make = input("Make: ")
    model = input("Model: ")
    
    #Set up database if none exists
    create_scraped_data_table()
    
    #Get first listing page
    listing_url = construct_listing_page(make, model, 0)
    print("Starting at page: ", listing_url)

    #Get the number of pages
    num_listing_pages = get_num_of_page_listings(listing_url)
    print(num_listing_pages)
    
    #Get urls for car pages
    car_urls = get_mult_car_urls(listing_url, num_listing_pages)
    
    #Get details from urls and add them to database
    car_count = 0
    existing_urls = get_scraped_urls()
    for url in car_urls:
        if url not in existing_urls:
            car_details = improved_get_car_details(url)
            add_scraped_car(car_details)
            car_count += 1
            print("Cars completed:", car_count)
            time.sleep(1)
        
    #Close DataBase
    close_cursor()
    
    print("Done!")
    
    #test_single_url()
    
    
    