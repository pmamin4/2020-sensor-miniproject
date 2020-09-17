#!/usr/bin/env python3
"""
This example assumes the JSON data is saved one line per timestamp (message from server).

It shows how to read and process a text file line-by-line in Python, converting JSON fragments
to per-sensor dictionaries indexed by time.
These dictionaries are immediately put into Pandas DataFrames for easier processing.

Feel free to save your data in a better format--I was just showing what one might do quickly.
"""
import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np
import math


def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:

    temperature = {}
    occupancy = {}
    co2 = {}

    
    with open('json.txt', "r") as f:
        for line in f:
            r = json.loads(line)
            room = list(r.keys())[0]
            time = datetime.fromisoformat(r[room]["time"])
            

            temperature[time] = {room: r[room]["temperature"][0]}
            occupancy[time] = {room: r[room]["occupancy"][0]}
            co2[time] = {room: r[room]["co2"][0]}

    data = {
        "temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index(),
        "occupancy": pandas.DataFrame.from_dict(occupancy, "index").sort_index(),
        "co2": pandas.DataFrame.from_dict(co2, "index").sort_index(),
    }

    return data


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="load and analyse IoT JSON data")
    p.add_argument("file", help="path to JSON data file")
    P = p.parse_args()

    
    file = "log.txt"

    data = load_data(file)
    
    counter_office = 0
    counter_class = 0
    counter_lab = 0
    number_of_data_office = len(data['temperature'].office)
    number_of_data_class = len(data['temperature'].class1)
    number_of_data_lab = len(data['temperature'].lab1)
    
    for x in range(len(data['temperature'])):
        if(not(math.isnan(data['temperature'].office[x]))):
            
            if(abs(data['temperature'].office[x]-data['temperature'].median().office)>= 2 * data['temperature'].std().office):
                counter_office +=1
    for x in range(len(data['temperature'])):
        if(not(math.isnan(data['temperature'].lab1[x]))):
            
            if(abs(data['temperature'].lab1[x]-data['temperature'].median().lab1)>= 2 * data['temperature'].std().lab1):
                counter_lab +=1
    for x in range(len(data['temperature'])):
        if(not(math.isnan(data['temperature'].class1[x]))):
            
            if(abs(data['temperature'].class1[x]-data['temperature'].median().class1)>= 2 * data['temperature'].std().class1):
                counter_class +=1
    
    for k in data:
        
        if k == 'temperature':
            print('Temperature Median is:')
            print(data[k].median())
            print('Temperature Variance is:')
            print(data[k].var())
            print('Temperature Standard Deviation is:')
            print(data[k].std())
            print('Temperature mean is:')
            print(data[k].mean())
            lower_bound_office = data[k]["office"].mean() - 2 * data[k]["office"].std()
            upper_bound_office = data[k]["office"].mean() + 2 * data[k]["office"].std()
            print("the lower bound in office is : "  , lower_bound_office)
            print("the upper bound in office is : "  , upper_bound_office)
            lower_bound_class = data[k]["class1"].mean() - 2 * data[k]["class1"].std()
            upper_bound_class = data[k]["class1"].mean() + 2 * data[k]["class1"].std()
            print("the lower bound in class1 is : "  , lower_bound_class)
            print("the upper bound in class1 is : "  , upper_bound_class)
            lower_bound_lab = data[k]["lab1"].mean() - 2 * data[k]["lab1"].std()
            upper_bound_lab = data[k]["lab1"].mean() + 2 * data[k]["lab1"].std()
            print("the lower bound in lab1 is : "  , lower_bound_lab)
            print("the upper bound in lab1 is : "  , upper_bound_lab)

            
                
            good = (data['temperature'].office < upper_bound_office) & (data['temperature'].office > lower_bound_office)
            temp_office = data['temperature'].office[good]
            print("office data", temp_office)
            print(temp_office.size)
            
            
            
            
            good2 = (data['temperature'].lab1 < upper_bound_lab) & (data['temperature'].lab1 > lower_bound_lab)
            temp_lab1 = data['temperature'].lab1[good2]
            print('lab data', temp_lab1)
            print(temp_lab1.size)
            
            
            
            
            good4 = (data['temperature'].class1 < upper_bound_class) & (data['temperature'].class1 > lower_bound_class)
            temp_class1 = data['temperature'].class1[good4]
            print('class data' , temp_class1)
            print(temp_class1.size)
            print('filtered mean temperature office :', temp_office.median())
            print('filtered variance temperature office :', temp_office.var())
            print('filtered mean temperature lab :', temp_lab1.median())
            print('filtered variance temperature lab :', temp_lab1.var())
            print('filtered mean temperature class :', temp_class1.median())
            print('filtered variance temperature class :', temp_class1.var())


            """  print("here is what : \n")
            print(data[k].std().office)
            print("here is what2 : \n")
            if(not(math.isnan(data[k].office[0]))):
                print(data[k].office[0])
            """

        if k == 'occupancy':
            print('Occupancy Median is:')
            print(data[k].median())
            print('Occupancy Variance is:')
            print(data[k].var())
            print('Occupancy Standard Deviation is:')
            print(data[k].std())
            print('Occupancy mean is:')
            print(data[k].mean())
        """
        time = data[k].index
        data[k].hist()
        plt.figure()
        plt.hist(np.diff(time.values).astype(np.int64) // 1000000000)
        plt.xlabel("Time (seconds)")
        """
        if k == 'temperature':
            data[k].plot.hist()
            plt.title('Temperature probability density function')
        elif k == 'occupancy':
            data[k].plot.hist()
            plt.title('Occupancy probability density function')
        else:
            data[k].plot.hist()
            plt.title('Co2 probability density function')
        

    time_diffrence = data['temperature'].index[1:] - data['temperature'].index[:-1]
    
    time = [t.total_seconds() for t in time_diffrence]
    
    time_series = pandas.Series(time)
    
    time_median = time_series.median()
    time_mean = time_series.mean()
    time_variation = time_series.var()
    time_standard_deviation = time_series.std()
    print("Time mean is : ", time_mean)
    print("Time median is : ", time_median)
    print("Time variation is : ", time_variation)
    print("Time standard deviation is : ", time_standard_deviation)
    plt.figure()
    time_series.plot.hist()
    plt.title("Time interval probability density function")
        
    percentage_class =  (number_of_data_class-counter_class)/(number_of_data_class) * 100  
    percentage_lab =  (number_of_data_lab-counter_lab)/(number_of_data_lab) * 100  
    percentage_office =  (number_of_data_office-counter_office)/(number_of_data_office) * 100  
    print("there are ", 100 - percentage_class, " % bad data in class1")
    print("there are ", 100 - percentage_lab, " % bad data in lab1")
    print("there are ", 100 - percentage_office, " % bad data in office")
    plt.show()

