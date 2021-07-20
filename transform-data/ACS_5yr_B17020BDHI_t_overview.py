#make poverty by race overview tables for Travis County (percent of total population and children under poverty level by race)

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
poverty_race_detail = pd.read_csv('Filename.csv', sep='\t')

#make percent overview table for Travis county, all available years
percent_travis_county = poverty_race_detail.loc[poverty_race_detail['geography'] == "Travis County"]
percent_travis_county = percent_travis_county[["race/ethnicity", "year", "percent_total_ibpl", "percent_child_ibpl"]]
percent_travis_county = percent_travis_county.pivot(index="year", columns="race/ethnicity")

#make percent overview table for Travis County, for latest data year only
percent_travis_county_latest_year = poverty_race_detail.loc[(poverty_race_detail['geography'] == "Travis County") & (poverty_race_detail["year"] == latest_data_year)]
percent_travis_county_latest_year = percent_travis_county_latest_year[["race/ethnicity", "percent_total_ibpl", "percent_child_ibpl"]]
percent_travis_county_latest_year

#make number overview table for Travis county, all available years
num_travis_county = poverty_race_detail.loc[poverty_race_detail['geography'] == "Travis County"]
num_travis_county = num_travis_county[["race/ethnicity", "year", "total_ibpl", "child_ibpl"]]
num_travis_county = num_travis_county.pivot(index="year", columns="race/ethnicity")

#make number overview table for Travis County, for latest data year only
num_travis_county_latest_year = poverty_race_detail.loc[(poverty_race_detail['geography'] == "Travis County") & (poverty_race_detail["year"] == latest_data_year)]
num_travis_county_latest_year = num_travis_county_latest_year[["race/ethnicity", "total_ibpl", "child_ibpl"]]
num_travis_county_latest_year

#four outputs, two for percents (one all years, one for latest year only) and two for numbers (one all years, one for latest year only)

#convert percent_travis_county to csv
percent_travis_county.to_csv('ByYouthAndRace_OverviewData_TravisPercentAllYears_' + str(latest_data_year) + '.csv', sep='\t')
#export to Google Drive
file = drive.CreateFile({'parents':[{u'id': googleDriveIDForExport}]})
file.SetContentFile('ByYouthAndRace_OverviewData_TravisPercentAllYears_' + str(latest_data_year) + '.csv')
file.Upload()

#convert percent_travis_county_latest_year to csv
percent_travis_county_latest_year.to_csv('ByYouthAndRace_OverviewData_TravisPercentLatestYearOnly_' + str(latest_data_year) + '.csv', sep='\t', index=False)
#export to Google Drive
file = drive.CreateFile({'parents':[{u'id': googleDriveIDForExport}]})
file.SetContentFile('ByYouthAndRace_OverviewData_TravisPercentLatestYearOnly_' + str(latest_data_year) + '.csv')
file.Upload()

#convert num_travis_county to csv
num_travis_county.to_csv('ByYouthAndRace_OverviewData_TravisNumAllYears_' + str(latest_data_year) + '.csv', sep='\t')
#export to Google Drive
file = drive.CreateFile({'parents':[{u'id': googleDriveIDForExport}]})
file.SetContentFile('ByYouthAndRace_OverviewData_TravisNumAllYears_' + str(latest_data_year) + '.csv')
file.Upload()

#convert num_travis_county_latest_year to csv
num_travis_county_latest_year.to_csv('ByYouthAndRace_OverviewData_TravisNumLatestYearOnly_' + str(latest_data_year) + '.csv', sep='\t', index=False)
#export to Google Drive
file = drive.CreateFile({'parents':[{u'id': googleDriveIDForExport}]})
file.SetContentFile('ByYouthAndRace_OverviewData_TravisNumLatestYearOnly_' + str(latest_data_year) + '.csv')
file.Upload()