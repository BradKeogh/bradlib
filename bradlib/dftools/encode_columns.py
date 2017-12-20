def encode_columns(df,column_list):
    """
    Function to create encoded columns in a dataframe

    Input:
    df - dataframe to act on
    column_list - list of column names

    Output:
    transformed dataframe with additional encoded columns

    """
    import pandas as pd
    import numpy as np
    
    for x in column_list:
        df1 = pd.get_dummies(df[x],prefix=x)
        df = pd.merge(df,df1,left_index=True,right_index=True)
        df.drop(x,axis=1,inplace=True)
    return(df)