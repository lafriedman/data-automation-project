# CAN project

This project contains the scripts and documentation that I and two team members created for the Community Advancement Network in Austin, TX. The scripts in the `get-raw-data` folder connect to the Census API to get relevant datasets related to poverty statistics. The `transform-data` scripts transform the raw data into either detailed or overview datasets that are used in CAN's dashboards. These scripts are meant to import and export datasets in CAN's Google Drive. API keys and Google Drive IDs have been removed for this public repo.

Below is the original readme file we created for CAN.

## Poverty Folder for Dashboard Drilldowns 04/19/2021

### Overview

This folder contains python code stored as a GoogleColab files that produces outputs as .csv files. This was designed to automate the 
pulling and cleaning US Census data from ACS for tables: B17002, B17024, and B1720BDHI.

Using this code one is able to pull ACS data from all of those tables, store the raw data in GoogleDrive, clean that data, and produce .csv outputs automatically.

### Motivation

This was created to reduce the time and resources previously necessary to perform annually recurring manual data pulling and manipulation. 

### ACS Data Interface

Refer to the corresponding file in the README folder for complete references. That document contains a table linking specific ACS tables to their corresponding python scrips and file outputs. It also contains links to the data that CAN used before this automation was put into practice. This may be helpful to discover how CAN processed this data before this new method was introduced.

Naming Conventions are also included in said folder. The goal is for the naming structure to be fairly intuitive. All files contain a 4 digit year. No folders contain a year.

### Naming conventions

#### Folders

The output data folders are named "TableNumber"_Poverty_"TableDescription" (Ex. B17002_Poverty_General). For consistency each TableNumber corresponds to a specific TableDescription:
* B17002 - "General"
* B17024 - "Youth"
* B17020BDHI - "ByYouthAndRace"  

The raw data folders follow the above naming convention in addition to a descriptor "TableNumber"_Poverty_"TableDescription"_"FolderDescription" (Ex. B17002_Poverty_General_Raw).

#### Files

The RawData files follow the above including the year "TableNumber"_Poverty_"TableDescription"_"FileDescription"_[year in xxxx] (Ex. B17024_Poverty_Youth_RawData_2019)

"FileDescription" is one of the following:
* RawData
* DetailedData
* OverviewData
* RawScript
* OverviewScript
* DetailedScript

The files within OutputData folders are named "TableDescription"_"FileDescription"_"DataDescription"_[year in xxxx]. "DataDescription" is not always applicable.
* Ex. General_DetailedData_2019
* Ex. ByYouthAndRace_OverviewData_TravisPercentAllYears_2019
Please note this is the only variation to the naming convention. This decision was made to reduce file name length.

### Folder Structure

DataOutput – Location for cleaned ACS data in accordance with Naming Convention as mentioned above

PullAndProcess – All necessary files to pull and clean data from ACS website. [This is where CAN representatives run the code necessary 
to produce tidy output data]
* RawData – storage of _RawFolders which contain _RawData
* CodeWorkbook – storage of step-by-step GoogleColab files to run automation

README – Metadata about the folder
* DataDictionary - .xlsx for all tables used in poverty folder
* ACS Data Interface - .docx linking tables, scripts, and outputs. Includes previous data management links and reinforces naming convention
* README - this file
* GitHub Change Tutorial - .pdf of how to make changes to items in Github
      
WebFinal – A staging folder for CAN representatives to store .jpeg and data links for the poverty section of its website 

***Folders can be renamed, but DO NOT DELETE folders as this will change the folder ID's and RawData and OutputData will not export to correct location***

### Workbook Instructions (Runs Colab copy of files in Google Drive)

Go to PullAndProcess
Go to CodeWorkbook
1. Select "Runtime" tab at top of page, then click "Run all"
2. Click on link that populates below. It will open a new tab that displays all of your Google profiles.
3. Select the CAN profile that is connected to the CAN Google Drive
4. Scroll down and click "Allow". A link will then be displayed in the center of the screen.
5. Copy the link and navigate back to this page
6. Paste the link in the white box that is populated below this box and hit "Enter"
7. The rest of the script will run on its own, it should take no more than 5-10 minutes
8. Let script run for about 5 minutes, then check output folders

The first part (steps 1-6) is the most user intensive. It is how the code is able to connect to the GoogleDrive. Typically this is only necessary to do one time.
The rest of the code will run automatically - updated for latest year. 

*Important to note* - If you run the code again, duplicate RawData and OutputData files will be created. You are able to delete all of the OutputData files and run the code again, but keep in mind that duplicates of RawData will be created as well. It could be beneficial to delete the files in both locations to avoid confusion should the need to run the code again for the same year arises. It is outside the scope of this current project, but in the future this may be automated to delete outdated files.
