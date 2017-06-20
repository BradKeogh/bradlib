def pd_tidy_column_heads(dataframe):
    """
    Function makes all column names lowercase and replaces any whitespace with _'s
    Returns dataframe for assignment to variable name
    """
    rename_cols = dict() # make dictionary of old column names and new ones
    for i in dataframe.columns:
        j = i.lower()
        j = j.strip()
        j = j.replace(' ','_')
        j = j.replace('.','_')
        j = j.replace('?','_')
        j = j.replace('&','_')
        j = j.replace('%','perc')
        j = j.replace('(','')
        j = j.replace(')','')
        j = j.replace(':','')
        j = j.replace(';','')
        rename_cols[i] = j

    dataframe = dataframe.rename(columns=rename_cols)
    return dataframe
