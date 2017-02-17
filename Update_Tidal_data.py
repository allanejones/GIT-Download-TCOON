## The point of this file is to open the 'tidal_Station_List.txt' file, obtain
## the TCOON gage station IDs and names from the file, and send them
## to the download_Tidal_data() function to download the most
## up-to-date data from each of the listed sites.

import re
import os
from Download_Tidal import download_Tidal_data

## Setting up the proper file path to the prepared list document
file_directory = os.getcwd()

file_name = 'tidal_Station_List.txt'

full_path = file_directory +'\\'+ file_name

## Opens the specified file to read ('r')
stnNM_list = []
stnID_list = []
with open(full_path, 'r') as fid:
    ## Reads lines in file and removes site numbers
    for line in fid:
        # obtains ID for lines that start with digits
        if re.match('^\d',line):
            # Sppends station ID to list
            stnID_list.append(line[:re.search('[^\d]',line).end()-1])

            # appends the station name to proper list
            name = ''
            for letter in line:
                 # Loop and IF isolate the letters from string
                 if letter.isalpha() or letter == ' ':
                     name+=letter

            # append the string 'name' to list
            stnNM_list.append(name)
            
final_list = list(zip(stnID_list, stnNM_list))

## Looping through the entries in "Final List" to obtain each station's data
for entry in final_list :
    test = download_Tidal_data(stn_ID = entry[0], stn_name = entry[1],
                      folder_name = 'Tidal Downloads', begin_date = '10.01.2007',
                       file_directory = file_directory)

    print('Finished downloading the file for Station: '+entry[0]+' '+
          entry[1]+'\n')
    print('############################################### \n\n')

    
print('FINISHED THE TIDAL FILE!! WOOHOO!!')
