import pandas as pd
import numpy as np
from dateparser import parse
import zipcodes

class attribute:
    def __init__(self , df , column_name):
        attribute_name = column_name
        is_numeric = np.issubdtype(df[column_name].dtype, np.number)
        is_categorical = (df[column_name].nunique() / df.shape[0]) < 0.005

def check_is_numeric(df,column_name):
    return np.issubdtype(df[df[column_name].notnull()][column_name].dtype, np.number)


def check_is_discrete(df,column_name):
    if df[df[column_name].notnull()][column_name].nunique() == 0:
        return None
    return (df[df[column_name].notnull()][column_name].nunique() / df.shape[0]) < 0.05


def check_is_date(df,column_name):
    nulls = 0
    for val in df[column_name]:
        if val is not None and not is_nan(val) and val != 'CA':   ## Parse Gives date value on CA.
            try:
                res = parse(val)
                if res is None:
                    return False
            except:
                return False
        else:
            nulls += 1
    if nulls != df.shape[0]:
        return True
    return False


def is_nan(x):
    return (x is np.nan or x != x)

def check_is_zip(df,column_name):
    nulls = 0
    for val in df[column_name]:
        if val is not None and not is_nan(val):
            try:
                if type(val) is not str:
                    val = str(int(val))
                res = zipcodes.is_real(val)
                if not res:
                    return False
            except:
                return False
        else:
            nulls += 1
    if nulls != df.shape[0]:
        return True
    return False


# for column_name in df.columns:
#     if check_is_date(df,column_name):
#         print("________")
#         print(column_name)
#         print("________")
#
# for column_name in df.columns:
#     print(column_name)
#     print(check_is_numeric(df,column_name))
#     print(check_is_discrete(df,column_name))
#     print(check_is_date(df,column_name))
#     print(check_is_zip(df,column_name))
#     print("________")

