# get data frame for table B17002 in 1-year ACS, first year available (2005) to latest year available

# table B17002 is 'Ratio of income to poverty level in the past 12 months'
# Notes on table usage: use the ratio to determine number of people with income at, below, or above poverty level. Ratio of 1 and lower means income is at or below poverty level.

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

# create var for variables
vars = 'B17002_001E,B17002_001M,B17002_002E,B17002_002M,B17002_003E,B17002_003M,B17002_004E,B17002_004M,B17002_005E,B17002_005M,B17002_006E,B17002_006M,B17002_007E,B17002_007M,B17002_008E,B17002_008M,B17002_009E,B17002_009M,B17002_010E,B17002_010M,B17002_011E,B17002_011M,B17002_012E,B17002_012M,B17002_013E,B17002_013M'

#initialize list to store dictionaries of API results
result_list = []

# create requests for each geography level and year since ACS 1-year began, store each request as a dictionary, and append the dictionary to `result_list`
for geokey, geovalue in geographyLevels.items() :
  for year in range(2005, latest_data_year + 1, 1) : #need to add one to latest data year since range doesn't include the last item
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

#turn list of dictionaries into a dataframe
df = pd.DataFrame(result_list)

#rewrite column names to be more descriptive 
newdf = df.rename(columns={'B17002_001E': "total_pop", "B17002_001M": "MOE_total_pop", "B17002_002E": "under_.50", "B17002_002M": "MOE_under_.50", "B17002_003E": ".50_to_.74", "B17002_003M": "MOE_.50_to_.74", "B17002_004E": ".75_to_.99", "B17002_004M": "MOE_.75_to_.99", "B17002_005E": "1_to_1.24", "B17002_005M": "MOE_1_to_1.24", "B17002_006E": "1.25_to_1.49", "B17002_006M": "MOE_1.25_to_1.49", "B17002_007E": "1.50_to_1.74", "B17002_007M": "MOE_1.50_to_1.74", "B17002_008E": "1.75_to_1.84", "B17002_008M": "MOE_1.75_to_1.84", "B17002_009E": "1.85_to_1.99", "B17002_009M": "MOE_1.85_to_1.99", "B17002_010E": "2_to_2.99", "B17002_010M": "MOE_2_to_2.99", "B17002_011E": "3_to_3.99", "B17002_011M": "MOE_3_to_3.99", "B17002_012E": "4_to_4.99", "B17002_012M": "MOE_4_to_4.99", "B17002_013E": "5_and_over", "B17002_013M": "MOE_5_and_over"})

#convert df to csv
newdf.to_csv('B17002_Poverty_General_RawData_' + str(latest_data_year) + '.csv', sep='\t', index=False)

#export to Google Drive
#make sure file id corresponds to correct folder
file = drive.CreateFile({'parents':[{u'id': googleDriveID}]})
file.SetContentFile('B17002_Poverty_General_RawData_' + str(latest_data_year) + '.csv')
file.Upload()