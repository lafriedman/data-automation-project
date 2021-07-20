# get totals for income below poverty level by age from tables B17020B, B17020B, B17020B, B17020B in 5-year ACS.
# first year available (2009) to latest year available
# table B17020B is 'Poverty status in the past 12 months by age (Black or African American alone)'
# table B17020D is 'Poverty status in the past 12 months by age (Asian alone)'
# table B17020H is 'Poverty status in the past 12 months by age (White alone, not Hispanic or Latino)'
# table B17020I is 'Poverty status in the past 12 months by age (Hispanic or Latino)'

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
  response = requests.get("https://api.census.gov/data/" + str(previous_year) + "/acs/acs5?get=NAME&for=state:*")
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

# create vars for variables. Doing four groups because will add a column for race/ethnicity/hispanic or latino origin
bvars = 'B17020B_001E,B17020B_001M,B17020B_002E,B17020B_002M,B17020B_003E,B17020B_003M,B17020B_004E,B17020B_004M,B17020B_005E,B17020B_005M,B17020B_006E,B17020B_006M,B17020B_007E,B17020B_007M,B17020B_008E,B17020B_008M,B17020B_009E,B17020B_009M,B17020B_010E,B17020B_010M,B17020B_011E,B17020B_011M,B17020B_012E,B17020B_012M,B17020B_013E,B17020B_013M,B17020B_014E,B17020B_014M,B17020B_015E,B17020B_015M,B17020B_016E,B17020B_016M,B17020B_017E,B17020B_017M' 
dvars = 'B17020D_001E,B17020D_001M,B17020D_002E,B17020D_002M,B17020D_003E,B17020D_003M,B17020D_004E,B17020D_004M,B17020D_005E,B17020D_005M,B17020D_006E,B17020D_006M,B17020D_007E,B17020D_007M,B17020D_008E,B17020D_008M,B17020D_009E,B17020D_009M,B17020D_010E,B17020D_010M,B17020D_011E,B17020D_011M,B17020D_012E,B17020D_012M,B17020D_013E,B17020D_013M,B17020D_014E,B17020D_014M,B17020D_015E,B17020D_015M,B17020D_016E,B17020D_016M,B17020D_017E,B17020D_017M'
hvars = 'B17020H_001E,B17020H_001M,B17020H_002E,B17020H_002M,B17020H_003E,B17020H_003M,B17020H_004E,B17020H_004M,B17020H_005E,B17020H_005M,B17020H_006E,B17020H_006M,B17020H_007E,B17020H_007M,B17020H_008E,B17020H_008M,B17020H_009E,B17020H_009M,B17020H_010E,B17020H_010M,B17020H_011E,B17020H_011M,B17020H_012E,B17020H_012M,B17020H_013E,B17020H_013M,B17020H_014E,B17020H_014M,B17020H_015E,B17020H_015M,B17020H_016E,B17020H_016M,B17020H_017E,B17020H_017M'
ivars = 'B17020I_001E,B17020I_001M,B17020I_002E,B17020I_002M,B17020I_003E,B17020I_003M,B17020I_004E,B17020I_004M,B17020I_005E,B17020I_005M,B17020I_006E,B17020I_006M,B17020I_007E,B17020I_007M,B17020I_008E,B17020I_008M,B17020I_009E,B17020I_009M,B17020I_010E,B17020I_010M,B17020I_011E,B17020I_011M,B17020I_012E,B17020I_012M,B17020I_013E,B17020I_013M,B17020I_014E,B17020I_014M,B17020I_015E,B17020I_015M,B17020I_016E,B17020I_016M,B17020I_017E,B17020I_017M'

#do separate loop for each table, because need to add a column specific to the table

#initialize lists to store dictionaries of API results
result_list_b = []
result_list_d = []
result_list_h = []
result_list_i = []

# create requests for each geography level and year, store each request as a dictionary, and append the dictionary to `result_list`
for geokey, geovalue in geographyLevels.items() :
  for year in range(2009, latest_data_year + 1, 1) : 
    urlb = 'https://api.census.gov/data/' + str(year) + '/acs/acs5?get=' + bvars + geovalue + '&key=' + apikey
    #get result
    rb = requests.get(urlb)
    xb = rb.json()
    #store as a dictionary
    result_dictb = dict(zip(xb[0], xb[1]))
    #add year key and value
    result_dictb['year'] = year
    #add race/ethnicity key and value
    result_dictb['race/ethnicity'] = 'Black'
    #add geography keys and values in usable format and get rid of current ones
    #note 'state' needs to come after 'county' and 'place' in the elifs because those also include a 'state' key
    if 'us' in result_dictb : 
      result_dictb['geography'] = 'US' #add new geography key/value
      del(result_dictb['us']) #delete current geography key/value
    elif 'county' in result_dictb : 
      result_dictb['geography'] = 'Travis County'
      del(result_dictb['county'])
      del(result_dictb['state'])
    elif 'place' in result_dictb : 
      result_dictb['geography'] = 'Austin'
      del(result_dictb['place'])
      del(result_dictb['state'])
    elif 'state' in result_dictb : 
      result_dictb['geography'] = 'Texas'
      del(result_dictb['state'])
    elif 'metropolitan statistical area/micropolitan statistical area' in result_dictb : 
      result_dictb['geography'] = 'Austin-Round Rock MSA'
      del(result_dictb['metropolitan statistical area/micropolitan statistical area'])
    #append dictionary to a list
    result_list_b.append(result_dictb)


for geokey, geovalue in geographyLevels.items() :
  for year in range(2009, latest_data_year + 1, 1) : 
    urld = 'https://api.census.gov/data/' + str(year) + '/acs/acs5?get=' + dvars + geovalue + '&key=' + apikey
    #get result
    rd = requests.get(urld)
    xd = rd.json()
    #store as a dictionary
    result_dictd = dict(zip(xd[0], xd[1]))
    #add year key and value
    result_dictd['year'] = year
    #add race/ethnicity key and value
    result_dictd['race/ethnicity'] = 'Asian'
    #add geography keys and values in usable format and get rid of current ones
    #note 'state' needs to come after 'county' and 'place' in the elifs because those also include a 'state' key
    if 'us' in result_dictd : 
      result_dictd['geography'] = 'US' #add new geography key/value
      del(result_dictd['us']) #delete current geography key/value
    elif 'county' in result_dictd : 
      result_dictd['geography'] = 'Travis County'
      del(result_dictd['county'])
      del(result_dictd['state'])
    elif 'place' in result_dictd : 
      result_dictd['geography'] = 'Austin'
      del(result_dictd['place'])
      del(result_dictd['state'])
    elif 'state' in result_dictd : 
      result_dictd['geography'] = 'Texas'
      del(result_dictd['state'])
    elif 'metropolitan statistical area/micropolitan statistical area' in result_dictd : 
      result_dictd['geography'] = 'Austin-Round Rock MSA'
      del(result_dictd['metropolitan statistical area/micropolitan statistical area'])
    #append dictionary to a list
    result_list_d.append(result_dictd)


for geokey, geovalue in geographyLevels.items() :
  for year in range(2009, latest_data_year + 1, 1) : 
    urlh = 'https://api.census.gov/data/' + str(year) + '/acs/acs5?get=' + hvars + geovalue + '&key=' + apikey
    #get result
    rh = requests.get(urlh)
    xh = rh.json()
    #store as a dictionary
    result_dicth = dict(zip(xh[0], xh[1]))
    #add year key and value
    result_dicth['year'] = year
    #add race/ethnicity key and value
    result_dicth['race/ethnicity'] = 'White'
    #add geography keys and values in usable format and get rid of current ones
    #note 'state' needs to come after 'county' and 'place' in the elifs because those also include a 'state' key
    if 'us' in result_dicth : 
      result_dicth['geography'] = 'US' #add new geography key/value
      del(result_dicth['us']) #delete current geography key/value
    elif 'county' in result_dicth : 
      result_dicth['geography'] = 'Travis County'
      del(result_dicth['county'])
      del(result_dicth['state'])
    elif 'place' in result_dicth : 
      result_dicth['geography'] = 'Austin'
      del(result_dicth['place'])
      del(result_dicth['state'])
    elif 'state' in result_dicth : 
      result_dicth['geography'] = 'Texas'
      del(result_dicth['state'])
    elif 'metropolitan statistical area/micropolitan statistical area' in result_dicth : 
      result_dicth['geography'] = 'Austin-Round Rock MSA'
      del(result_dicth['metropolitan statistical area/micropolitan statistical area'])
    #append dictionary to a list
    result_list_h.append(result_dicth)


for geokey, geovalue in geographyLevels.items() :
  for year in range(2009, latest_data_year + 1, 1) : 
    urli = 'https://api.census.gov/data/' + str(year) + '/acs/acs5?get=' + ivars + geovalue + '&key=' + apikey
    #get result
    ri = requests.get(urli)
    xi = ri.json()
    #store as a dictionary
    result_dicti = dict(zip(xi[0], xi[1]))
    #add year key and value
    result_dicti['year'] = year
    #add race/ethnicity key and value
    result_dicti['race/ethnicity'] = 'Hispanic or Latino'
    #add geography keys and values in usable format and get rid of current ones
    #note 'state' needs to come after 'county' and 'place' in the elifs because those also include a 'state' key
    if 'us' in result_dicti : 
      result_dicti['geography'] = 'US' #add new geography key/value
      del(result_dicti['us']) #delete current geography key/value
    elif 'county' in result_dicti : 
      result_dicti['geography'] = 'Travis County'
      del(result_dicti['county'])
      del(result_dicti['state'])
    elif 'place' in result_dicti : 
      result_dicti['geography'] = 'Austin'
      del(result_dicti['place'])
      del(result_dicti['state'])
    elif 'state' in result_dicti : 
      result_dicti['geography'] = 'Texas'
      del(result_dicti['state'])
    elif 'metropolitan statistical area/micropolitan statistical area' in result_dicti : 
      result_dicti['geography'] = 'Austin-Round Rock MSA'
      del(result_dicti['metropolitan statistical area/micropolitan statistical area'])
    #append dictionary to a list
    result_list_i.append(result_dicti)

#turn lists of dictionaries into dataframes
dfb = pd.DataFrame(result_list_b)
dfd = pd.DataFrame(result_list_d)
dfh = pd.DataFrame(result_list_h)
dfi = pd.DataFrame(result_list_i)

#rewrite column names to be more descriptive
dfb = dfb.rename(columns={"B17020B_001E": "total", "B17020B_001M": "MOE_total", "B17020B_002E": "total_ibpl", "B17020B_002M": "MOE_total_ibpl", "B17020B_003E": "under_6yrs_ibpl", "B17020B_003M": "MOE_under_6yrs_ibpl", "B17020B_004E": "6_to_11yrs_ibpl", "B17020B_004M": "MOE_6_to_11yrs_ibpl", "B17020B_005E": "12_to_17yrs_ibpl", "B17020B_005M": "MOE_12_to_17yrs_ibpl", "B17020B_006E": "18_to_59yrs_ibpl", "B17020B_006M": "MOE_18_to_59yrs_ibpl", "B17020B_007E": "60_to_74yrs_ibpl", "B17020B_007M": "MOE_60_to_74yrs_ibpl", "B17020B_008E": "75_to_84yrs_ibpl", "B17020B_008M": "MOE_75_to_84yrs_ibpl", "B17020B_009E": "85yrs_and_over_ibpl", "B17020B_009M": "MOE_85yrs_and_over_ibpl", "B17020B_010E": "total_iapl", "B17020B_010M": "MOE_total_iapl", "B17020B_011E": "under_6yrs_iapl", "B17020B_011M": "MOE_under_6yrs_iapl", "B17020B_012E": "6_to_11yrs_iapl", "B17020B_012M": "MOE_6_to_11yrs_iapl", "B17020B_013E": "12_to_17yrs_iapl", "B17020B_013M": "MOE_12_to_17yrs_iapl", "B17020B_014E": "18_to_59yrs_iapl", "B17020B_014M": "MOE_18_to_59yrs_iapl", "B17020B_015E": "60_to_74yrs_iapl", "B17020B_015M": "MOE_60_to_74yrs_iapl", "B17020B_016E": "75_to_84yrs_iapl", "B17020B_016M": "MOE_75_to_84yrs_iapl", "B17020B_017E": "85yrs_and_over_iapl", "B17020B_017M": "MOE_85yrs_and_over_iapl"})
dfd = dfd.rename(columns={"B17020D_001E": "total", "B17020D_001M": "MOE_total", "B17020D_002E": "total_ibpl", "B17020D_002M": "MOE_total_ibpl", "B17020D_003E": "under_6yrs_ibpl", "B17020D_003M": "MOE_under_6yrs_ibpl", "B17020D_004E": "6_to_11yrs_ibpl", "B17020D_004M": "MOE_6_to_11yrs_ibpl", "B17020D_005E": "12_to_17yrs_ibpl", "B17020D_005M": "MOE_12_to_17yrs_ibpl", "B17020D_006E": "18_to_59yrs_ibpl", "B17020D_006M": "MOE_18_to_59yrs_ibpl", "B17020D_007E": "60_to_74yrs_ibpl", "B17020D_007M": "MOE_60_to_74yrs_ibpl", "B17020D_008E": "75_to_84yrs_ibpl", "B17020D_008M": "MOE_75_to_84yrs_ibpl", "B17020D_009E": "85yrs_and_over_ibpl", "B17020D_009M": "MOE_85yrs_and_over_ibpl", "B17020D_010E": "total_iapl", "B17020D_010M": "MOE_total_iapl", "B17020D_011E": "under_6yrs_iapl", "B17020D_011M": "MOE_under_6yrs_iapl", "B17020D_012E": "6_to_11yrs_iapl", "B17020D_012M": "MOE_6_to_11yrs_iapl", "B17020D_013E": "12_to_17yrs_iapl", "B17020D_013M": "MOE_12_to_17yrs_iapl", "B17020D_014E": "18_to_59yrs_iapl", "B17020D_014M": "MOE_18_to_59yrs_iapl", "B17020D_015E": "60_to_74yrs_iapl", "B17020D_015M": "MOE_60_to_74yrs_iapl", "B17020D_016E": "75_to_84yrs_iapl", "B17020D_016M": "MOE_75_to_84yrs_iapl", "B17020D_017E": "85yrs_and_over_iapl", "B17020D_017M": "MOE_85yrs_and_over_iapl"})
dfh = dfh.rename(columns={"B17020H_001E": "total", "B17020H_001M": "MOE_total", "B17020H_002E": "total_ibpl", "B17020H_002M": "MOE_total_ibpl", "B17020H_003E": "under_6yrs_ibpl", "B17020H_003M": "MOE_under_6yrs_ibpl", "B17020H_004E": "6_to_11yrs_ibpl", "B17020H_004M": "MOE_6_to_11yrs_ibpl", "B17020H_005E": "12_to_17yrs_ibpl", "B17020H_005M": "MOE_12_to_17yrs_ibpl", "B17020H_006E": "18_to_59yrs_ibpl", "B17020H_006M": "MOE_18_to_59yrs_ibpl", "B17020H_007E": "60_to_74yrs_ibpl", "B17020H_007M": "MOE_60_to_74yrs_ibpl", "B17020H_008E": "75_to_84yrs_ibpl", "B17020H_008M": "MOE_75_to_84yrs_ibpl", "B17020H_009E": "85yrs_and_over_ibpl", "B17020H_009M": "MOE_85yrs_and_over_ibpl", "B17020H_010E": "total_iapl", "B17020H_010M": "MOE_total_iapl", "B17020H_011E": "under_6yrs_iapl", "B17020H_011M": "MOE_under_6yrs_iapl", "B17020H_012E": "6_to_11yrs_iapl", "B17020H_012M": "MOE_6_to_11yrs_iapl", "B17020H_013E": "12_to_17yrs_iapl", "B17020H_013M": "MOE_12_to_17yrs_iapl", "B17020H_014E": "18_to_59yrs_iapl", "B17020H_014M": "MOE_18_to_59yrs_iapl", "B17020H_015E": "60_to_74yrs_iapl", "B17020H_015M": "MOE_60_to_74yrs_iapl", "B17020H_016E": "75_to_84yrs_iapl", "B17020H_016M": "MOE_75_to_84yrs_iapl", "B17020H_017E": "85yrs_and_over_iapl", "B17020H_017M": "MOE_85yrs_and_over_iapl"})
dfi = dfi.rename(columns={"B17020I_001E": "total", "B17020I_001M": "MOE_total", "B17020I_002E": "total_ibpl", "B17020I_002M": "MOE_total_ibpl", "B17020I_003E": "under_6yrs_ibpl", "B17020I_003M": "MOE_under_6yrs_ibpl", "B17020I_004E": "6_to_11yrs_ibpl", "B17020I_004M": "MOE_6_to_11yrs_ibpl", "B17020I_005E": "12_to_17yrs_ibpl", "B17020I_005M": "MOE_12_to_17yrs_ibpl", "B17020I_006E": "18_to_59yrs_ibpl", "B17020I_006M": "MOE_18_to_59yrs_ibpl", "B17020I_007E": "60_to_74yrs_ibpl", "B17020I_007M": "MOE_60_to_74yrs_ibpl", "B17020I_008E": "75_to_84yrs_ibpl", "B17020I_008M": "MOE_75_to_84yrs_ibpl", "B17020I_009E": "85yrs_and_over_ibpl", "B17020I_009M": "MOE_85yrs_and_over_ibpl", "B17020I_010E": "total_iapl", "B17020I_010M": "MOE_total_iapl", "B17020I_011E": "under_6yrs_iapl", "B17020I_011M": "MOE_under_6yrs_iapl", "B17020I_012E": "6_to_11yrs_iapl", "B17020I_012M": "MOE_6_to_11yrs_iapl", "B17020I_013E": "12_to_17yrs_iapl", "B17020I_013M": "MOE_12_to_17yrs_iapl", "B17020I_014E": "18_to_59yrs_iapl", "B17020I_014M": "MOE_18_to_59yrs_iapl", "B17020I_015E": "60_to_74yrs_iapl", "B17020I_015M": "MOE_60_to_74yrs_iapl", "B17020I_016E": "75_to_84yrs_iapl", "B17020I_016M": "MOE_75_to_84yrs_iapl", "B17020I_017E": "85yrs_and_over_iapl", "B17020I_017M": "MOE_85yrs_and_over_iapl"})

#add the dataframes together (they all have the same columns, so this just adds all the rows beneath each other)
df = pd.concat([dfb, dfd, dfh, dfi])

#convert df to csv
df.to_csv('B17020BDHI_Poverty_ByYouthAndRace_RawData_' + str(latest_data_year) + '.csv', sep='\t', index=False)

#export to Google Drive
file = drive.CreateFile({'parents':[{u'id': googleDriveID}]})
file.SetContentFile('B17020BDHI_Poverty_ByYouthAndRace_RawData_' + str(latest_data_year) + '.csv')
file.Upload()