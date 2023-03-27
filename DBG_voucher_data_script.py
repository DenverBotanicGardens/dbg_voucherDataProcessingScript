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
    input_file = 'C:/DBG_voucherDataProcessingScript/TEMPLATE_fungariumVoucherData.xlsx'
    output_file = 'C:/DBG_voucherDataProcessingScript/testOutput.csv'

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
        fieldnames = reader.fieldnames + ['habitat', 'dataGeneralizations', 'locationRemarks', 'occurrenceRemarks', 'description', 'dynamicProperties', 'otherCatalogNumbers']
        # Open the output file
        with open(outfile, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
        
            # Skip the first row below the header. 
            # If the first row below the header is to be skipped only in the example file you sent, then you can delete this line of code.
            next(reader)

            # Execute a function for each new data field        
            for row in reader:
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
        habitat = ''
        if row['plants nearby']:
            habitat += 'Plants nearby: ' + row['plants nearby'] + '. '
        # if row['microHabitat']:
        #     habitat += 'Area immediately surrounding specimen: ' + row['microHabitat'] + '. '
        # if row['land use/disturbance']:
        #     habitat += 'Land use/disturbance history: ' + row['land use/disturbance'] + '. '
        # if row['slope']:
        #     habitat += 'Estimated slope in degrees: ' + row['slope'] + '. '                
    
        # # Translate the aspect values to long strings.
        # aspect_long = '' 
        # if row['aspect'].upper() == 'N':
        #     aspect_long = 'north'
        # elif row['aspect'].upper() == 'E':
        #     aspect_long = 'east'
        # elif row['aspect'].upper() == 'S':
        #     aspect_long = 'south'
        # elif row['aspect'].upper() == 'W':
        #     aspect_long = 'west'
        
        # elif row['aspect'].upper() == 'NE':
        #     aspect_long = 'northeast'
        # elif row['aspect'].upper() == 'NW':
        #     aspect_long = 'northwest'
        # elif row['aspect'].upper() == 'SE':
        #     aspect_long = 'southeast'
        # elif row['aspect'].upper() == 'SW':
        #     aspect_long = 'southwest'
        
        # elif row['aspect'].upper() == 'ENE':
        #     aspect_long = 'east northeast'
        # elif row['aspect'].upper() == 'WNW':
        #     aspect_long = 'west northwest'
        # elif row['aspect'].upper() == 'ESE':
        #     aspect_long = 'east southeast'
        # elif row['aspect'].upper() == 'WSW':
        #     aspect_long = 'west southwest'
        
        # elif row['aspect'].upper() == 'NNE':
        #     aspect_long = 'north northeast'
        # elif row['aspect'].upper() == 'NNW':
        #     aspect_long = 'north northwest'
        # elif row['aspect'].upper() == 'SSE':
        #     aspect_long = 'south southeast'
        # elif row['aspect'].upper() == 'SSW':
        #     aspect_long = 'south southwest'
        # else:
        #     aspect_long = 'UNRECOGNIZED ASPECT VALUE - POSSIBLE ERROR'

        # Populate the field 'habitat'    
        habitat = ''
        if row['plants nearby']:
            habitat += 'Plants nearby: ' + row['plants nearby'] + '. '
        # if row['microHabitat']:
        #     habitat += 'Area immediately surrounding specimen: ' + row['microHabitat'] + '. '
        # if row['land use/disturbance']:
        #     habitat += 'Land use/disturbance history: ' + row['land use/disturbance'] + '. '
        # if row['slope']:
        #     habitat += 'Estimated slope in degrees: ' + row['slope'] + '. '                
        # if row['aspect']:
        #     habitat += 'Slope aspect: ' + aspect_long + '. '          
        # if row['soil']:
        #     habitat += 'Soil description: ' + row['soil'] + '. '
        # if row['terrain']:
        #     habitat += 'Terrain: ' + row['terrain'] + '. '
        # if row['additional habitat descriptions']:
        #     habitat += 'Additional habitat descriptions: ' + row['additional habitat descriptions'] + '.'                
        # row['habitat'] = habitat
            


# Populate new field 'dataGeneralizations'   
def dataGeneralizations(row):
            dataGeneralizations = ''
            if row['Permit']:
                dataGeneralizations += 'Permit: ' + row['Permit'] + '.'
            row['dataGeneralizations'] = dataGeneralizations

            
# Populate new field 'locationRemarks'
def locationRemarks(row):             
            locationRemarks = ''
            # if row['Element Occurrence ID']:
            #     locationRemarks += 'Element Occurrence ID: ' + row['Element Occurrence ID'] + '. '
            if row['Landowner']:
                locationRemarks += 'Landowner: ' + row['Landowner'] + '.'
            row['locationRemarks'] = locationRemarks            
           
            
# Populate new field 'occurrenceRemarks'
# Frequency data are being translated to new values.
def occurrenceRemarks(row):   

            # Translate the Frequency data         
            # freq = ''
            # if row['Frequency'] == 'Abundant' or row['Frequency'] == 'abundant':
            #         freq = 'Abundant (>500)'
            # elif row['Frequency'] == 'Common' or row['Frequency'] == 'common':
            #         freq = 'Common (101-500)'                    
            # elif row['Frequency'] == 'Frequent' or row['Frequency'] == 'frequent':
            #         freq = 'Frequent (11-100)'                          
            # elif row['Frequency'] == 'Occassional' or row['Frequency'] == 'occassional':
            #         freq = 'Occassional (6-10)'                  
            # elif row['Frequency'] == 'Rare' or row['Frequency'] == 'rare':
            #         freq = 'Rare (1-5)'  

            # Populate field 'occurrenceRemarks'         
            occurrenceRemarks = ''
            if row['Project Title']:
                occurrenceRemarks += row['Project Title'].title() + '. '
            # if row['Frequency']:
            #     occurrenceRemarks += 'Estimated frequency within viewshed: ' + freq + '. '
            # if row['Tissue Collected'].lower() == 'y'and row['Tissue Relationship'].lower() == 'same individual':
            #     occurrenceRemarks += 'Tissue sample collected. '
            # if row['Tissue Collected'].lower() == 'y'and row['Tissue Relationship'].lower() == 'same population':
            #     occurrenceRemarks += 'Tissue sample collected from another individual in the same population. '
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


# Populate new field 'materialSample-sampleType'
# def materialSample_sampleType(row):    
#             materialSample_sampleType = ''
#             if row['Tissue Collected'].lower() == 'y':
#                 materialSample_sampleType += 'tissue'
#             row['materialSample-sampleType'] = materialSample_sampleType


# Populate new field 'materialSample-disposition'
# def materialSample_disposition(row):            
#             materialSample_disposition = ''
#             if row['Tissue Collected'].lower() == 'y':
#                 materialSample_disposition += 'in collection'
#             row['materialSample-disposition'] = materialSample_disposition
            
            
# Populate new field 'materialSample-preservationType'
# def materialSample_preservationType(row):
#     materialSample_preservationType = ''            
#     if row['Tissue Collected'].lower() == 'y':
#         materialSample_preservationType += 'dessicated'
#     row['materialSample-preservationType'] = materialSample_preservationType

# Populate new field otherCatalogNumbers
def otherCatalogNumbers(row):
    otherCatalogNumbers = ''
    if row['catalogNumber']:
        otherCatalogNumbers += row['catalogNumber'][6:]
    row['otherCatalogNumbers'] = otherCatalogNumbers
     

if __name__ == "__main__":
    main()
