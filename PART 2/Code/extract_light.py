# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 13:01:08 2020

@author: jeremy.fouillou
"""

#IMPORT LIBRARIES
import requests
import pandas as pd
import numpy
summarytable = pd.DataFrame(columns = ['Category','Type','U-Value (W/m2K)'])
df0 = pd.DataFrame()


servername = 'http://hkg1902w0057/project/api/'
id = 4197


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

def getByKeyword(id,keyword, servername):
    url=servername+str(id)+'/'+keyword
    r = requests.get(url)
    #print (r.json()[0])
    value=r.json()[0]["json"]
    raw_dict=replace_value(value,'\xa0',"")
    cols=list(raw_dict.keys())
    df=dict2df(raw_dict,cols)
    #print(df)
    return raw_dict


#def main_light(id, servername):
values = getByKeyword(id,"light", servername)

#return(summarytable)