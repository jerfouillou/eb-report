# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 09:58:55 2019
@author: jeremy.fouillou
"""

#IMPORT LIBRARIES
import requests
import pandas as pd
summarytable = pd.DataFrame(columns = ['Category','Type','U-Value (W/m2K)'])


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
    df.loc[:,cols] = df[cols].apply(pd.to_numeric, errors='coerce')
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


"""This function assigns the 'type' of each entry in the dataframe. Maybe the boundaries can be discusses (can a roof be <180 
degrees??)"""
def assignCategory(row):
    if row == 0:
        return "Floor"
    elif row > 0 and row < 180:
        return "Wall"
    elif row == 180:
        return "Roof"

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
    values.loc[:,"category"]=values["Tilt [deg]"].apply(assignCategory)
    wall = values[(values.category=="Wall")]    
    wall_u_types = wall["U-Factor with Film [W/m2-K]"].unique()
    wall.loc[:,"type"] = wall["U-Factor with Film [W/m2-K]"].apply(assignType, types = wall_u_types) 
    roof = values[(values.category=="Roof")]        
    roof_u_types = roof["U-Factor with Film [W/m2-K]"].unique() 
    roof.loc[:,"type"] = roof["U-Factor with Film [W/m2-K]"].apply(assignType, types = roof_u_types)
    floor = values[(values.category=="Floor")]        
    floor_u_types = floor["U-Factor with Film [W/m2-K]"].unique() 
    floor.loc[:,"type"] = floor["U-Factor with Film [W/m2-K]"].apply(assignType, types = floor_u_types)
    formattedvalues=pd.concat([wall,roof,floor], axis=0)
    return formattedvalues


"""This function takes the formatted values (with types and categoreies), and appends unique entries
to the (global) summarytable. The summary table can then be used directly to fill the report sheet"""
def fillSummaryTable(row):
    uvalue = row['U-Factor with Film [W/m2-K]']
    types = row["type"]
    category=row["category"]
    global summarytable
    i = 0
    for row_index,rows in summarytable.iterrows():
        if category == summarytable.loc[row_index, "Category"] and types == summarytable.loc[row_index,"Type"]:
            i=i+1
    if i == 0 :
        newrow = pd.DataFrame.from_dict([{"Category" : category, "Type" : types, 'U-Value (W/m2K)' : uvalue}])
        summarytable = summarytable.append(newrow,  ignore_index = True, sort = False)
    pass

def main(id):
    values = getByKeyword(id,"opaque")
    formattedvalues = assignCatAndType(values)
    formattedvalues.apply(fillSummaryTable, axis = 1)
    return(summarytable)
    print("DONE")

main(2159)

