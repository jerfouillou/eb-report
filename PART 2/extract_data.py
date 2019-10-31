# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 09:58:55 2019
@author: jeremy.fouillou
"""

#IMPORT LIBRARIES
import requests
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

id = 2159

#API CALL FUNCTION
def replace_value(dict, value_to_find, value_to_replace):
    # This function is to replace specified value('\xa0') in dictionary
    for k, v in dict.items():
        for k1, v1 in v.items():
            if v1 == value_to_find:
                v[k1] = value_to_replace
            dict[k] = v
        return dict

def dict2df(dict, cols):
    raw_df = pd.DataFrame.from_dict(dict)
    df = raw_df.drop(raw_df.index[0])  # first row is duplicated with columns
    df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
    return df

def getByKeyword(id,keyword):
    url='http://hkgaet105/project/api/'+str(id)+'/'+keyword
    r = requests.get(url)
    #print (r.json()[0])
    value=r.json()[0]["json"]
    raw_dict=replace_value(value,'\xa0',"")
    cols=list(raw_dict.keys())
    df=dict2df(raw_dict,cols)
    return df

#SECTION 5: Input Parmeters Summary Table: Building Envelope
#This function assigns the 'type' of each entry in the dataframe. Maybe the boundaries can be discusses (can a roof be <180 degrees??)
def assignCategory(row):
    if row == 0:
        return "floor"
    elif row > 0 and row < 180:
        return "wall"
    elif row == 180:
        return "roof"

def assignType(row, types):
    i = 1
    for x in types:
        if row == x:
            return i
        else:
            i=i+1
            
"""This function first separates the input dataframe into its separate categories (roof/wall/type) before
finding the number of types, and assigning these accordingly. Once all types have been added to the 3 dataframes,
the function concatenates the dataframes to form the "formatted vales" dataframe"""
def assignCatAndType(values):
    values["category"]=values["Tilt [deg]"].apply(assignCategory)
    wall = values[(values.category=="wall")]    
    wall_u_types = wall["U-Factor with Film [W/m2-K]"].unique() #Gets list of unique U-values
    wall.loc[:,"type"] = wall["U-Factor with Film [W/m2-K]"].apply(assignType, types = wall_u_types) #Assigns a type to each row
    roof = values[(values.category=="roof")]        
    roof_u_types = roof["U-Factor with Film [W/m2-K]"].unique() #Gets list of unique U-values
    roof.loc[:,"type"] = roof["U-Factor with Film [W/m2-K]"].apply(assignType, types = roof_u_types) #Assigns a type to each row
    floor = values[(values.category=="floor")]        
    floor_u_types = floor["U-Factor with Film [W/m2-K]"].unique() #Gets list of unique U-values
    floor.loc[:,"type"] = floor["U-Factor with Film [W/m2-K]"].apply(assignType, types = floor_u_types) #Assigns a type to each row
    formattedvalues=pd.concat([wall,roof,floor], axis=0)
    return formattedvalues


"""This function takesthe formatted values (with types and categoreies), and creates a dataframe containing a 
unique entry for each value (the summary table). The summary table can then be used directly to fill the report sheet"""
def fillSummaryTable(row, formattedvalues, summarytable):
   
    """PROBLEM IS HERE"""
    uvalue = formattedvalues[row,'U-Factor no Film [W/m2-K]']
    types = formattedvalues[row,'type']
    category=formattedvalues[row,'category']
    if category in summarytable['category'] and types in summarytable['Type']:
        pass
    else :
        print("got this far")
        summarytable.append(category, types, uvalue)
        pass



#MAIN
values = getByKeyword(id,"opaque")
formattedvalues = assignCatAndType(values)
summarytable = pd.DataFrame(columns = ['Category','Type','U-Value (W/m2K)'])
formattedvalues.apply(fillSummaryTable, axis = 0, args = (formattedvalues, summarytable))# = formattedvalues, summarytable = summarytable)
#formattedvalues.apply(fillSummaryTable, uvalue = formattedvalues['U-Factor no Film [W/m2-K]'], types = formattedvalues['type'], category=formattedvalues['category'], summarytable = summarytable)
print("DONE")


