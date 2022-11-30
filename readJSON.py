# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 21:55:09 2022

@author: SAMANNOY
"""
import json
import pandas as pd

def readJSON(fileName):
    df = pd.read_json(fileName) # Read JSON file
    return df                   # Return the dataframe