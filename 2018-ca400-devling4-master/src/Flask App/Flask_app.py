
from flask import Flask
import MySQLdb
import pandas as pd
import numpy as np
import collections
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing

app = Flask(__name__)




#Speak to the database trieving display cars
@app.route('/simple_db_conn')
def db_conn():

    conn = MySQLdb.connect("GDevlin.mysql.pythonanywhere-services.com", "GDevlin", "cardealspotter", "GDevlin$Car_Deal_Spotter")
    c = conn.cursor()
    c.execute("SELECT * FROM display_cars")
    rows = c.fetchall()

    items = str(rows)
    items = items.replace(' ', '')
    return items

#Add car to training_cars table
@app.route('/add_training_car/<URL>/<ID>/<Make>/<Model>/<Year>/<Price>/<Odometer>/<Fuel_Type>/<Engine_Size>/<Colour>/<Body>/<Owners>/<Transmission>/<NCT>/<Road_Tax>/<Fuel_Economy>/<SIMI_Dealer>/<Last_Update>/<Date_Scraped>/<excess>/<Predicted_Price>/<price_diff>')
def add_car_training(URL, ID, Make, Model, Year, Price, Odometer, Fuel_Type, Engine_Size, Colour, Body, Owners, Transmission, NCT, Road_Tax, Fuel_Economy, SIMI_Dealer, Last_Update, Date_Scraped, excess, Predicted_Price, price_diff):

    car_url = URL.replace('FORWARDSLASH', '/')
    car_url = car_url.replace('QUESTIONMARK', '?')
    car_url = car_url.replace('PERCENTAGESIGN', '%')
    car_price_diff = int(price_diff)
    car = [car_url, ID, Make, Model, Year, Price, Odometer, Fuel_Type, Engine_Size, Colour, Body, Owners, Transmission, NCT, Road_Tax, Fuel_Economy,
                SIMI_Dealer, Last_Update, Date_Scraped, excess, Predicted_Price, car_price_diff]

    #return str(car)
    #return str(car)

    conn = MySQLdb.connect("GDevlin.mysql.pythonanywhere-services.com", "GDevlin", "cardealspotter", "GDevlin$Car_Deal_Spotter")
    c = conn.cursor()

    add_car = ("INSERT INTO training_cars "
                "(URL, ID, Make, Model, Year, Price, Odometer, Fuel_Type, Engine_Size, Colour, Body, Owners, Transmission, NCT_Due, Road_Tax, "
                "Fuel_Economy, SIMI_Dealer, Last_Update, Date_Scraped, excess, Predicted_Price, price_diff) "
                "Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

    c.execute(add_car, car)
    conn.commit()
    return "Entry Added!"

#Add car to training_cars table
@app.route('/add_display_car/<URL>/<ID>/<Make>/<Model>/<Year>/<Price>/<Odometer>/<Fuel_Type>/<Engine_Size>/<Colour>/<Body>/<Owners>/<Transmission>/<NCT>/<Road_Tax>/<Fuel_Economy>/<SIMI_Dealer>/<Last_Update>/<Date_Scraped>/<excess>/<Predicted_Price>/<price_diff>')
def add_car_dispay(URL, ID, Make, Model, Year, Price, Odometer, Fuel_Type, Engine_Size, Colour, Body, Owners, Transmission, NCT, Road_Tax, Fuel_Economy, SIMI_Dealer, Last_Update, Date_Scraped, excess, Predicted_Price, price_diff):

    car_url = URL.replace('FORWARDSLASH', '/')
    car_url = car_url.replace('QUESTIONMARK', '?')
    car_url = car_url.replace('PERCENTAGESIGN', '%')
    car_price_diff = int(price_diff)
    car = [car_url, ID, Make, Model, Year, Price, Odometer, Fuel_Type, Engine_Size, Colour, Body, Owners, Transmission, NCT, Road_Tax, Fuel_Economy,
                SIMI_Dealer, Last_Update, Date_Scraped, excess, Predicted_Price, car_price_diff]

    #return str(car)
    #return str(car)

    conn = MySQLdb.connect("GDevlin.mysql.pythonanywhere-services.com", "GDevlin", "cardealspotter", "GDevlin$Car_Deal_Spotter")
    c = conn.cursor()

    add_car = ("INSERT INTO display_cars "
                "(URL, ID, Make, Model, Year, Price, Odometer, Fuel_Type, Engine_Size, Colour, Body, Owners, Transmission, NCT_Due, Road_Tax, "
                "Fuel_Economy, SIMI_Dealer, Last_Update, Date_Scraped, excess, Predicted_Price, price_diff) "
                "Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

    c.execute(add_car, car)
    conn.commit()
    return "Entry Added!"


#Add car to test table
@app.route('/test_table/<name>/<age>')
def add_test_table(name, age):

    person = [name, age]
    conn = MySQLdb.connect("GDevlin.mysql.pythonanywhere-services.com", "GDevlin", "cardealspotter", "GDevlin$Car_Deal_Spotter")
    c = conn.cursor()

    #add_person = ("INSERT INTO (Name, Age) VALUES (%s, %s)")
    #c.execute = ("INSERT INTO test_table(Name, Age) VALUES (%s, %s)", (name, age))
    add_person = ("""INSERT INTO test_table (Name, Age) Values(%s, %s);""")
    c.execute(add_person, person)
    conn.commit()

    return "Entry Added!"


##---------Linear Regression model for valuing car----
#Take a users car to value it
@app.route('/accept_car/<make>/<model>/<year>/<odometer>/<fuel>/<enginesize>/<colour>/<body>/<owners>/<transmission>')
def take_users_car(make, model, year, odometer, fuel, enginesize, colour, body, owners, transmission):

    car_features = []

    #Place holder url, id and price
    car_url = "www.filler.com"
    car_id = "123456"
    car_price = '0'

    car_make = make
    car_model = model.replace('.', ' ')
    car_year = year
    if len(car_year) == 4:
        car_year = float(car_year)
    elif len(car_year) == 10:
        if car_year[8] == '1':
            car_year = float(car_year[0:4])
        else:
            car_year = float(car_year[0:4]) + 0.5

    car_odometer = float(odometer)
    car_fuel_type = fuel
    car_engine_size = float(enginesize)
    car_colour = colour
    car_body = body
    car_owners = int(owners)
    car_transmission = transmission

    car_features.extend((car_url, car_id, car_make, car_model, car_year, car_price, car_odometer, car_fuel_type, car_engine_size, car_colour, car_body, car_owners, car_transmission))

    #Starts prediction process
    #return car_make
    predicted_price = read_in_training_data(car_features)
    predicted_price = int(predicted_price[0])
    return str(predicted_price)

#Read training data to value car
def read_in_training_data(car_features):
    car_model = car_features[3]
    print(car_model)

    conn = MySQLdb.connect("GDevlin.mysql.pythonanywhere-services.com", "GDevlin", "cardealspotter", "GDevlin$Car_Deal_Spotter")
    c = conn.cursor()
    c.execute("SELECT * FROM training_cars")

    list_of_cars = []
    for row in c.fetchall():
        row = list(row)
        row = row[0:13]
        list_of_cars.append(row)

    for row in list_of_cars[:5]:
        print(row)

    list_of_cars = get_same_model_cars(list_of_cars, car_model)
    for row in list_of_cars[:5]:
        print(row)
    #Add users car here
    list_of_cars.append(car_features)


    #convert list to dataframe
    car_data_frame = convert_list_to_dataframe(list_of_cars)
    print(car_data_frame.head(3))
    print()
    print(car_data_frame.tail(1))
    print()

    for row in list_of_cars[:5]:
        print(row)

    dependent_variables = list(car_data_frame.columns.values)
    dependent_variables.remove('ID')
    dependent_variables.remove('Make')
    dependent_variables.remove('Price')

    #Retirieve users car from the end of the dataframe
    users_car = car_data_frame[dependent_variables].iloc[-1].values.reshape(1, -1)
    print(users_car)
    car_data_frame = car_data_frame.drop(car_data_frame.index[-1])

    car_prediction_model = multiple_regression_model(car_data_frame)
    predicted_price  = car_prediction_model.predict(users_car)
    return predicted_price


#Get cars that are similar model for regression
def get_same_model_cars(list_of_cars, car_model):
    selected_cars = []
    models = []

    user_choice = car_model.lower()
    if user_choice == 'a4':
        models.extend(['a4'])
    elif user_choice in ['3 series', '318', '325', '316', '320', 'm3', '335', '330']:
        models.extend(['3 series', '318', '325', '316', '320', 'm3', '335', '330'])
    elif user_choice in ['5 series', '520', '525', '523', '530', 'm5', '535', '518']:
        models.extend(['5 series', '520', '525', '523', '530', 'm5', '535', '518'])
    elif user_choice == 'focus':
        models.extend(['focus'])
    elif user_choice in ['qashqai', 'qashqai +2']:
        models.extend(['qashqai', 'qashqai +2'])
    elif user_choice == 'astra':
        models.extend(['astra'])
    elif user_choice == 'octavia':
        models.extend(['octavia'])
    elif user_choice == 'golf':
        models.extend(['golf'])
    elif user_choice == 'passat':
        models.extend(['passat'])

    for car in list_of_cars:
        if car[3].lower() in models:
            selected_cars.append(car)

    return selected_cars

#Convert list of cars to a dataframe
def convert_list_to_dataframe(cars):
    car_data = collections.OrderedDict()
    list_of_ids = []
    list_of_makes = []
    list_of_models = []
    list_of_years = []
    list_of_prices = []
    list_of_odometers = []
    list_of_fuel_types = []
    list_of_engine_sizes = []
    list_of_colours = []
    list_of_bodies = []
    list_of_owners = []
    list_of_transmissions = []

    #Get relevant features
    for car in cars:
        car = list(car)
        list_of_ids.append(car[1])
        list_of_makes.append(car[2])
        list_of_models.append(car[3])
        car[4] = float(car[4])
        list_of_years.append(car[4])
        car[5] = int(car[5])
        list_of_prices.append(car[5])
        car[6] = float(car[6])
        list_of_odometers.append(car[6])
        list_of_fuel_types.append(car[7])
        car[8] = float(car[8])
        list_of_engine_sizes.append(car[8])
        list_of_colours.append(car[9])
        list_of_bodies.append(car[10])
        car[11] = int(car[11])
        list_of_owners.append(car[11])
        list_of_transmissions.append(car[12])

    car_data['ID'] = list_of_ids
    car_data['Make'] = list_of_makes
    car_data['Model'] = encode_categoricals(list_of_models)
    car_data['Year'] = list_of_years
    car_data['Price'] = list_of_prices
    car_data['Odometer'] = list_of_odometers
    car_data['Fuel Type'] = encode_categoricals(list_of_fuel_types)
    car_data['Engine Size'] = list_of_engine_sizes
    car_data['Colour'] = encode_categoricals(list_of_colours)
    car_data['Body'] = encode_categoricals(list_of_bodies)
    car_data['Owners'] = list_of_owners
    car_data['Transmission'] = encode_categoricals(list_of_transmissions)

    car_data_frame = pd.DataFrame(data = car_data)
    return car_data_frame

#Turns labels into numbers
def encode_categoricals(list_of_categories):
    le = preprocessing.LabelEncoder()
    le.fit(list_of_categories)
    return le.transform(list_of_categories)

#Normalise the dataframe, unused
def normalise_data_frame(car_data_frame):
    features_to_normalise = list(car_data_frame.columns.values)
    features_to_normalise.remove('ID')
    features_to_normalise.remove('Make')
    features_to_normalise.remove('Price')

    for feat in features_to_normalise:
        car_data_frame[feat] = (car_data_frame[feat] - car_data_frame[feat].min()) / (car_data_frame[feat].max() - car_data_frame[feat].min())

    return car_data_frame

#Fit model
def multiple_regression_model(car_data_frame):
    mult_lin_reg = LinearRegression()

    dependent_variables = list(car_data_frame.columns.values)
    dependent_variables.remove('ID')
    dependent_variables.remove('Make')
    dependent_variables.remove('Price')

    mult_lin_reg = mult_lin_reg.fit(car_data_frame[dependent_variables], car_data_frame['Price'])
    return mult_lin_reg

##----------Cars used from browsing feature----------
##Display cars for browsing
@app.route('/search_cars/<make>/<model>/<minYear>/<maxYear>/<minPrice>/<maxPrice>/<county>/<fuel>')
def search_cars(make, model, minYear, maxYear, minPrice, maxPrice, county, fuel):
    search_criteria = convert_criteria_to_searchable(make, model, minYear, maxYear, minPrice, maxPrice, county, fuel)

    car_data = read_display_cars()
    #print(car_data)

    relevant_list_of_cars = get_relevant_cars(search_criteria, car_data)

    #for r in relevant_list_of_cars:
        #print(r)

    string_of_cars = convert_list_to_string(relevant_list_of_cars)
    print(string_of_cars)
    return string_of_cars

#Use to users search criteria to select cars
def convert_criteria_to_searchable(make, model, minYear, maxYear, minPrice, maxPrice, county, fuel):
    search_criteria = []
    search_make = str(make)
    model = model.replace('.', ' ')
    if model.lower() == "3 series":
        search_model = ['3 series', '318', '325', '316', '320', 'm3', '335', '330']
    elif model.lower() == "5 series":
        search_model = ['5 series', '520', '525', '523', '530', 'm5', '535', '518']
    elif model.lower == "Qashqai":
        search_model = ['qashqai', 'qashqai +2']
    else:
        search_model = [model.lower()]

    if minYear == "Min Year":
        search_min_year = int(1950)
    else:
        search_min_year = int(minYear)
    if maxYear == "Max Year":
        search_max_year = float(2018.5)
    else:
        search_max_year = float(maxYear) + 0.5
    search_min_price = 0
    if minPrice == "Min Price":
        search_min_price = 0
    else:
        search_min_price = int(minPrice)
    search_max_price = 0
    if maxPrice == "Max Price":
        search_max_price = 100000
    else:
        search_max_price = int(maxPrice)

    search_county = str(county)
    search_county = []
    if county == "County":
        search_county = ["Antrim", "Armagh", "Carlow", "Cavan", "Clare", "Cork", "Derry",
                            "Donegal", "Down", "Dublin", "Fermanagh", "Galway", "Kerry", "Kildare",
                            "Kilkenny", "Laois", "Leitrim", "Limerick", "Longford", "Louth", "Mayo",
                            "Meath", "Monaghan", "Offaly", "Roscommon", "Sligo", "Tipperary", "Tyrone",
                            "Waterford", "Westmeath", "Wexford", "Wicklow"]
    else:
        search_count.append(str(county))
    search_fuel_type = ["Diesel", "Petrol"]
    if fuel == "Diesel":
        search_fuel_type.remove("Petrol")
    elif fuel == "Petrol":
        search_fuel_type.remove("Diesel")

    search_criteria.extend([search_make, search_model, search_min_year, search_max_year, search_min_price, search_max_price, search_county, search_fuel_type])
    print(search_criteria)

    return search_criteria

#Go through list of cars only get cars that match search criteria
def get_relevant_cars(search_criteria, list_of_cars):
    relevant_cars = []
    for car in list_of_cars:
        if is_car_relavant(car, search_criteria):
            relevant_cars.append(car)

    return relevant_cars

#Finds if car matches search criteria
def is_car_relavant(car, search_criteria):
    make_and_model_satisfied = False
    year_satisfied = False
    price_satisfied = False
    fuel_type_satisfied = False
    county_satisfied = False
    car_good_deal = False

    #print(type(search_criteria[0]))
    if (car[2] == search_criteria[0]) and (car[3].lower() in search_criteria[1]):
        make_and_model_satisfied = True
    if search_criteria[2] <= int(float(car[4])) <= search_criteria[3]:
        year_satisfied = True
    if search_criteria[4] <= int(car[5]) <= search_criteria[5]:
        price_satisfied = True
    if car[7] in search_criteria[7]:
        fuel_type_satisfied = True
    if car[13].lower in search_criteria[6]:
        county_satisfied = True
    if int(car[21]) < 0:
        car_good_deal = True

    if make_and_model_satisfied and year_satisfied and price_satisfied and fuel_type_satisfied and car_good_deal:
        return True
    else:
        return False

#Reads in display cars for browisng
def read_display_cars():
    conn = MySQLdb.connect("GDevlin.mysql.pythonanywhere-services.com", "GDevlin", "cardealspotter", "GDevlin$Car_Deal_Spotter")
    c = conn.cursor()
    c.execute("SELECT * FROM training_cars")
    #c.execute("SELECT * FROM display_cars")

    list_of_cars = []
    for row in c.fetchall():
        row = list(row)
        list_of_cars.append(row)

    return list_of_cars

#Converts a list to string, so app can read
#cars seperted by {, features seperated by |
def convert_list_to_string(list_of_cars):
    whole_cars_string = ''
    for car in list_of_cars:
        for feat in car:
            feat = str(feat)
            whole_cars_string += feat + '|'
        whole_cars_string += "{"

    print(whole_cars_string)
    return whole_cars_string








