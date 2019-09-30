'''
@author: Glen Devlin
'''
#import DBHandler
#import data_cleaner
import random
from sqlite3 import collections
from sklearn.metrics.regression import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
#from numpy.random import random


from DBHandler import write_predicted_price
from DBHandler import read_training_cars
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
import numpy as np
import pandas as pd

#Read cars from database
def read_cars(training_choice):
    cars = []
    
    #Training Cars
    if training_choice == "training":
        cars = read_training_cars()
        
    list_of_cars = []
    for car in cars: 
        #Car features
        list_of_cars.append([car[0], car[1], car[2], car[3], float(car[4]), int(car[5]), float(car[6]), 
                        car[7], float(car[8]), car[9], car[10], int(car[11]), car[12], car[13], int(car[14]), int(car[15]), 
                        car[16], car[17], car[18], car[19], float(car[20])])
            
    return list_of_cars        
 
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
    list_of_road_taxes = []
    list_of_fuel_economies = []
    
    for car in cars:
        list_of_ids.append(car[1])
        list_of_makes.append(car[2])
        list_of_models.append(car[3])
        list_of_years.append(car[4])
        list_of_prices.append(car[5])
        list_of_odometers.append(car[6])
        list_of_fuel_types.append(car[7])
        list_of_engine_sizes.append(car[8])
        list_of_colours.append(car[9])
        list_of_bodies.append(car[10])
        list_of_owners.append(car[11])
        list_of_transmissions.append(car[12])
        list_of_road_taxes.append(car[14])
        list_of_fuel_economies.append(car[15])
        
        
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
    car_data['Road Tax'] = list_of_road_taxes
    car_data['Fuel Economy'] = list_of_fuel_economies
    
    car_data_frame = pd.DataFrame(data = car_data)
    return car_data_frame
    
    
#Turns labels into numbers    
def encode_categoricals(list_of_categories):
    le = preprocessing.LabelEncoder()
    le.fit(list_of_categories)
    return le.transform(list_of_categories)

#Normalise data frame to get correlations
def normalise_data_frame(car_data_frame):
    features_to_normalise = list(car_data_frame.columns.values)
    features_to_normalise.remove('ID')
    features_to_normalise.remove('Make')
    features_to_normalise.remove('Price')
    
    for feat in features_to_normalise:
        car_data_frame[feat] = (car_data_frame[feat] - car_data_frame[feat].min()) / (car_data_frame[feat].max() - car_data_frame[feat].min())

    return car_data_frame
 
#Create multiple linear regression model and return it           
def multiple_regression_model(car_data_frame):
    mult_lin_reg = LinearRegression()
    #car_data_frame = car_data_frame.reset_index()
    
    dependent_variables = list(car_data_frame.columns.values)
    dependent_variables.remove('ID')
    dependent_variables.remove('Make')
    dependent_variables.remove('Price')

    mult_lin_reg = mult_lin_reg.fit(car_data_frame[dependent_variables], car_data_frame['Price'])
    
    return mult_lin_reg
        
#Comb through list of cars getting only inteded make and model
def make_and_model(list_of_cars, make):
    selected_cars = []
    models = []
    #user_choice = input("Choose make & model - 1: Audi A4 \t 2: BMW 3 series \t 3: BMW 5 series \n"
                                    #"\t\t      4: Ford Focus \t 5: Nissan Qashqai \t 6: Opel Astra\n"
                                    #"\t\t      7: Skoda Octavia \t 8: Volkswagen Golf \t 9: Volkswagen Passat ")
    user_choice = make
    if user_choice == '1':
        models.extend(['a4'])
    elif user_choice == '2':
        models.extend(['3 series', '318', '325', '316', '320', 'm3', '335', '330'])
    elif user_choice == '3':
        models.extend(['5 series', '520', '525', '523', '530', 'm5', '535', '518'])
    elif user_choice == '4':
        models.extend(['focus'])
    elif user_choice == '5':
        models.extend(['qashqai', 'qashqai +2'])
    elif user_choice == '6':
        models.extend(['astra'])
    elif user_choice == '7':
        models.extend(['octavia'])
    elif user_choice == '8':
        models.extend(['golf'])
    elif user_choice == '9':
        models.extend(['passat'])
        
    for car in list_of_cars:
        if car[3].lower() in models:
            selected_cars.append(car)
    
    
    print(models)     
    return selected_cars


#Get mean squared error for a model    
def get_mean_square_error(list_of_cars, price_series):
    car_predicted_prices = []
    #car_predicted_prices = list_of_cars
    
    for car in list_of_cars:
        car_predicted_prices.append(car[20])
    
    mse = mean_squared_error(car_predicted_prices, price_series)
    return mse

#Get the root mean squared error   
def get_RMSE(mse):
    return np.sqrt(mse)

#Show Correlation with price
def show_correlation(car_data_frame):
    selected_featurres = list(car_data_frame.columns.values)
    selected_featurres.remove('ID')
    selected_featurres.remove('Make')
    
    corr_matrix = car_data_frame[selected_featurres].corr()
    print(corr_matrix['Price'].abs().sort_values())

#Get the variance of features  
def get_feature_varaince(car_data_frame):
    features = list(car_data_frame.columns.values)
    features.remove('ID')
    features.remove('Make')
    features.remove('Price')
    
    unit_train = (car_data_frame[features] - car_data_frame[features].min())/(car_data_frame[features].max() - car_data_frame[features].min())
    sorted_vars = unit_train.var().sort_values()
    return sorted_vars

#Generate a heatmap to show correlations
def generate_heat_map(car_data_frame):
    correlation_matrix = car_data_frame.corr()
    sorted_correlations = correlation_matrix['Price'].abs().sort_values()
    price_heatmap = car_data_frame[sorted_correlations.index].corr()
    sns.heatmap(price_heatmap)
    plt.show()

#Write predicted prices for cars in training table   
def write_training_predicted_prices():
    table_choice = "training"
    list_of_cars = read_cars(table_choice)#Read Training Cars
    
    #Start at first make, model    
    car_selection = 1
    
    #used to count cars where value < sale price
    total_car_count = 0
    while car_selection <= 1:
        print(car_selection)
        make = str(car_selection)
        selected_cars = make_and_model(list_of_cars, make)

        #Convert list to dataframe then print model        
        car_data_frame = convert_list_to_dataframe(selected_cars)
        mult_regression_model = multiple_regression_model(car_data_frame)
        car_data_frame = car_data_frame.reset_index()
        
        index = 0
        for car in car_data_frame.iterrows():
            dependent_variables = ['Model', 'Year', 'Odometer', 'Fuel Type', 'Engine Size', 
                                    'Colour', 'Body', 'Owners', 'Transmission', 'Road Tax', 'Fuel Economy']
            
            car_id = car_data_frame['ID'].loc[index]     
            car_price = car_data_frame['Price'].loc[index]
            current_car = car_data_frame[dependent_variables].loc[index]
            #print(//current car details)
            
            predicted_price = mult_regression_model.predict(current_car.values.reshape(1, -1))
            write_predicted_price(car_id, float(predicted_price))
            
            
            if car_price < predicted_price:
                total_car_count += 1
                
            index += 1
        
        car_selection += 1
    
    print(total_car_count)
            
#Get each of the model coefficients   
def model_coeffients_and_intercept():
    table_choice = "training"
    list_of_cars = read_cars(table_choice)#Read Training Cars
        
    car_selection = 1
    while car_selection < 9:
        make = str(car_selection)
        selected_cars = make_and_model(list_of_cars, make)
        
        car_data_frame = convert_list_to_dataframe(selected_cars)        
        mult_regression_model = multiple_regression_model(car_data_frame)
        
        for coeffiecient in mult_regression_model.coef_:
            print(coeffiecient)
            
        print(mult_regression_model.coef_)
        print()
        
        car_selection += 1
    
#Return the metrics for a given model   
def get_model_metrics():
    #Read in Training Data
    training_data = read_cars("training")
    
    #Select a model of cars to build predictive model
    list_certaine_make_model = make_and_model(training_data, '1')
    print(len(list_certaine_make_model[0]))
    print()
    
    print("Data Frame")
    training_data_frame = convert_list_to_dataframe(list_certaine_make_model)
    print(training_data_frame.head(5))
    print()
    
    print("Normalised Data Frame")
    normalised_data_frame = normalise_data_frame(training_data_frame)
    print(normalised_data_frame.head(5))
    print()
    
    mse = get_mean_square_error(list_certaine_make_model, normalised_data_frame['Price'])
    rmse = get_RMSE(mse)
    print("Mean Squared Error: ", mse)
    print("Root Mean Squared Error: ", rmse)
        
    print("\nShow correlation")
    show_correlation(normalised_data_frame)
    
    print("\nVariance")
    print(get_feature_varaince(normalised_data_frame))
        
    print("\nHeatmap")
    generate_heat_map(normalised_data_frame)
    
    print("Done")
       
if __name__ == '__main__':
    get_model_metrics()
    
    
    
    
    