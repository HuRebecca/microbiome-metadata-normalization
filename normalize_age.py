'''

OVERALL GOALS:
--------------
-Make the normalization process more generalizable and time efficent for all features
(I chose to start with age because its one of the more complicated normalizations)

REQUIREMENTS:
-------------
-import numpy, pandas, re
-metadata is loaded in as df
-numerical values are numeric type and cleaned of strings (ex. no '25y', '125kg')

SOME CONCERNS:
---------------
-if no age unit and it cannot be inferred should it go to nan or assume years

-would it be possible to clean the values found in the antibiotic columns listing
a bunch of medications???

-right now I operate under the assumption that each row will have an age value and age unit value,
but I'm looking for a way to handle if a row only has 'age_in_years', but no separate age unit value;
currently I've created a function to try and decipher whether or not the age unit is given in the
column header but its not super efficient, for example if I determine 'age_in_years' tells us the
age unit is years, it will have to re-determine that for each row that gives the age value as 'age_in_years'
'''

age_cols = [] #add columns associated with age
age_unit_cols = [] #add all column associated with age unit

age_unit_dict = {
                 'year': ['year', 'years', 'yr', 'yrs', 'y'],
                 'month': ['month', 'months', 'mon', 'mons'],
                 'day': ['day', 'days', 'd'],
                 'hour': ['hour', 'hours', 'hr', 'hrs', 'h'],
                 'minute': ['minute', 'minutes', 'min', 'mins']
                }
age_unit_conversion_dict = {
                        'year': 1,
                        'month': 12,
                        'day': 365,
                        'hour': 21900,
                        'minute': 1314000
                        }



def fill_age_unit(column_name):
    '''
    helper function that tries to decipher an age unit if a host has an age value
    but no age unit associated with them, defaults to years

    Parameters
    -----------
    column_name: str
        the column name containing the host's age value

    Returns
    -----------
    str:
        a standardized age unit that has been inferred from the column name of the age value
    '''
    #I think using this would be more robust, but I don't think its necessary
    #column_name = column_name.lower().replace('_', ' ')
    #words = column_name.split()

    age_unit_list = re.findall('year|yr|day|month|hour|hr|min', column_name)

    #standardize the age unit
    if len(age_unit_list) > 0:
        for key, list in age_unit_dict.items():
            if age_unit_list[0] in list: #not really sure what to do in the case of more than 1 match
                return key
    return np.nan #If no age unit should I infer years or just have nan qiita_host_age?



def clean_age(age, age_unit):
    # Also not sure if this would be the best way to *assume* if no age unit, then put years
    '''
    helper function that normalizes an age value to years

    Parameters
    -----------
    age: float or int
        a numerical age value
    age_unit: str
        the age unit associated with the age value

    Returns
    -----------
    float:
        normalized age value based on age_unit, or nan if value does not fall within bounds
    '''
    #normalizes the age value based on what the age unit is determined to be
    conversion_val = age_unit_conversion_dict[age_unit]
    new_age = round(float(age) / conversion_val, 3) #ideally the age value columns would already by floats

    if new_age < 120 and new_age > 0:
            return new_age
    else:
        return np.nan



def clean_age_unit(age_unit):
    '''
    helper function to standard age unit using age_unit_dict dictionary

    Parameters
    -----------
    age_unit: str
        an age unit specifying the unit of measure for the age value for a host/row in the df

    Returns
    -----------
    str
        a standardized age unit
    '''
    age_unit = age_unit.lower()

    #if the age unit is not standard, find the standardized version
    new_unit = np.nan
    if not (age_unit in age_unit_dict.keys()):
        for key, vals in age_unit_dict.items():
            if age_unit in vals:
                new_unit = key
                break
    else:
        return age_unit

    return new_unit





def find_age_vals(row):
    '''
    helper function to find age values and age unit values associated with each host/row

    Parameters
    -----------
    row: pd.Series object
        a row of a DataFrame containing host metadata

    Returns
    -----------
    float
        a cleaned age value that has been normalized to years, or nan if no age value is found
    '''
    #This for loop finds the age value
    for age_col in age_cols:
        age = row[age_col]
        if not pd.isna(age):
            break

    #This for loop finds the age unit and cleans it
    for unit_col in age_unit_cols:
        age_unit = row[unit_col]
        if not pd.isna(age_unit):
            age_unit = clean_age_unit(age_unit)
            break

    if pd.isna(age):
        return np.nan
    #if age unit is nan, try to infer from age column header
    elif pd.isna(age_unit):
        age_unit = fill_age_unit(age_col)
    # if age unit is still nan, return nan (COULD CHANGE)
    if pd.isna(age_unit):
        return np.nan # If I don't find an age unit and can't infer age unit from age column header should it become years or nan?
    #if both age and age units are found, find the final normalized age value
    return clean_age(age, age_unit)





def mergenorm_age():
    '''
    creates a series with merged and normalized age values in 'years'

    Parameters
    -----------
    none

    I don't think its necessary to have params if age_cols and unit_cols are gloablly defined

    age_cols: list
        a list containing all column names (str) of columns containing numerical age data
    unit_cols: list
        a list containing all column names (str) of columns containing age unit data

    Returns
    -----------
    pd.Series
        a pd.Series with merged age data that has been normalized to units of year
    '''
    #create a smaller df to search through
    age_df = df[age_cols+ age_unit_cols]
    #make age columns numeric, ideally this wouldn't have to be done?
    age_df[age_cols] = age_df[age_cols].apply(lambda x: pd.to_numeric(x, errors = 'coerce'))
    #apply all helper function to entire df
    return age_df.apply(find_age_vals, axis = 1)
