#make overview table - percent of children and youth living below the poverty level

#create vars for Google Drive ids
googleDriveIDForImport = 'insert_here'
googleDriveIDForExport = 'insert_here'

#import from Google Drive
#create variable for the file within the folder
df_file =[]
file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(googleDriveIDForImport)}).GetList()
for file in file_list:
  if str('DetailedData') and str(latest_data_year) in file['title']:
     df_file.append(file['id'])

df_file = df_file[len(df_file)-1]

#download the identified folder
downloaded = drive.CreateFile({'id':df_file}) 
downloaded.GetContentFile('Filename.csv')
child_poverty_overview = pd.read_csv('Filename.csv', sep='\t')

#create overview table
child_poverty_overview = child_poverty_detail.pivot(index="year", columns="geography", values="percent_poverty")

#reorder columns
child_poverty_overview_cols = ['Austin', 'Travis County', 'Austin-Round Rock MSA', 'Texas', 'US']
child_poverty_overview = child_poverty_overview[child_poverty_overview_cols]

#convert df to csv
child_poverty_overview.to_csv('Youth_OverviewData_' + str(latest_data_year) + '.csv', sep='\t')

#export to Google Drive
#make sure file id corresponds to correct folder
file = drive.CreateFile({'parents':[{u'id': googleDriveIDForExport}]})
file.SetContentFile('Youth_OverviewData_' + str(latest_data_year) + '.csv')
file.Upload()