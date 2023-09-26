# -*- coding: utf-8 -*-
"""
Created on Thu Mar  10 20:43:03 2023

@author: Ernie Marx & Richard Levy

Reformatting of data for fungarium voucher records

This script adds and populates new fields in the herbarium voucher data file.

User must enter paths for input and output files.
Paths can be entered as command line arguments or inside the script.
Use mode = 1 for command line arguments
Use mode = 2 to name file paths inside script

Input and/or output files can be .csv or .xlsx.
File names cannot contain periods ('.') other than the file extension.
 
If the input is .xlsx, the first sheet of the Excel file is used to create a temporary input csv file ('temp_in.csv') 
in the working directory. The temporary file is removed at script completion.

If the output is .xlsx, a temporary output csv file ('temp_out.csv')  
is created in the working directory. The temporary file is removed at script completion.
"""


import csv, os, sys
import pandas as pd
import requests
import urllib
import json
# Set mode = 1 to enter file names as command line arguments
# Set mode = 2 to enter file names inside this script
mode = 2

if mode == 1:
    if len(sys.argv) != 3:
        print("Usage: python name_of_script.py input_file output_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

#-------------------------------------------------
# Name input and output files here for mode = 2
#-------------------------------------------------    
if mode == 2:
    input_file = 'C:/dbg_voucherDataProcessingScript/TEMPLATE_DataFields_Vouchers_Fungi_gnrTest.xlsx'
    output_file = 'C:/dbg_voucherDataProcessingScript/testOutput.csv'

def main():
    
    # If the INPUT file is an .xlsx spreadsheet, create a temporary .csv file from the first sheet in the spreadsheet. 
    ext_in = input_file.split('.')[1]
    if ext_in == "csv":
        input_csv = input_file
    if ext_in == "xlsx":
        excel_file = pd.read_excel(input_file, sheet_name=0)
        excel_file.to_csv('temp_in.csv', index=False)
        input_csv = 'temp_in.csv'       

    # If the OUTPUT file is an .xlsx spreadsheet, create a temporary .csv outfile and convert to .xlsx at end of script.    
    ext_out = output_file.split('.')[1]
    if ext_out == "csv":  
        outfile = output_file
    if ext_out == "xlsx":
        outfile = 'temp_out.csv'  
        
    # Read the csv file
    with open(input_csv, 'r') as infile:
        reader = csv.DictReader(infile)
        # Add a list of new field names to be added to existing fields
        fieldnames = reader.fieldnames + ['habitat', 'dataGeneralizations', 'locationRemarks', 'occurrenceRemarks', 'description', 'dynamicProperties', 'otherCatalogNumbers', 'minimumElevationInMeters_USGS', 'georeferenceRemarks','GNVmatchType','GNVmatchedCanonicalFull','GNVisSynonym','GNVdataSourceTitleShort']
        # Open the output file
        with open(outfile, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
        
            # Skip the first row below the header. 
            # If the first row below the header is to be skipped only in the example file you sent, then you can delete this line of code.
            next(reader)

            # Execute a function for each new data field        
            for row in reader:
                minimumElevationInMeters(row)
                verifyScientificNames(row)
                habitat(row)
                dataGeneralizations(row)
                locationRemarks(row)
                occurrenceRemarks(row)
                description(row)
                dynamicProperties(row)
                associatedTaxa(row)
                otherCatalogNumbers(row)
            
                writer.writerow(row)
                
        # Export the outfile as an Excel file if user indicated .xlsx
        if ext_out == "xlsx":
            df = pd.read_csv('temp_out.csv')
            df.to_excel(output_file, index=False)

        # Clean up
        infile.close()
        outfile.close()
        
        # Remove the temporary .csv file if the input file was Excel
        if os.path.exists('temp_in.csv'):
            os.remove('temp_in.csv')
        if os.path.exists('temp_out.csv'):
            os.remove('temp_out.csv')            
#-------------------------------------------------------------
# Each new data field is defined in the functions below
#-------------------------------------------------------------

# define new field 'habitat' 
def habitat(row):         
        # Populate the field 'habitat'    
        habitat = ''
        if row['plants nearby']:
            habitat += 'Plants nearby: ' + row['plants nearby'] + '. '              
        row['habitat'] = habitat
            


# Populate new field 'dataGeneralizations'   
def dataGeneralizations(row):
            dataGeneralizations = ''
            if row['Permit']:
                dataGeneralizations += 'Permit: ' + row['Permit'] + '.'
            row['dataGeneralizations'] = dataGeneralizations

            
# Populate new field 'locationRemarks'
def locationRemarks(row):             
            locationRemarks = ''
            if row['Landowner']:
                locationRemarks += 'Landowner: ' + row['Landowner'] + '.'
            row['locationRemarks'] = locationRemarks            
           
            
# Populate new field 'occurrenceRemarks'
# Frequency data are being translated to new values.
def occurrenceRemarks(row):   
            # Populate field 'occurrenceRemarks'         
            occurrenceRemarks = ''
            if row['Project Title']:
                occurrenceRemarks += row['Project Title'].title() + '. '
            if row['collector notes']:
                occurrenceRemarks += row['collector notes'].title() + '. '
            if row['iNaturalist ID']:
                occurrenceRemarks += "<a href='https://inaturalist.org/observations/" + row['iNaturalist ID'] + "' target='_blank' style='color: blue';>iNaturalist Record: " + row['iNaturalist ID']  + "</a>."
            row['occurrenceRemarks'] = occurrenceRemarks              
            
# Populate new field 'description'
def description(row):
            description = ''
            if row['habit']:
                description += 'Habit: ' + row['habit'] + '. '
            if row['odor']:
                description += 'Odor: ' + row['odor'] + '. '
            if row['taste']:
                description += 'Taste: ' + row['taste'] + '. '
            if row['sporocarp form']:
                description += 'Sporocarp form: ' + row['sporocarp form'] + '. '
            if row['pileus']:
                description += 'Pileus: ' + row['pileus'] + '. '
            if row['context']:
                description += 'Context: ' + row['context'] + '.'
            if row['hymenophore']:
                description += 'Hymenophore: ' + row['hymenophore'] + '.'
            if row['stipe']:
                description += 'Stipe: ' + row['stipe'] + '. '
            if row['micro']:
                description += 'Microscopic analysis: ' + row['micro'] + '.'                      
            row['description'] = description
                
# Populate new field 'dynamicProperties'
def dynamicProperties(row):
            dynamicProperties = '' 
            dynamicProperties += '{'            
            if row['habit']:
                dynamicProperties += '"habit":"' + row['habit'] + '",'
            if row['odor']:
                dynamicProperties += '"odor":"' + row['odor'] + '",'
            if row['taste']:
                dynamicProperties += '"taste":"' + row['taste'] + '",'
            if row['sporocarp form']:
                dynamicProperties += '"sporocarpForm":"' + row['sporocarp form'] + '",'
            if row['pileus']:
                dynamicProperties += '"pileus":"' + row['pileus'] + '",'
            if row['context']:
                dynamicProperties += '"context":"' + row['context'] + '",'
            if row['hymenophore']:
                dynamicProperties += '"hymenophore":"' + row['hymenophore'] + '",'
            if row['stipe']:
                dynamicProperties += '"stipe":"' + row['stipe'] + '",'
            if row['micro']:
                dynamicProperties += '"microscopicAnalysis":"' + row['micro'] + '",'

            # remove dangling comma if exists                
            if dynamicProperties.endswith(','):
                dynamicProperties = dynamicProperties.rstrip(",")
            dynamicProperties += '}'

            # if JSON is empty then remove
            if dynamicProperties == '{}':
                dynamicProperties = ''
                
            row['dynamicProperties'] = dynamicProperties                
            
            
# update 'associatedTaxa'
# This updates an existing field rather than populating a new field
def associatedTaxa(row):            
            associatedTaxa = ''
            if row['host']:
                associatedTaxa += row['associatedTaxa'] + ', host: ' + row['host']
            # remove dangling comma if exists                
            if associatedTaxa.endswith(','):
                associatedTaxa = associatedTaxa.rstrip(",")
            if associatedTaxa.startswith(','):
                associatedTaxa = associatedTaxa.lstrip(" ,")
            row['associatedTaxa'] = associatedTaxa

# Populate new field otherCatalogNumbers
def otherCatalogNumbers(row):
    otherCatalogNumbers = ''
    if row['catalogNumber']:
        otherCatalogNumbers += row['catalogNumber'][6:]
    row['otherCatalogNumbers'] = otherCatalogNumbers

#ELEVATION FROM USGS API---------------------------------------------------------------------------------------------
# USGS Elevation Point Query Service
# Generates elevation values from coordinates, when supplied.
url = r'https://epqs.nationalmap.gov/v1/json?'

#create the lat & lon variables
lon = ''
lat = ''
# create an Empty DataFrame object
df = pd.DataFrame()
#create empty variable for elevation value result
elevationResult = ''

#Populate new field 'minimumElevationInMeters'
def minimumElevationInMeters(row):
     minimumElevationInMeters = ''
     #if there are latitude and longitude values, set the variables and then add to the dataframe
     if row['decimalLongitude'] and row['decimalLatitude']:
          lon = row['decimalLongitude']
          lat = row['decimalLatitude']
          df = pd.DataFrame({
          'lat': lat,
          'lon': lon
          }, index=[0])
          #run function that calls API
          elevation_function(df, 'lat', 'lon')
          georeferenceRemarks(row)
          #set row value to result rfom API call
     row['minimumElevationInMeters_USGS'] = elevationResult

#Function to call the USGS API
def elevation_function(df, lat_column, lon_column):
    for lat, lon in zip(df[lat_column], df[lon_column]):
    # define rest query params
     params = {
        'output': 'json',
        'x': lon,
        'y': lat,
        'units': 'Meters'
    }
    
    # format query string and return query value
    result = requests.get((url + urllib.parse.urlencode(params)))
    #elevations.append(result.json()['USGS_Elevation_Point_Query_Service']['Elevation_Query']['Elevation'])
    #new 2023:
    #print(json.dumps((result.json()['value'])))
    global elevationResult
    elevationResult = json.dumps((result.json()['value'])).replace('"','')[:-8]
    # print("value from api" + json.dumps((result.json()['value'])))

# Populate new field 'georeferenceRemarks' with note about elevation source. Executes within minimElevationInMeters function
def georeferenceRemarks(row):
    georeferenceRemarks = ''            
    remark = "Elevation value calculated using USGS Bulk Point Query Service (V 2.0)"
    row['georeferenceRemarks'] = remark




#SCIENTIFIC NAME VALIDATION FROM GLOBAL NAMES INDEX API---------------------------------------------------------------------------------------------
# Global Names Resolver API endpoint
verifier_api_url = "https://verifier.globalnames.org/api/v1/verifications"

#create the scientificName variable
nameStrings = ''
# create an Empty DataFrame object
df = pd.DataFrame()
#create empty variable for results
gnvResult = {}

#Populate new field 'minimumElevationInMeters'
def verifyScientificNames(row):
     #if there is a scientificName, set as variable and then add to the dataframe
    if row['scientificName']:
            nameStrings = row['scientificName']
            df = pd.DataFrame({
            'nameStrings': nameStrings
            }, index=[0])
            #run function that calls API
            gnv_function(df, 'nameStrings')
            #set row value to result rfom API call
    # row['GNVmatchType'] = gnvResult.matchType
    # row['GNVmatchedCanonicalFull'] = gnvResult.matchedCanonicalFull
    # row['GNVisSynonym'] = gnvResult.isSynonym
    # row['GNVdataSourceTitleShort'] = gnvResult.dataSourceTitleShort

def gnv_function(df, nameStrings_column):
    for nameStrings in zip(df[nameStrings_column]):
    # define rest query params
     params = {
        'nameStrings': nameStrings,
        'dataSources': 5,
        'withAllMatches': True,
        'withCapitalization': True,
        'withSpeciesGroup': True,
        'withUninomialFuzzyMatch': False,
        'withStats': True,
        'mainTaxonThreshold': 0.6
    }
    print(params)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()