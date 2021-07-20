#create tidy version of the poverty overview table: percent and number of people below the poverty level

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

#initialize the overview table, tidy version
poverty_ov_tidy = newdf[["year","geography", "total_pop"]].copy()

#change the data type to integer for the columns that need to be added together
rows_to_add = newdf.loc[:,["under_.50", ".50_to_.74", ".75_to_.99"]].apply(pd.to_numeric)

#add the column that totals below poverty to the overview table
poverty_ov_tidy["num_below_poverty_level"] = rows_to_add.iloc[:,:].sum(axis=1)

#change data type of total column to integer
poverty_ov_tidy["total_pop"] = poverty_ov_tidy["total_pop"].apply(pd.to_numeric)

#add the percent column rounded to 1 decimal
poverty_ov_tidy["percent_below_poverty_level"] = round(((poverty_ov_tidy["num_below_poverty_level"] / poverty_ov_tidy["total_pop"]) * 100), 1)

#drop the total population column
poverty_ov_tidy = poverty_ov_tidy.drop(columns='total_pop')

#note poverty_ov_tidy is difficult to make charts with in excel, but bc it is tidy it will be useful for charts in Tableau and other software
#so will also make versions of poverty_ov_tidy optimized for excel charts, one for percentages and one for number 

#make version of poverty_ov_tidy, percentages
#this output is: Percent of indivudals living below the Federal Poverty Level
poverty_ov_percent = poverty_ov_tidy.pivot(index="year", columns="geography", values="percent_below_poverty_level")
column_order = ['Austin', 'Austin-Round Rock MSA', 'Travis County', 'Texas', 'US'] #make list in order we want the columns to be in
poverty_ov_percent = poverty_ov_percent.reindex(column_order, axis=1) #reorder columns

#make version of poverty_ov_tidy, number
#this output is: Number of indivdiuals living below the Federal Poverty Level 
poverty_ov_number = poverty_ov_tidy.pivot(index="year", columns="geography", values="num_below_poverty_level")
column_order = ['Austin', 'Austin-Round Rock MSA', 'Travis County', 'Texas', 'US'] #make list in order we want the columns to be in
poverty_ov_number = poverty_ov_number.reindex(column_order, axis=1) #reorder columns

# export poverty_ov_tidy:
poverty_ov_tidy.to_csv('General_OverviewData_Tidy_' + str(latest_data_year) + '.csv', sep='\t', index=False) #convert df to csv
file = drive.CreateFile({'parents':[{u'id': googleDriveIDForExport}]}) #export to Google Drive 
file.SetContentFile('General_OverviewData_Tidy_' + str(latest_data_year) + '.csv')
file.Upload()

# export poverty_ov_percent:
poverty_ov_percent.to_csv('General_OverviewData_Percent_' + str(latest_data_year) + '.csv', sep='\t') #convert df to csv
file = drive.CreateFile({'parents':[{u'id': googleDriveIDForExport}]}) #export to Google Drive 
file.SetContentFile('General_OverviewData_Percent_' + str(latest_data_year) + '.csv')
file.Upload()

# export poverty_ov_number:
poverty_ov_number.to_csv('General_OverviewData_Number_' + str(latest_data_year) + '.csv', sep='\t') #convert df to csv
file = drive.CreateFile({'parents':[{u'id': googleDriveIDForExport}]}) #export to Google Drive
file.SetContentFile('General_OverviewData_Number_' + str(latest_data_year) + '.csv')
file.Upload()