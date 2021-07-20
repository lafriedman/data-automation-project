#make poverty detailed table

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
newdf = pd.read_csv('Filename.csv', sep='\t')

#Create a copy of all columns except year and geography as numeric.
poverty_detail = newdf.iloc[:, :-2].apply(pd.to_numeric).copy()

#add year and geography columns
poverty_detail["year"] = newdf["year"].copy()
poverty_detail["geography"] = newdf["geography"].copy()

#reorder columns so year and geography are first
cols = poverty_detail.columns.to_list()
cols = cols[-2:] + cols[:-2]
poverty_detail = poverty_detail[cols]

#before adding cumulative columns, separate relevant columns to perform functions on
low_income_cols = poverty_detail[["under_.50", ".50_to_.74", ".75_to_.99", "1_to_1.24", "1.25_to_1.49", "1.50_to_1.74", "1.75_to_1.84", "1.85_to_1.99"]].copy()
low_income_MOE_cols = poverty_detail[["MOE_under_.50", "MOE_.50_to_.74", "MOE_.75_to_.99", "MOE_1_to_1.24", "MOE_1.25_to_1.49", "MOE_1.50_to_1.74", "MOE_1.75_to_1.84", "MOE_1.85_to_1.99"]].copy()
poverty_cols = poverty_detail[["under_.50", ".50_to_.74", ".75_to_.99"]].copy()
poverty_MOE_cols = poverty_detail[["MOE_under_.50", "MOE_.50_to_.74", "MOE_.75_to_.99"]].copy()

#add cumulative columns:

#low-income:

#num low-income = sum under_.50 to 1.85_to_1.99
poverty_detail["num_low_income"] = low_income_cols.sum(axis=1)

#num low-income MOE = sqrt(sum of squares of (MOE_under.50 to MOE_1.85_to_1.99))
poverty_detail["num_low_income_MOE"] = ((low_income_MOE_cols**2).sum(axis=1))**.5

#num low-income lower estimate = num_low_income - num_low_income_MOE
poverty_detail["num_low_income_lower_estimate"] = poverty_detail["num_low_income"] - poverty_detail["num_low_income_MOE"]

#num low-income upper estimate = num_low_income + num_low_income_MOE
poverty_detail["num_low_income_upper_estimate"] = poverty_detail["num_low_income"] + poverty_detail["num_low_income_MOE"]

#percent of low-income = num_low_income / total_pop
poverty_detail["percent_low_income"] = poverty_detail["num_low_income"] / poverty_detail["total_pop"]

#percent of low-income MOE = (sqrt (num_low_income_MOE^2 - (percent_low_income^2 * MOE_total_pop^2))) / total_pop
poverty_detail["percent_low_income_MOE"] = ((poverty_detail["num_low_income_MOE"]**2 - ((poverty_detail["percent_low_income"]**2) * (poverty_detail["MOE_total_pop"]**2)))**.5) / poverty_detail["total_pop"]

#percent low-income lower estimate = percent_low_income - percent_low_income_MOE
poverty_detail["percent_low_income_lower_estimate"] = poverty_detail["percent_low_income"] - poverty_detail["percent_low_income_MOE"]

#percent low-income upper estimate = percent_low_income + percent_low_income_MOE
poverty_detail["percent_low_income_upper_estimate"] = poverty_detail["percent_low_income"] + poverty_detail["percent_low_income_MOE"]

#percent low-income coefficient of variation = ( percent_low_income_MOE / 1.645 ) / percent_low_income
poverty_detail["percent_low_income_coeff_variation"] = (poverty_detail["percent_low_income_MOE"] / 1.645) / poverty_detail["percent_low_income"]

#poverty:

#num of people under poverty level = sum under_.50 to .75_to_.99
poverty_detail["num_poverty"] = poverty_cols.sum(axis=1)

#num poverty MOE = rounded sqrt(sum of squares of (MOE_under.50 to MOE_.75_to_.99))
poverty_detail["num_poverty_MOE"] = ((poverty_MOE_cols**2).sum(axis=1))**.5

#num poverty lower estimate = num_poverty - num_poverty_MOE
poverty_detail["num_poverty_lower_estimate"] = poverty_detail["num_poverty"] - poverty_detail["num_poverty_MOE"]

#num poverty upper estimate = num_poverty + num_poverty_MOE
poverty_detail["num_poverty_upper_estimate"] = poverty_detail["num_poverty"] + poverty_detail["num_poverty_MOE"]

#percent of poverty = num_poverty / total_pop
poverty_detail["percent_poverty"] = poverty_detail["num_poverty"] / poverty_detail["total_pop"]

#percent of poverty MOE = (sqrt (num_poverty_MOE^2 - (percent_poverty^2 * MOE_total_pop^2))) / total_pop
poverty_detail["percent_poverty_MOE"] = ((poverty_detail["num_poverty_MOE"]**2 - ((poverty_detail["percent_poverty"]**2) * (poverty_detail["MOE_total_pop"]**2)))**.5) / poverty_detail["total_pop"]

#percent poverty lower estimate = percent_poverty - percent_poverty_MOE
poverty_detail["percent_poverty_lower_estimate"] = poverty_detail["percent_poverty"] - poverty_detail["percent_poverty_MOE"]

#percent poverty upper estimate = percent_poverty + percent_poverty_MOE
poverty_detail["percent_poverty_upper_estimate"] = poverty_detail["percent_poverty"] + poverty_detail["percent_poverty_MOE"]

#percent poverty coefficient of variation = ( percent_poverty_MOE / 1.645 ) / percent_poverty
poverty_detail["percent_poverty_coeff_variation"] = (poverty_detail["percent_poverty_MOE"] / 1.645) / poverty_detail["percent_poverty"]

#final touches: 

#round numbers to nearest integers, round percents to 4 decimal points
poverty_detail = poverty_detail.round({"num_low_income_MOE": 0, "num_low_income_lower_estimate": 0, "num_low_income_upper_estimate": 0, "num_poverty_MOE": 0, "num_poverty_lower_estimate": 0, "num_poverty_upper_estimate": 0, "percent_low_income": 4, "percent_low_income_MOE": 4, "percent_low_income_lower_estimate": 4, "percent_low_income_upper_estimate": 4, "percent_low_income_coeff_variation": 4, "percent_poverty": 4, "percent_poverty_MOE": 4, "percent_poverty_lower_estimate": 4, "percent_poverty_upper_estimate": 4, "percent_poverty_coeff_variation": 4})

#change data type to int for integer columns
poverty_detail = poverty_detail.astype({"num_low_income_MOE": int, "num_low_income_lower_estimate": int, "num_low_income_upper_estimate": int, "num_poverty_MOE": int, "num_poverty_lower_estimate": int, "num_poverty_upper_estimate": int})

#convert df to csv
poverty_detail.to_csv('General_DetailedData_' + str(latest_data_year) + '.csv', sep='\t', index=False)

#export to Google Drive
#make sure file id corresponds to correct folder
file = drive.CreateFile({'parents':[{u'id': googleDriveIDForExport}]})
file.SetContentFile('General_DetailedData_' + str(latest_data_year) + '.csv')
file.Upload()