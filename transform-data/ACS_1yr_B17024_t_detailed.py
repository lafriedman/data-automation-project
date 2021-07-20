# make child poverty detailed table

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
df3 = pd.read_csv('Filename.csv', sep='\t')

# create dataframe that can be summed (need to change datatype of most columns)
to_sum = df3.iloc[:, 2:].apply(pd.to_numeric).copy() #copy of all columns except year and geography as numeric
to_sum['year'] = df3['year'].copy() #add year column
to_sum['geography'] = df3['geography'].copy() #add geography column

#group columns that will be aggregated (preparing to add all child ages together for each income ratio)
child_total = to_sum[['total_under_6yrs', 'total_6_to_11yrs', 'total_12_to_17yrs']]
MOE_child_total = to_sum[['MOE_total_under_6yrs', 'MOE_total_6_to_11yrs', 'MOE_total_12_to_17yrs']]
child_under_50 = to_sum[['under_6yrs_under_.50', '6_to_11yrs_under_.50', '12_to_17yrs_under_.50']]
MOE_child_under_50 = to_sum[['MOE_under_6yrs_under_.50', 'MOE_6_to_11yrs_under_.50', 'MOE_12_to_17yrs_under_.50']]
child_50_to_99 = to_sum[['under_6yrs_.50_to_.74', '6_to_11yrs_.50_to_.74', '12_to_17yrs_.50_to_.74','under_6yrs_.75_to_.99', '6_to_11yrs_.75_to_.99', '12_to_17yrs_.75_to_.99']]
MOE_child_50_to_99 = to_sum[['MOE_under_6yrs_.50_to_.74', 'MOE_6_to_11yrs_.50_to_.74', 'MOE_12_to_17yrs_.50_to_.74', 'MOE_under_6yrs_.75_to_.99', 'MOE_6_to_11yrs_.75_to_.99', 'MOE_12_to_17yrs_.75_to_.99']] 
child_1_to_124 = to_sum[['under_6yrs_1_to_1.24', '6_to_11yrs_1_to_1.24', '12_to_17yrs_1_to_1.24']]
MOE_child_1_to_124 = to_sum[['MOE_under_6yrs_1_to_1.24', 'MOE_6_to_11yrs_1_to_1.24', 'MOE_12_to_17yrs_1_to_1.24']]
child_125_to_199 = to_sum[['under_6yrs_1.25_to_1.49', '6_to_11yrs_1.25_to_1.49', '12_to_17yrs_1.25_to_1.49','under_6yrs_1.50_to_1.74', '6_to_11yrs_1.50_to_1.74', '12_to_17yrs_1.50_to_1.74','under_6yrs_1.75_to_1.84', '6_to_11yrs_1.75_to_1.84', '12_to_17yrs_1.75_to_1.84','under_6yrs_1.85_to_1.99', '6_to_11yrs_1.85_to_1.99', '12_to_17yrs_1.85_to_1.99']]
MOE_child_125_to_199 = to_sum[['MOE_under_6yrs_1.25_to_1.49', 'MOE_6_to_11yrs_1.25_to_1.49', 'MOE_12_to_17yrs_1.25_to_1.49', 'MOE_under_6yrs_1.50_to_1.74', 'MOE_6_to_11yrs_1.50_to_1.74', 'MOE_12_to_17yrs_1.50_to_1.74','MOE_under_6yrs_1.75_to_1.84', 'MOE_6_to_11yrs_1.75_to_1.84', 'MOE_12_to_17yrs_1.75_to_1.84','MOE_under_6yrs_1.85_to_1.99', 'MOE_6_to_11yrs_1.85_to_1.99', 'MOE_12_to_17yrs_1.85_to_1.99']]

# create table
child_poverty_detail = to_sum.iloc[:, -2:].copy() #adds year and geography columns

#add columns that aggregate child age groups for each income ratio level
child_poverty_detail["child_total"] = child_total.sum(axis=1)
child_poverty_detail["MOE_child_total"] = ((MOE_child_total**2).sum(axis=1))**.5
child_poverty_detail["child_under_.50"] = child_under_50.sum(axis=1)
child_poverty_detail["MOE_child_under_.50"] = ((MOE_child_under_50**2).sum(axis=1))**.5
child_poverty_detail["child_.50_to_.99"] = child_50_to_99.sum(axis=1)
child_poverty_detail["MOE_child_.50_to_.99"] = ((MOE_child_50_to_99**2).sum(axis=1))**.5
child_poverty_detail["child_1_to_1.24"] = child_1_to_124.sum(axis=1)
child_poverty_detail["MOE_child_1_to_1.24"] = ((MOE_child_1_to_124**2).sum(axis=1))**.5
child_poverty_detail["child_1.25_to_1.99"] = child_125_to_199.sum(axis=1)
child_poverty_detail["MOE_child_1.25_to_1.99"] = ((MOE_child_125_to_199**2).sum(axis=1))**.5


#low-income calculations:

#num low-income = sum under_.50 to 1.85_to_1.99
child_poverty_detail["num_low_income"] = child_poverty_detail[["child_under_.50", "child_.50_to_.99","child_1_to_1.24", "child_1.25_to_1.99"]].sum(axis=1)

#num low-income MOE = sqrt(sum of squares of (MOE_under.50 to MOE_1.85_to_1.99))
child_poverty_detail["num_low_income_MOE"] = ((child_poverty_detail[["MOE_child_under_.50", "MOE_child_.50_to_.99","MOE_child_1_to_1.24", "MOE_child_1.25_to_1.99"]]**2).sum(axis=1))**.5

#num low-income lower estimate = num_low_income - num_low_income_MOE
child_poverty_detail["num_low_income_lower_estimate"] = child_poverty_detail["num_low_income"] - child_poverty_detail["num_low_income_MOE"]

#num low-income upper estimate = num_low_income + num_low_income_MOE
child_poverty_detail["num_low_income_upper_estimate"] = child_poverty_detail["num_low_income"] + child_poverty_detail["num_low_income_MOE"]

#percent of low-income = num_low_income / child_total
child_poverty_detail["percent_low_income"] = child_poverty_detail["num_low_income"] / child_poverty_detail["child_total"]

#percent of low-income MOE = (sqrt (num_low_income_MOE^2 - (percent_low_income^2 * MOE_child_total^2))) / child_total
child_poverty_detail["percent_low_income_MOE"] = ((child_poverty_detail["num_low_income_MOE"]**2 - ((child_poverty_detail["percent_low_income"]**2) * (child_poverty_detail["MOE_child_total"]**2)))**.5) / child_poverty_detail["child_total"]

#percent low-income lower estimate = percent_low_income - percent_low_income_MOE
child_poverty_detail["percent_low_income_lower_estimate"] = child_poverty_detail["percent_low_income"] - child_poverty_detail["percent_low_income_MOE"]

#percent low-income upper estimate = percent_low_income + percent_low_income_MOE
child_poverty_detail["percent_low_income_upper_estimate"] = child_poverty_detail["percent_low_income"] + child_poverty_detail["percent_low_income_MOE"]

#percent low-income coefficient of variation = ( percent_low_income_MOE / 1.645 ) / percent_low_income
child_poverty_detail["percent_low_income_coeff_variation"] = (child_poverty_detail["percent_low_income_MOE"] / 1.645) / child_poverty_detail["percent_low_income"]

#poverty calculations:

#num of people under poverty level = sum under_.50 to .75_to_.99
child_poverty_detail["num_poverty"] = child_poverty_detail[["child_under_.50", "child_.50_to_.99"]].sum(axis=1)

#num poverty MOE = rounded sqrt(sum of squares of (MOE_under.50 to MOE_.75_to_.99))
child_poverty_detail["num_poverty_MOE"] = ((child_poverty_detail[["MOE_child_under_.50", "MOE_child_.50_to_.99"]]**2).sum(axis=1))**.5

#num poverty lower estimate = num_poverty - num_poverty_MOE
child_poverty_detail["num_poverty_lower_estimate"] = child_poverty_detail["num_poverty"] - child_poverty_detail["num_poverty_MOE"]

#num poverty upper estimate = num_poverty + num_poverty_MOE
child_poverty_detail["num_poverty_upper_estimate"] = child_poverty_detail["num_poverty"] + child_poverty_detail["num_poverty_MOE"]

#percent of poverty = num_poverty / child_total
child_poverty_detail["percent_poverty"] = child_poverty_detail["num_poverty"] / child_poverty_detail["child_total"]

#percent of poverty MOE = (sqrt (num_poverty_MOE^2 - (percent_poverty^2 * MOE_child_total^2))) / child_total
child_poverty_detail["percent_poverty_MOE"] = ((child_poverty_detail["num_poverty_MOE"]**2 - ((child_poverty_detail["percent_poverty"]**2) * (child_poverty_detail["MOE_child_total"]**2)))**.5) / child_poverty_detail["child_total"]

#percent poverty lower estimate = percent_poverty - percent_poverty_MOE
child_poverty_detail["percent_poverty_lower_estimate"] = child_poverty_detail["percent_poverty"] - child_poverty_detail["percent_poverty_MOE"]

#percent poverty upper estimate = percent_poverty + percent_poverty_MOE
child_poverty_detail["percent_poverty_upper_estimate"] = child_poverty_detail["percent_poverty"] + child_poverty_detail["percent_poverty_MOE"]

#percent poverty coefficient of variation = ( percent_poverty_MOE / 1.645 ) / percent_poverty
child_poverty_detail["percent_poverty_coeff_variation"] = (child_poverty_detail["percent_poverty_MOE"] / 1.645) / child_poverty_detail["percent_poverty"] 

#final touches:

#round numbers to nearest integers, round percents to 4 decimal points
child_poverty_detail = child_poverty_detail.round({"num_low_income_MOE": 0, "num_low_income_lower_estimate": 0, "num_low_income_upper_estimate": 0, "num_poverty_MOE": 0, "num_poverty_lower_estimate": 0, "num_poverty_upper_estimate": 0, "percent_low_income": 4, "percent_low_income_MOE": 4, "percent_low_income_lower_estimate": 4, "percent_low_income_upper_estimate": 4, "percent_low_income_coeff_variation": 4, "percent_poverty": 4, "percent_poverty_MOE": 4, "percent_poverty_lower_estimate": 4, "percent_poverty_upper_estimate": 4, "percent_poverty_coeff_variation": 4})

#change data type to int for integer columns
child_poverty_detail = child_poverty_detail.astype({"num_low_income_MOE": int, "num_low_income_lower_estimate": int, "num_low_income_upper_estimate": int, "num_poverty_MOE": int, "num_poverty_lower_estimate": int, "num_poverty_upper_estimate": int})

#convert df to csv
child_poverty_detail.to_csv('Youth_DetailedData_' + str(latest_data_year) + '.csv', sep='\t', index=False)

#export to Google Drive
#make sure file id corresponds to correct folder
file = drive.CreateFile({'parents':[{u'id': googleDriveIDForExport}]})
file.SetContentFile('Youth_DetailedData_' + str(latest_data_year) + '.csv')
file.Upload()