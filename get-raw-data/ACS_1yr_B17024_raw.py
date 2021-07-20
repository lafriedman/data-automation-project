# get table B17024 in 1-year ACS, first year available (2006) to latest year available
# table B17024 is 'AGE BY RATIO OF INCOME TO POVERTY LEVEL IN THE PAST 12 MONTHS'

# Import packages
import requests
import json
import pandas as pd
from datetime import date

#create variable for previous year
todays_date = date.today()
previous_year = todays_date.year - 1

#check if previous year's data has been released. Use this info to set the latest year data is available to either 1. previous year or 2. the year before previous year 
try: 
  response = requests.get("https://api.census.gov/data/" + str(previous_year) + "/acs/acs1?get=NAME&for=state:*")
  x = response.json() #this will cause an error if the previous year is not available and so will run the except statement
  latest_data_year = previous_year
except :
  latest_data_year = previous_year - 1

# create var for API key
apikey = 'insert_here'

#create var for Google Drive id
googleDriveID = 'insert_here'

# create dictionary for geography levels
geographyLevels = {
  'US': '&for=us:*',
  'TX': '&for=state:48',
  'TravisCounty': '&for=county:453&in=state:48',
  'Austin': '&for=place:05000&in=state:48',
  'AustinRRMSA': '&for=metropolitan%20statistical%20area/micropolitan%20statistical%20area:12420'
}

# create vars for variables. Need to do two here because only 50 variables allowed in a call.
vars = 'B17024_001E,B17024_001M,B17024_002E,B17024_002M,B17024_003E,B17024_003M,B17024_004E,B17024_004M,B17024_005E,B17024_005M,B17024_006E,B17024_006M,B17024_007E,B17024_007M,B17024_008E,B17024_008M,B17024_009E,B17024_009M,B17024_010E,B17024_010M,B17024_015E,B17024_015M,B17024_016E,B17024_016M,B17024_017E,B17024_017M,B17024_018E,B17024_018M,B17024_019E,B17024_019M,B17024_020E,B17024_020M,B17024_021E,B17024_021M,B17024_022E,B17024_022M,B17024_023E,B17024_023M,B17024_028E,B17024_028M,B17024_029E,B17024_029M,B17024_030E,B17024_030M,B17024_031E,B17024_031M,B17024_032E,B17024_032M,B17024_033E,B17024_033M'
vars2 = 'B17024_034E,B17024_034M,B17024_035E,B17024_035M,B17024_036E,B17024_036M'

#initialize list to store dictionaries of API results
result_list = []

# create requests for each geography level and year since ACS 1-year began, store each request as a dictionary, and append the dictionary to `result_list`
for geokey, geovalue in geographyLevels.items() :
  for year in range(2006, latest_data_year + 1, 1) : #2005 is not available
    url = 'https://api.census.gov/data/' + str(year) + '/acs/acs1?get=' + vars + geovalue + '&key=' + apikey
    #get result
    r = requests.get(url)
    x = r.json()
    #store as a dictionary
    result_dict = dict(zip(x[0], x[1]))
    #add year key and value
    result_dict['year'] = year
    #add geography keys and values in usable format and get rid of current ones (there is probably a more concise way to do this)
    #note 'state' needs to come after 'county' and 'place' in the elifs because those also include a 'state' key
    if 'us' in result_dict : 
      result_dict['geography'] = 'US' #add new geography key/value
      del(result_dict['us']) #delete current geography key/value
    elif 'county' in result_dict : 
      result_dict['geography'] = 'Travis County'
      del(result_dict['county'])
      del(result_dict['state'])
    elif 'place' in result_dict : 
      result_dict['geography'] = 'Austin'
      del(result_dict['place'])
      del(result_dict['state'])
    elif 'state' in result_dict : 
      result_dict['geography'] = 'Texas'
      del(result_dict['state'])
    elif 'metropolitan statistical area/micropolitan statistical area' in result_dict : 
      result_dict['geography'] = 'Austin-Round Rock MSA'
      del(result_dict['metropolitan statistical area/micropolitan statistical area'])
    #append dictionary to a list
    result_list.append(result_dict)

#repeat for other 6 vars in a second list of dictionaries
result_list2 = []

for geokey, geovalue in geographyLevels.items() :
  for year in range(2006, latest_data_year + 1, 1) : 
    url = 'https://api.census.gov/data/' + str(year) + '/acs/acs1?get=' + vars2 + geovalue + '&key=' + apikey
    #get result
    r2 = requests.get(url)
    x2 = r2.json()
    #store as a dictionary
    result_dict2 = dict(zip(x2[0], x2[1]))
    #add year key and value
    result_dict2['year'] = year
    #add geography keys and values in usable format and get rid of current ones (there is probably a more concise way to do this)
    #note 'state' needs to come after 'county' and 'place' in the elifs because those also include a 'state' key
    if 'us' in result_dict2 : 
      result_dict2['geography'] = 'US' #add new geography key/value
      del(result_dict2['us']) #delete current geography key/value
    elif 'county' in result_dict2 : 
      result_dict2['geography'] = 'Travis County'
      del(result_dict2['county'])
      del(result_dict2['state'])
    elif 'place' in result_dict2 : 
      result_dict2['geography'] = 'Austin'
      del(result_dict2['place'])
      del(result_dict2['state'])
    elif 'state' in result_dict2 : 
      result_dict2['geography'] = 'Texas'
      del(result_dict2['state'])
    elif 'metropolitan statistical area/micropolitan statistical area' in result_dict2 : 
      result_dict2['geography'] = 'Austin-Round Rock MSA'
      del(result_dict2['metropolitan statistical area/micropolitan statistical area'])
    #append dictionary to a list
    result_list2.append(result_dict2)

#turn lists of dictionaries into dataframes
df1 = pd.DataFrame(result_list)
df2 = pd.DataFrame(result_list2)

#join dataframes on year and geography
df3 = pd.merge(df1, df2, on=['year','geography'])

#rewrite column names to be more descriptive 
df3 = df3.rename(columns={"B17024_001E": "total", "B17024_001M": "MOE_total", "B17024_002E": "total_under_6yrs", "B17024_002M": "MOE_total_under_6yrs", "B17024_003E": "under_6yrs_under_.50", "B17024_003M": "MOE_under_6yrs_under_.50", "B17024_004E": "under_6yrs_.50_to_.74", "B17024_004M": "MOE_under_6yrs_.50_to_.74", "B17024_005E": "under_6yrs_.75_to_.99", "B17024_005M": "MOE_under_6yrs_.75_to_.99", "B17024_006E": "under_6yrs_1_to_1.24", "B17024_006M": "MOE_under_6yrs_1_to_1.24", "B17024_007E": "under_6yrs_1.25_to_1.49", "B17024_007M": "MOE_under_6yrs_1.25_to_1.49", "B17024_008E": "under_6yrs_1.50_to_1.74", "B17024_008M": "MOE_under_6yrs_1.50_to_1.74", "B17024_009E": "under_6yrs_1.75_to_1.84", "B17024_009M": "MOE_under_6yrs_1.75_to_1.84", "B17024_010E": "under_6yrs_1.85_to_1.99", "B17024_010M": "MOE_under_6yrs_1.85_to_1.99","B17024_015E": "total_6_to_11yrs", "B17024_015M": "MOE_total_6_to_11yrs", "B17024_016E": "6_to_11yrs_under_.50", "B17024_016M": "MOE_6_to_11yrs_under_.50", "B17024_017E": "6_to_11yrs_.50_to_.74", "B17024_017M": "MOE_6_to_11yrs_.50_to_.74", "B17024_018E": "6_to_11yrs_.75_to_.99", "B17024_018M": "MOE_6_to_11yrs_.75_to_.99", "B17024_019E": "6_to_11yrs_1_to_1.24", "B17024_019M": "MOE_6_to_11yrs_1_to_1.24", "B17024_020E": "6_to_11yrs_1.25_to_1.49", "B17024_020M": "MOE_6_to_11yrs_1.25_to_1.49", "B17024_021E": "6_to_11yrs_1.50_to_1.74", "B17024_021M": "MOE_6_to_11yrs_1.50_to_1.74", "B17024_022E": "6_to_11yrs_1.75_to_1.84", "B17024_022M": "MOE_6_to_11yrs_1.75_to_1.84", "B17024_023E": "6_to_11yrs_1.85_to_1.99", "B17024_023M": "MOE_6_to_11yrs_1.85_to_1.99","B17024_028E": "total_12_to_17yrs", "B17024_028M": "MOE_total_12_to_17yrs", "B17024_029E": "12_to_17yrs_under_.50", "B17024_029M": "MOE_12_to_17yrs_under_.50", "B17024_030E": "12_to_17yrs_.50_to_.74", "B17024_030M": "MOE_12_to_17yrs_.50_to_.74", "B17024_031E": "12_to_17yrs_.75_to_.99", "B17024_031M": "MOE_12_to_17yrs_.75_to_.99", "B17024_032E": "12_to_17yrs_1_to_1.24", "B17024_032M": "MOE_12_to_17yrs_1_to_1.24", "B17024_033E": "12_to_17yrs_1.25_to_1.49", "B17024_033M": "MOE_12_to_17yrs_1.25_to_1.49", "B17024_034E": "12_to_17yrs_1.50_to_1.74", "B17024_034M": "MOE_12_to_17yrs_1.50_to_1.74", "B17024_035E": "12_to_17yrs_1.75_to_1.84", "B17024_035M": "MOE_12_to_17yrs_1.75_to_1.84", "B17024_036E": "12_to_17yrs_1.85_to_1.99", "B17024_036M": "MOE_12_to_17yrs_1.85_to_1.99"})

#move the year and geography columns to the front (select slices of the list of columns add back together to reorder)
cols = df3.columns.to_list()
cols = cols[50:52] + cols[:50] + cols[52:]
df3 = df3[cols]

#convert df to csv
df3.to_csv('B17024_Poverty_Youth_RawData_' + str(latest_data_year) + '.csv', sep='\t', index=False)

#export to Google Drive
#make sure file id corresponds to correct folder
file = drive.CreateFile({'parents':[{u'id': googleDriveID}]}) 
file.SetContentFile('B17024_Poverty_Youth_RawData_' + str(latest_data_year) + '.csv')
file.Upload()