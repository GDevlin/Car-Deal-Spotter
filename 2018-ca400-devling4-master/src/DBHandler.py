'''
@author: Glen Devlin
'''

import sqlite3
import time
import datetime
import random
import requests

#Connections to database files for SQLite
conn = sqlite3.connect('display_cars.db')

c = conn.cursor()

#conn2 = sqlite3.connect('display_cars.db')
#c2 = conn2.cursor()
'''
#Read cars from a scraped table
def read_scraped_cars():
    c2.execute("""SELECT * FROM scraped_cars""")
    list_of_cars = []
    for row in c2.fetchall():
        list_of_cars.append(row)
    
    return list_of_cars

#Get urls from scraped cars
def get_scraped_urls():
    c2.execute("""SELECT URL FROM scraped_cars""")
    urls_list = []
    for row in c2.fetchall():
        urls_list.append(row[0])
        
    return urls_list
    
#Get ids from 2 database
def ids_from_2_DB():
    training_data = read_training_cars()
    scraped_data = read_scraped_cars()
    print(len(training_data))
    print(len(scraped_data))
    
    list_of_ids_1 = []
    for car in training_data:
        list_of_ids_1.append(car[1])
    
    count = 0    
    for car in scraped_data:
        if car[1] in list_of_ids_1:
            count += 1
        
    print(count)
'''

#Read cars from a training table
def read_training_cars():
    c.execute("""SELECT * FROM training_cars""")
    list_of_cars = []
    for row in c.fetchall():
        list_of_cars.append(row)
    
    return list_of_cars

def read_display_cars():
    c.execute("""SELECT * FROM display_cars""")
    list_of_cars = []
    for row in c.fetchall():
        list_of_cars.append(row)
    
    return list_of_cars
    
#Write predicted price
def write_predicted_price(car_id, predicted_price):
    c.execute("""UPDATE training_cars SET Predicted_Price = ? WHERE ID == ?""", (predicted_price, car_id))
    conn.commit()
      
#Used when price was deleted accidentlly   
def write_price(car_id, price):
    c.execute("""UPDATE training_cars SET Price = ? WHERE ID == ?""", (price, car_id))
    conn.commit()

#Write year  
def write_year(car_id, year):
    c.execute("""UPDATE training_cars SET Year = ? WHERE ID == ?""", (year, car_id))
    conn.commit()

#Fill odometer   
def write_odometer(car_id, odometer):
    c.execute("""UPDATE training_cars SET Odometer = ? WHERE ID == ?""", (odometer, car_id))
    conn.commit()

#Fill owners   
def write_owners(car_id, owners):
    c.execute("""UPDATE training_cars SET Owners = ? WHERE ID == ?""", (owners, car_id))
    conn.commit()
 
 #Fill road tax   
def write_road_tax(car_id, road_tax):
    c.execute("""UPDATE training_cars SET Road_Tax = ? WHERE ID == ?""", (road_tax, car_id))
    conn.commit()

#Fill fuel economy   
def write_fuel_economy(car_id, fuel_economy):
    c.execute("""UPDATE training_cars SET Fuel_Economy = ? WHERE ID == ?""", (fuel_economy, car_id))
    conn.commit()
    
#Create a table for scraped cars    
def create_scraped_data_table():
     c.execute("""CREATE TABLE IF NOT EXISTS scraped_cars(
                                                    URL TEXT, 
                                                    ID TEXT, 
                                                    Make TEXT,
                                                    Model TEXT,
                                                    Year TEXT,
                                                    Price TEXT,
                                                    Odometer TEXT,
                                                    Fuel_Type TEXT,
                                                    Engine_Size TEXT,
                                                    Colour TEXT,
                                                    Body TEXT,
                                                    Owners TEXT,
                                                    Transmission TEXT,
                                                    NCT_Due TEXT,
                                                    Tax_Due TEXT,
                                                    Seats TEXT,
                                                    Road_Tax TEXT,
                                                    Fuel_Economy TEXT,
                                                    Max_Speed TEXT,
                                                    Zero_to_62_mph TEXT,
                                                    Engine_Power Text,
                                                    SIMI_Dealer TEXT,
                                                    Last_Update TEXT,
                                                    County TEXT,
                                                    Status TEXT,
                                                    Date_Scraped Text,
                                                    Predicted_Price)""")

#Add a car to the scraped car table  
def add_scraped_car(car_details):
    url = car_details[0]
    car_id = car_details[1]
    make = car_details[2]
    model = car_details[3]
    year = car_details[4]
    price = car_details[5]
    odometer = car_details[6]
    fuel_type = car_details[7]
    engine_size = car_details[8]
    colour = car_details[9]
    body = car_details[10]
    owners = car_details[11]
    transmission = car_details[12]
    nct_due = car_details[13]
    tax_due = car_details[14]
    seats = car_details[15]
    road_tax = car_details[16]
    fuel_economy = car_details[17]
    max_speed = car_details[18]
    zero_to_62 = car_details[19]
    engine_power = car_details[20]
    simi_dealer = car_details[21]
    last_update = car_details[22]
    county = car_details[23]
    status = car_details[24]
    
    sys_time = time.time()
    date_scraped = str(datetime.datetime.fromtimestamp(sys_time).strftime('%Y-%m-%d %H:%M:%S')) 
    
    c.execute("""INSERT INTO scraped_cars (URL, ID, Make, Model, Year, Price, Odometer, Fuel_Type,
                                    Engine_Size, Colour, Body, Owners, Transmission, NCT_Due, Tax_Due, Seats,
                                    Road_Tax, Fuel_Economy, Max_Speed, Zero_to_62_mph, Engine_Power,
                                    SIMI_Dealer, Last_Update, County, Status, Date_Scraped)
                        Values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (url, car_id, make, model, year, price, odometer, fuel_type, engine_size,
                        colour, body, owners, transmission, nct_due, tax_due, seats, road_tax, fuel_economy,
                        max_speed, zero_to_62, engine_power, simi_dealer, last_update, county, status, date_scraped))
    
#Add a car to the training car table  
def add_training_car(car_details):
    url = car_details[0]
    car_id = car_details[1]
    make = car_details[2]
    model = car_details[3]
    year = car_details[4]
    price = car_details[5]
    odometer = car_details[6]
    fuel_type = car_details[7]
    engine_size = car_details[8]
    colour = car_details[9]
    body = car_details[10]
    owners = car_details[11]
    transmission = car_details[12]
    county = car_details[23]
    road_tax = car_details[16]
    fuel_economy = car_details[17]
    simi_dealer = car_details[21]
    last_update = car_details[22]
    seats = car_details[15]
    
    sys_time = time.time()
    date_scraped = str(datetime.datetime.fromtimestamp(sys_time).strftime('%Y-%m-%d %H:%M:%S')) 
    
    c.execute("""INSERT INTO trainig_cars (URL, ID, Make, Model, Year, Price, Odometer, Fuel_Type,
                                    Engine_Size, Colour, Body, Owners, Transmission, NCT_Due,
                                    Road_Tax, Fuel_Economy, SIMI_Dealer, Last_Update, Date_Scraped, excess)
                        Values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (url, car_id, make, model, year, price, odometer, fuel_type, engine_size,
                        colour, body, owners, transmission, county, road_tax, fuel_economy,
                        simi_dealer, last_update, date_scraped, seats))
    
#Used when data was in wrong columns
#Before scraper was fixed
def update_car(car_details):
    url = car_details[0]
    car_id = car_details[1]
    make = car_details[2]
    model = car_details[3]
    year = car_details[4]
    price = car_details[5]
    odometer = car_details[6]
    fuel_type = car_details[7]
    engine_size = car_details[8]
    colour = car_details[9]
    body = car_details[10]
    owners = car_details[11]
    transmission = car_details[12]
    nct_due = car_details[13]
    road_tax = car_details[14]
    fuel_economy = car_details[15]
    simi_dealer = car_details[16]
    last_update = car_details[17]
    date_scraped = car_details[18]
    excess = car_details[19]
    
    c.execute("""UPDATE cars SET URL = ?, ID = ?, Make = ?, Model = ?, Year = ?, Price = ?, Odometer = ?, Fuel_Type = ?,
                                    Engine_Size = ?, Colour = ?, Body = ?, Owners = ?, Transmission = ?, NCT_Due = ?,
                                    Road_Tax = ?, Fuel_Economy = ?, SIMI_Dealer = ?, Last_Update = ?, Date_Scraped = ?,
                                    excess = ? WHERE ID = ?""",
                        (url, car_id, make, model, year, price, odometer, fuel_type, engine_size,
                        colour, body, owners, transmission, nct_due, road_tax, fuel_economy,
                        simi_dealer, last_update, date_scraped, excess, car_id))
    
    conn.commit()
    
#Get exisitng urls from a table
def get_exisitng_urls():
    c.execute("""SELECT URL FROM training_cars""")
    urls_list = []
    for row in c.fetchall():
        urls_list.append(row[0])
        
    return urls_list

##-----MySQL-Server-----
#Adds a car to the MySQL DB on pyhton anywhere
def upload_trainging_data():
    training_cars = read_training_cars()
    
    training_cars = training_cars[8675:]
    
    print(training_cars[0])
    count = 0
    for car in training_cars:
        print()
        #car = list(training_cars[0])
        car = list(car)
        car[0] = car[0].replace('/', 'FORWARDSLASH')
        car[0] = car[0].replace('?', 'QUESTIONMARK')
        car[0] = car[0].replace('%', 'PERCENTAGESIGN')
        car[21] = str(car[21])
        end_of_url = '/'.join(car)
        
        whole_url = "http://gdevlin.pythonanywhere.com/add_training_car/" + end_of_url
        print(whole_url)
        #req = requests.post('http://gdevlin.pythonanywhere.com/add_training_car/%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s' % car[0] % car[1] % car[2] % car[3] % car[4] % car[5] % car[6] % car[7] % car[8] % car[9] % car[10] % car[11] % car[12] % car[13] % car[14] % car[15] % car[16] % car[17] % car[18] % car[19] % car[20] % car[21])
        
        count += 1
        print(count)
        
        #Going to url with variables in url
        #adds car to database
        req = requests.get(whole_url)
        print(req.text)
        
    print("Done!")
    
def upload_display_data():
    display_cars = read_display_cars()
    
    print(display_cars[0])
    count = 0
    for car in display_cars:
        print()
        #car = list(training_cars[0])
        car = list(car)
        car[0] = car[0].replace('/', 'FORWARDSLASH')
        car[0] = car[0].replace('?', 'QUESTIONMARK')
        car[0] = car[0].replace('%', 'PERCENTAGESIGN')
        car[13] = car[23]
        car[14] = "410"#car[16]
        car[15] = car[17]
        car[16] = car[21]
        car[17] = car[21]
        car[18] = car[22]
        car[19] = car[24]
        car[20] = "3100"#car[27]
        car[21] = "310"#car[28]
        car = car[0:22]
        print(car)
        end_of_url = '/'.join(car)
        
        whole_url = "http://gdevlin.pythonanywhere.com/add_display_car/" + end_of_url
        print(whole_url)
        #req = requests.post('http://gdevlin.pythonanywhere.com/add_training_car/%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s' % car[0] % car[1] % car[2] % car[3] % car[4] % car[5] % car[6] % car[7] % car[8] % car[9] % car[10] % car[11] % car[12] % car[13] % car[14] % car[15] % car[16] % car[17] % car[18] % car[19] % car[20] % car[21])
        
        count += 1
        print(count)
        
        #Going to url with variables in url
        #adds car to database
        req = requests.get(whole_url)
        print(req.text)
        
    print("Done!")
    
def set_predicted_price_display(car_id):
    training_cars = read_training_cars()
    display_cars = read_display_cars()
    
    for car_t in training_cars:
        for car_d in display_cars:
            #If they have the same id
            if car_t[1] == car_d[1]:
                car_id = car_d[1]
                car_predicted_price = car_t[20]
                price_diff = car_t[21]
                c.execute("""UPDATE display_cars Set Predicted_Price = ?, Price_Diff = ? WHERE ID = ?""",
                                car_predicted_price, price_diff, car_id)
            conn.commit()
    
        
#Close cursors
def close_cursor():
    c.close()
    #c2.close()
    
    
    
if __name__ == '__main__':
    #create_cars_table()
    #create_scraped_data_table()
    #add_car()
    #get_exisitng_urls()
    #write_predicted_price("1932784", "22,000")
    #upload_trainging_data()
    upload_display_data()
    #add_to_test_table()
    #ids_from_2_DB()


