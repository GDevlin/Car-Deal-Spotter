'''
@author: Glen Devlin
'''

from DBHandler import read_training_cars
from DBHandler import close_cursor
from DBHandler import update_car
from random import shuffle
import re
import DBHandler
import numpy as np
from _collections import defaultdict
from collections import Counter

##---------- Functions for inspecting data ----------
#Following functions will print out and car which doens't have the corresponding feature

def check_makes(cars):
    car_makes = ['Audi', 'Volkswagen', 'Nissan', 'Skoda', 'Ford', 'Opel']
    for row in cars:
        if row[2] not in car_makes:
            print(row)
            
def check_models(cars):
    car_models = ['A4', '5 Series', '520', '525', '523', '530', 'M5', '535', '518', '3 Series', '318', '325', '316', '320', 'M3', '335', '330', 'Focus', 'Golf', 'Passat', 'Octavia', 'Astra', 'Qashqai', 'Qashqai +2']
    for row in cars:
        if row[3] not in car_models:
            print(row)
    
def check_year(cars):
    for row in cars:
        if not row[4][0:4].isdigit():
            print(row)
            
def check_price(cars):
    count = 0
    for row in cars:
        num = row[5][1:]
        num = num.replace(',','')
        if not num.isdigit():
            print(row)
            count += 1
    
    print(count)
    
def check_odometer(cars):
    for row in cars:
        if 'miles' not in row[6] and 'Unspecified' not in row[6]:
            print(row)
            
def check_fuel_type(cars):
    fuel_types = ['Petrol', 'Diesel', 'Hybrid', 'Electric', 'Unknown']
    for row in cars:
        if row[7] not in fuel_types:
            print(row)
            
def check_engine_size(cars):
    for row in cars:
        engine = row[8].replace('.', '')
        acceptable_answers = ['Unknown', '4.0 & above', 'under 1.0']
        if not engine.isdigit() and row[8] not in acceptable_answers:
            print(row)
            
#Colour
def check_colours(cars):
    colours = ['red', 'yellow', 'black', 'white', 'blue', 'grey', 'green', 'orange', 
                    'brown', 'silver', 'beige', 'bronze', 'pearl', 'gold', 'wine', 'purple', 'metallic',
                    'burgundy', 'caffe latte', 'carbon flash', 'silky shadow', 'macadamia', 'maroon', 'nightshade',
                    'cashmere', 'Navy']
    for row in cars:
        colour_present = False
        for c in colours:
            if c in row[9].lower():
                colour_present = True
            
        if colour_present == False:
            print(row[5:])
        
        
#Body
def check_body(cars):
    bodies = ['saloon', 'hatchback', 'estate', 'mpv', 'suv', 'van', 'convertible', 'coupe', 'other']
    for row in cars:
        if row[10].lower() not in bodies:
            print(row)
                    
#Owners
def check_owners(cars):
    acceptable_answers = ['','1','2','3','4','5','5 or more','6','7', '8', '9', '10']
    for row in cars:
        if row[11] not in acceptable_answers:
            print(row[11:])

#Transmission            
def check_transmission(cars):
    count = 0
    transmissions = ['Automatic', 'Manual']
    for row in cars:
        if row[12] not in transmissions:
            print(row)
            count += 1
            
    print(count)

#NCT 
def check_nct(cars):
    count = 0
    for row in cars:
        try:
            if not row[13][0] == '\u20ac':#Euro Sign
                print(row[13:]) 
                count += 1
        except IndexError:
            pass
    print(count)
    

    
    
#Road Tax
##--------- Fix Row
#Boolean functions used to check if feature is okay
def is_make_correct(make):
    car_makes = ['Audi', 'Volkswagen', 'BMW', 'Nissan', 'Skoda', 'Ford', 'Opel']
    if make in car_makes:
        return True

def is_model_correct(model):
    car_models = ['A4', '5 Series', '520', '525', '523', '530', 'M5', '535', '518', 
                  '3 Series', '318', '325', '316', '320', 'M3', '335', '330', 'Focus', 
                  'Golf', 'Passat', 'Octavia', 'Astra', 'Qashqai', 'Qashqai +2']
    if model in car_models:
        return True
    
def is_year_correct(year):
    if year[0:4].isdigit():
        if int(year[0:4]) > 1900 and int(year[0:4]) < 2020:
            return True

def is_price_correct(price):
    ##print("price", price)
    if not len(price) == 0:
        if price[0] == '\u20ac':
            price_number = price[1:]
            price_number = price_number.replace(',','')
            if price_number.isdigit() or price == 'POA':
                return True
        elif price == 'POA':
            return True
    
def is_odometer_correct(odometer):
    if 'miles' in odometer or 'Unspecified' in odometer:
        return True

def is_fuel_type_correct(fuel):
    fuel_types = ['Petrol', 'Diesel', 'Hybrid', 'Electric', 'Unknown']
    if fuel in fuel_types:
        return True
    
def is_engine_size_correct(engine_size):
    #engine_size_trimmed = engine_size.replace('.', '')
    acceptable_answers = ['Unknown', '4.0 & above', 'under 1.0']
    if engine_size in acceptable_answers or ('.' in engine_size and 'seconds' not in engine_size):
        return True    
    
def is_colour_correct(colour):
    colours = ['red', 'yellow', 'black', 'white', 'blue', 'grey', 'green', 'orange', 
                    'brown', 'silver', 'beige', 'bronze', 'pearl', 'gold', 'wine', 'purple', 'metallic',
                    'burgundy', 'caffe latte', 'carbon flash', 'silky shadow', 'macadamia', 'maroon', 'nightshade',
                    'cashmere', 'Navy', 'Lava', 'IMPERIAL', ' SPACE', 'Jatoba', 'ALPINE', 'DEEP SEA', 
                    'CALLISTO', 'Semi-auto', 'SPACE', 'Carbon Schwarz', 'Havanna', 'Sophisto Gray', 
                    'Alpine', ' Other', 'Alpinweiss', 'SOPHISTO', 'SAPPIRE', 'Carbon', ' ALPINE', 
                    'TITANIUM', 'CARBON', 'SOPHISTICO', ' NAVY MET', 'ROYAL', 'NAVY', 'SOPISTO', 
                    'SOPHISTO', 'Mineral', 'Arctic', 'MINERAL', 'MELBOURNE', 'Sparkling Graphite', 
                    'Turquoise', 'Monaco', 'Navy', 'panther', 'BURGANDY', 'MOONDUST', 'magnetic', 
                    'CHILL', 'Moondust', 'Chill', 'LUNAR SKY', 'Magnetic', 'lunar sky', 'Lunar Sky', 
                    'MAGNETIC', 'moondust', 'Frozen', ' Magnetic', 'Lunar', 'SLATE', 'Panther', 'DARK MICA', 
                    'Techtonic', 'shadow', 'DEEP IMPACT', 'Lunar Sky', 'Avalon', 'MINIGHT SKY', 'navy', 
                    'MICASTONE', ' Frozen', 'CARIBOU', 'Denim', ' Night Shadow', 'deep impace', 'GUN METAL', 
                    'Carbon Steel', 'MIDNIGHT', 'GREAY', 'CORRIDA', 'BEIGH', 'GRAY', 'CAPPUCCINO', 'Undefined']

    
    for col in colours:
        if col.lower() in colour.lower():
            return True
        
def is_body_correct(body):
    bodies = ['saloon', 'hatchback', 'estate', 'mpv', 'suv', 'van', 'convertible', 'coupe', 'other']
    if body.lower() in bodies:
        return True
    
def is_owner_correct(owner):
    acceptable_answers = ['','1','2','3','4','5 or more']
    if owner in acceptable_answers:
        return True
    
def is_transmission_correct(transmission):
    acceptable_answers = ['Automatic', 'Manual', 'Semi-auto']
    if transmission in acceptable_answers:
        return True
    
def is_nct_correct(nct):
    months = ['january', 'february', 'march',
              'april', 'may', 'june', 'july',
              'august', 'september', 'october'
              'november', 'december']
    for mon in months:
        if mon in nct.lower():
            return True
    
def is_road_tax_correct(road_tax):
    if not len(road_tax) == 0:
        road_tax = road_tax.replace(',','')
        road_tax_num = re.sub('[^0-9]','',road_tax)
        if road_tax[0] == '\u20ac' and int(road_tax_num) < 1000:
            return True


def is_fuel_economy_correct(fuel_economy):
    if 'MPG' in fuel_economy:
        return True

#Clean Coresping features
def clean_price(list_of_cars):
    for car in list_of_cars:
        price = car[5].replace("\u20ac",'')
        price = price.replace(',','')
        DBHandler.write_price(car[1], price)
        
def clean_year(list_of_cars):
    for car in list_of_cars[89:]:
        year = car[4]
        if len(year) == 10:
            if year[8] == '1':
                year = year[0:4]
                print(year)
                DBHandler.write_year(car[1], year[0:4])
            else:
                year = float(year[0:4]) + 0.5
                print(year)
                DBHandler.write_year(car[1], str(year))
        else:
            print(year)
            DBHandler.write_year(car[1], str(year))
                    
def clean_odometer(list_of_cars):
    for car in list_of_cars:
        odometer = car[6]
        if 'miles' in odometer:
            space_index = odometer.find(' ')
            odometer = odometer[:space_index]
            odometer = odometer.replace(',','')
            DBHandler.write_odometer(car[1], odometer)

def generalise_colour(list_of_cars):
    return 0

def fix_row(car):
    #car = ['A4', 'Audi', '2017', "27,500", '57,918 /93,207 km', 'Electric', '1.4', 'light yellow',
                #'Hatchback', '5 or more', 'Manual', 'feb 2020', '400', '55 MPG', 'n', 'm']
    
    incorrect_attributes = []
    #Check if each row attribute is correct
    make_correct = is_make_correct(car[0])
    if make_correct == None:
        incorrect_attributes.append(car[0])
    #print("Make", make_correct)
    
    #Model
    model_correct = is_model_correct(car[1])
    if model_correct == None:
        incorrect_attributes.append(car[1])
    #print("Model", model_correct)
    
    #Year
    year_correct = is_year_correct(car[2])
    if year_correct == None:
        incorrect_attributes.append(car[2])
    #print("Year", year_correct)
    
    #Price
    price_correct = is_price_correct(car[3])
    if price_correct == None:
        incorrect_attributes.append(car[3])
    #print("Price", price_correct)
    
    #Odometer
    odometer_correct = is_odometer_correct(car[4])
    if odometer_correct == None:
        incorrect_attributes.append(car[4])
    #print("Odometer", odometer_correct)
    
    #Fuel Type
    fuel_type_correct = is_fuel_type_correct(car[5])
    if fuel_type_correct == None:
        incorrect_attributes.append(car[5])
    #print("Fuel Type", fuel_type_correct)
    
    #Engine Size
    engine_size_correct = is_engine_size_correct(car[6])
    if engine_size_correct == None:
        incorrect_attributes.append(car[6])
    #print("Engine size", engine_size_correct)
    
    #Colours - fix later
    colour_correct = is_colour_correct(car[7])
    if colour_correct == None:
        incorrect_attributes.append(car[7])
    #print("Colour", colour_correct)
    
    #Body
    body_correct = is_body_correct(car[8])
    if body_correct == None:
        incorrect_attributes.append(car[8])
    #print("Body", body_correct)
    
    #Owners
    owner_correct = is_owner_correct(car[9])
    if owner_correct == None:
        incorrect_attributes.append(car[9])
    #print("Owner", owner_correct)
    
    #transmission
    transmission_correct = is_transmission_correct(car[10])
    if transmission_correct == None:
        incorrect_attributes.append(car[10])
    #print("Transmission", transmission_correct)
    
    
    #nct
    nct_correct = is_nct_correct(car[11])
    if nct_correct == None:
        incorrect_attributes.append(car[11])
    #print("NCT", nct_correct)
    
    #Road tax
    road_tax_correct = is_road_tax_correct(car[12])
    if road_tax_correct == None:
        incorrect_attributes.append(car[12])
    #print("Road Tax", road_tax_correct)
    
    #Fuel Economy
    fuel_economy_correct = is_fuel_economy_correct(car[13])
    if fuel_economy_correct == None:
        incorrect_attributes.append(car[13])
    #print("Fuel Economy", fuel_economy_correct)
    
    
    #columns that will no longer be used but contain other columns values
    incorrect_attributes.append(car[14])
    incorrect_attributes.append(car[15])
    
    #print(car)
    
    #print(incorrect_attributes)
    
    ##assign incorrect attributes to right place
    #Make - 0
    if make_correct == None:
        for attr in incorrect_attributes:
            if(is_make_correct(attr)) == True:
                car[0] = attr
                incorrect_attributes.remove(attr)
                break
            else:
                car[0] = ''
    
    #Model - 1          
    if model_correct == None:
        for attr in incorrect_attributes:
            if(is_model_correct(attr)) == True:
                car[1] = attr
                incorrect_attributes.remove(attr)
                break
            else:
                car[1] = ''
        
    #Year - 2
    if year_correct == None:
        for attr in incorrect_attributes:
            if(is_year_correct(attr)) == True:
                car[2] = attr
                incorrect_attributes.remove(attr)
                break
            else:
                car[2] = ''
    
    #Price - 3
    if price_correct == None:
        for attr in incorrect_attributes:
            if(is_price_correct(attr)) == True:
                car[3] = attr
                incorrect_attributes.remove(attr)
                break
            else:
                car[3] = ''
    
    #Odometer - 4
    if odometer_correct == None:
        for attr in incorrect_attributes:
            if(is_odometer_correct(attr)) == True:
                car[4] = attr
                incorrect_attributes.remove(attr)
                break
            else:
                car[4] = ''
                
    #Fuel Type - 5
    if fuel_type_correct == None:
        for attr in incorrect_attributes:
            if(is_fuel_type_correct(attr)) == True:
                car[5] = attr
                incorrect_attributes.remove(attr)
                break
            else:
                car[5] = ''
    
    #Engine Size - 6
    if engine_size_correct == None:
        for attr in incorrect_attributes:
            if(is_engine_size_correct(attr)) == True:
                car[6] = attr
                incorrect_attributes.remove(attr)
                break
            else:
                car[6] = ''
                
    #Colour - 7
    if colour_correct == None:
        for attr in incorrect_attributes:
            if(is_colour_correct(attr)) == True:
                car[7] = attr
                incorrect_attributes.remove(attr)
                break
            else:
                car[7] = ''
                
    #Body - 8
    if body_correct == None:
        for attr in incorrect_attributes:
            if(is_body_correct(attr)) == True:
                car[8] = attr
                incorrect_attributes.remove(attr)
                break
            else:
                car[8] = ''
                
    #Owner - 9
    if owner_correct == None:
        for attr in incorrect_attributes:
            if(is_owner_correct(attr)) == True:
                car[9] = attr
                incorrect_attributes.remove(attr)
                break
            else:
                car[9] = ''
                
    #Transmission - 10
    if transmission_correct == None:
        for attr in incorrect_attributes:
            if(is_transmission_correct(attr)) == True:
                car[10] = attr
                incorrect_attributes.remove(attr)
                break
            else:
                car[10] = ''
                
    #NCT - 11
    if nct_correct == None:
        for attr in incorrect_attributes:
            if(is_nct_correct(attr)) == True:
                car[11] = attr
                incorrect_attributes.remove(attr)
                break
            else:
                car[11] = ''
                
    #Road Tax - 12
    if road_tax_correct == None:
        for attr in incorrect_attributes:
            if(is_road_tax_correct(attr)) == True:
                car[12] = attr
                incorrect_attributes.remove(attr)
                break
            else:
                car[12] = ''
                
    #Fuel Economy - 13
    if fuel_economy_correct == None:
        for attr in incorrect_attributes:
            if(is_fuel_economy_correct(attr)) == True:
                car[13] = attr
                incorrect_attributes.remove(attr)
                break
            else:
                car[13] = ''
                
    #print(car)
    #print(incorrect_attributes)
    #Turn incorrect attributes into one string
    excess = ",".join(incorrect_attributes)
    #print(excess)
    car.append(excess)
    return car

#Fixes cars by finding the best place for each feature
#Does not mess with features it deems correct
def fix_cars(cars):
    total_excess = []
    count = 0
    for car in cars:
        car_url = car[0]
        car_id = car[1]
        car_date_scraped = car[18]
        
        clean_car = fix_row(list(car[2:18]))
        car_excess = clean_car[len(clean_car)-1].split(',')
        
        clean_car.insert(0, car_url)
        clean_car.insert(1, car_id)
        clean_car.insert(18, car_date_scraped)
        
        for ex in car_excess:
            if ex not in total_excess:
                total_excess.append(ex)
                
        update_car(clean_car)
        
        count += 1
        if count % 10 == 0:
            print(count)  

#Used to fix prices that were accidentally deleted           
def car_get_prices(list_of_cars):
    ids = []
    
    ids_and_prices = []
    for car in list_of_cars:
        if car[1] in ids:
            #print(car[1], car[5])
            ids_and_prices.append([car[1], car[5]])
            
            
    print(ids_and_prices[1][0], ids_and_prices[1][1])
    print()
    
    for iap in ids_and_prices:    
        print(iap)

#finds cars without prices and notes there id  
def find_car_prices(list_of_cars_without_prices):
    ids_and_prices = []
    
    for car in list_of_cars_without_prices:
        for iap in ids_and_prices:
            if car[1] == iap[0]:
                print(iap[0], iap[1], car[1])
                DBHandler.write_price(car[1], iap[1])
            
    return 0

#Used to fill in missing odometer
def fill_odometer(list_of_cars):
    cars_missing_odometer = []
    for car in list_of_cars:
        if car[6] == 'Unspecified':
            cars_missing_odometer.append(car)
    
    #Fill with average of cars from same year 
    index = 0      
    for car in cars_missing_odometer:
        index += 1
        print(index)
        
        average_odometers = []
        for car_2 in list_of_cars:
            #If two cars have same year
            if car[4] == car_2[4] and car_2[6].isdigit():
                average_odometers.append(int(car_2[6]))
            
        average_odometer_reading = np.mean(average_odometers)
        DBHandler.write_odometer(car[1], average_odometer_reading)
        
#Used to fill owner    
def fill_owners(list_of_cars):
    cars_missing_owner = []
    #Creates a dictionary of average owners for every year
    average_owner_per_year = defaultdict(list)
    for car in list_of_cars:
        if car[11] == '':
            cars_missing_owner.append(car)
        else:
            average_owner_per_year[car[4]].append(int(car[11]))
    
    print(len(cars_missing_owner))
    print(len(average_owner_per_year['2017']))
    print(int(round(np.mean(average_owner_per_year['2017.5']))))

    index = 0
    for car in cars_missing_owner:
        index += 1
        owner_num = int(round(np.mean(average_owner_per_year[car[4]])))
        DBHandler.write_owners(car[1], str(owner_num))
        print(index)
        
#Fill road tax by findind similar cars        
def fill_road_tax(list_of_cars):
    cars_missing_road_tax = []
    for car in list_of_cars:
        if car[14] == '':# and float(car[4]) < 2008:
            cars_missing_road_tax.append(car)
    
    index = 0   
    print(len(cars_missing_road_tax))     
    for car in cars_missing_road_tax:
        index += 1
        road_taxes = []
        for car_2 in list_of_cars:
            #Removed year and engine size for final few models float(car_2[4]) < 2008
            if car[3] == car_2[3] and car[7] == car_2[7]:
                road_taxes.append(car_2[14])
        
        car_road_tax = Counter(road_taxes)
        DBHandler.write_road_tax(car[1], str(car_road_tax.most_common(1)[0][0]))
        print(car_road_tax.most_common(1))
        print(str(car_road_tax.most_common(1)[0][0]))
        print(index)
        
def fill_fuel_economy(list_of_cars):
    cars_missing_fuel_economy = []
    for car in list_of_cars:
        if car[15] == '':# and float(car[4]) < 2008:
            cars_missing_fuel_economy.append(car)
    
    index = 0   
    print(len(cars_missing_fuel_economy))     
    for car in cars_missing_fuel_economy:
        index += 1
        fuel_economies = []
        for car_2 in list_of_cars:
            #Removed year and fuel_type as results were harder to fill 
            
            if car[2] == car_2[2] and car[7] == car_2[7] and not car_2[15] == '':
                fuel_economies.append(car_2[15])
        
        car_fuel_economy = Counter(fuel_economies)
        try:
            DBHandler.write_fuel_economy(car[1], str(car_fuel_economy.most_common(1)[0][0]))
            print(car_fuel_economy.most_common(1)[0][0])
            print(str(car_fuel_economy.most_common(1)[0][0]))
        except IndexError:
            pass
        
        print(index)
        
            
def get_fuel_economy_from_excess(list_of_cars):
    cars_missing_fuel_economy = []
    for car in list_of_cars:
        if car[15] == '':
            cars_missing_fuel_economy.append(car)
            car_excess = car[19]
            car_excess = car_excess.split(',')
            print(car_excess)
            for el in car_excess:
                if len(el) > 0:
                    if 'MPG' in el:
                        fuel_economy = el
                        print(el)
                        DBHandler.write_fuel_economy(car[1], fuel_economy)
                        
    print(len(cars_missing_fuel_economy))
        
if __name__ == '__main__':
    list_of_cars = list(read_training_cars())
    fill_fuel_economy(list_of_cars)
          

    
    
   
    
    
    
    
    
    