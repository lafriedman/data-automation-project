# make poverty by race detailed table (total and child percent poverty by race)

#create vars for Google Drive ids
googleDriveIDForImport = 'insert_here'
googleDriveIDForExport = 'insert_here'

#import from Google Drive
#create variable for the file within the folder
df_file =[]
file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(googleDriveIDForImport)}).GetList()
for file in file_list:
  if str(latest_data_year) in file['title']:
     df_file.append(file['id'])

df_file = df_file[len(df_file)-1]

#download the identified folder
downloaded = drive.CreateFile({'id':df_file}) 
downloaded.GetContentFile('Filename.csv')
df = pd.read_csv('Filename.csv', sep='\t')

#Create a copy of all columns except year and geography as numeric.
poverty_race_detail = df.iloc[:, :-3].apply(pd.to_numeric).copy()

#add year and geography columns
poverty_race_detail["race/ethnicity"] = df["race/ethnicity"].copy()
poverty_race_detail["year"] = df["year"].copy()
poverty_race_detail["geography"] = df["geography"].copy()

#group child ages
child_below_poverty = poverty_race_detail[["under_6yrs_ibpl","6_to_11yrs_ibpl", "12_to_17yrs_ibpl"]]
MOE_child_below_poverty = poverty_race_detail[["MOE_under_6yrs_ibpl","MOE_6_to_11yrs_ibpl", "MOE_12_to_17yrs_ibpl"]]
child_above_poverty = poverty_race_detail[["under_6yrs_iapl","6_to_11yrs_iapl", "12_to_17yrs_iapl"]]
MOE_child_above_poverty = poverty_race_detail[["MOE_under_6yrs_iapl","MOE_6_to_11yrs_iapl", "MOE_12_to_17yrs_iapl"]]

#add columns that aggregates child counts for ages 0-17
poverty_race_detail["child_ibpl"] = child_below_poverty.sum(axis=1)
poverty_race_detail["MOE_child_ibpl"] = ((MOE_child_below_poverty**2).sum(axis=1))**.5
poverty_race_detail["child_ibpl_lower_estimate"] = poverty_race_detail["child_ibpl"] - poverty_race_detail["MOE_child_ibpl"]
poverty_race_detail["child_ibpl_upper_estimate"] = poverty_race_detail["child_ibpl"] + poverty_race_detail["MOE_child_ibpl"]
poverty_race_detail["child_iapl"] = child_above_poverty.sum(axis=1)
poverty_race_detail["MOE_child_iapl"] = ((MOE_child_above_poverty**2).sum(axis=1))**.5
poverty_race_detail["child_total"] = poverty_race_detail["child_ibpl"] + poverty_race_detail["child_iapl"]
poverty_race_detail["MOE_child_total"] = ((poverty_race_detail["MOE_child_ibpl"]**2) + (poverty_race_detail["MOE_child_iapl"]**2))**.5

#create percent columns
poverty_race_detail["percent_total_ibpl"] = poverty_race_detail["total_ibpl"] / poverty_race_detail["total"]
poverty_race_detail["MOE_percent_total_ibpl"] = ((poverty_race_detail["MOE_total_ibpl"]**2 - ((poverty_race_detail["percent_total_ibpl"]**2) * (poverty_race_detail["MOE_total"]**2)))**.5) / poverty_race_detail["total"]
poverty_race_detail["percent_total_ibpl_lower_estimate"] = poverty_race_detail["percent_total_ibpl"] - poverty_race_detail["MOE_percent_total_ibpl"]
poverty_race_detail["percent_total_ibpl_upper_estimate"] = poverty_race_detail["percent_total_ibpl"] + poverty_race_detail["MOE_percent_total_ibpl"]

poverty_race_detail["percent_child_ibpl"] = poverty_race_detail["child_ibpl"] / poverty_race_detail["child_total"]
poverty_race_detail["MOE_percent_child_ibpl"] = ((poverty_race_detail["MOE_child_ibpl"]**2 - ((poverty_race_detail["percent_child_ibpl"]**2) * (poverty_race_detail["MOE_child_total"]**2)))**.5) / poverty_race_detail["child_total"]
poverty_race_detail["percent_child_ibpl_lower_estimate"] = poverty_race_detail["percent_child_ibpl"] - poverty_race_detail["MOE_percent_child_ibpl"]
poverty_race_detail["percent_child_ibpl_upper_estimate"] = poverty_race_detail["percent_child_ibpl"] + poverty_race_detail["MOE_percent_child_ibpl"]

#reorder columns, include only the new columns (refer to raw file for the other columns)
cols = ['race/ethnicity','year','geography','total','MOE_total','total_ibpl','MOE_total_ibpl','total_iapl','MOE_total_iapl','percent_total_ibpl','MOE_percent_total_ibpl','percent_total_ibpl_lower_estimate','percent_total_ibpl_upper_estimate', 'child_total', 'MOE_child_total', 'child_ibpl', 'MOE_child_ibpl', 'child_ibpl_lower_estimate', 'child_ibpl_upper_estimate','child_iapl', 'MOE_child_iapl', 'percent_child_ibpl', 'MOE_percent_child_ibpl', 'percent_child_ibpl_lower_estimate', 'percent_child_ibpl_upper_estimate']
poverty_race_detail = poverty_race_detail[cols]

#round numbers to nearest integers, round percents to 4 decimal points
poverty_race_detail = poverty_race_detail.round({"percent_total_ibpl": 4, "MOE_percent_total_ibpl": 4, "percent_total_ibpl_lower_estimate": 4, "percent_total_ibpl_upper_estimate": 4, "MOE_child_total": 0, "MOE_child_ibpl": 0, "child_ibpl_lower_estimate": 0, "child_ibpl_upper_estimate": 0, "MOE_child_iapl": 0, "percent_child_ibpl": 4, "MOE_percent_child_ibpl": 4, "percent_child_ibpl_lower_estimate": 4, "percent_child_ibpl_upper_estimate": 4})
                                             
#change data type to int for integer columns
poverty_race_detail = poverty_race_detail.astype({"MOE_child_total": int, "MOE_child_ibpl": int, "child_ibpl_lower_estimate": int, "child_ibpl_upper_estimate": int, "MOE_child_iapl": int})

#convert df to csv
poverty_race_detail.to_csv('ByYouthAndRace_DetailedData_' + str(latest_data_year) + '.csv', sep='\t', index=False)

#export to Google Drive
file = drive.CreateFile({'parents':[{u'id': googleDriveIDForExport}]})
file.SetContentFile('ByYouthAndRace_DetailedData_' + str(latest_data_year) + '.csv')
file.Upload()