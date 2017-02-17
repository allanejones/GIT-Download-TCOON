def download_Tidal_data(stn_ID ='036', begin_date='10.01.2007',
                        end_date='today', dwld_specs = ['pwl','bwl','harmwl'],
                        stn_name = 'unspecified', file_name = 'unspecified',
                        file_directory = 'current', folder_name='unknown'):
    """\
Basic input:
download_Tidal_data(stn_ID ='036', begin_date='10.01.2007',
                        end_date='today', dwld_specs = ['pwl','bwl','harmwl'],
                        file_name = 'unspecified', file_directory = 'current',
                        folder_name='unknown'):

This script (written using Python3.3) is desgined to download the tidal
data from a designated TCOON tidal station over the designated time-period.

The begin date for this script must be provided by the user. There is no
date of initiation for the tidal gaging stations. The date information
must be provided in the following format "mm.dd.yyyy" (ex - 10.01.2007
represents October 1, 2007).

When reading in the 

This script uses the following site to predict the tidal stage for the
requested dates:
TCOON....
permalink ==> http://www.cbi.tamucc.edu/data/036

Example link:
"http://lighthouse.tamucc.edu/pd?stnlist=036&
serlist=pwl%2Cbwl%2Charmwl&when=10.01.2007-12.02.2014
&whentz=CST6CDT&-action=c&unit=metric&elev=msl&interval=1800&
datefmt=%25m-%25d-%25Y%20%25H%25M"

The selections within the example link are (using TCOON lingo):
Sources         = 036
Series            = primary (pwl), backup (bwl), and harmonic predicted
                            water level (harmwl)
Dates             = 10.01.2007-12.02.2014 in US. Central Time (CST/CDT)
Format           = Text Columns
Units              = Metric
Interval         = Every half hour at :00 and :30
Date Format = mm-dd-yyyy hhmm (24 hour)

Description of inputs:  ALL INPUTS ARE STRINGS.

Remember:
!!! ALL INPUTS ARE STRINGS !!!!
"""

### find the end_date, if used 'today'
    if end_date == 'today':
        import time
        time_fmt = "%m.%d.%Y"
        end_date = time.strftime(time_fmt)

### Imports
    print('Beginning download for tidal station: '+stn_ID+' '+stn_name+'\n')
    import urllib.request
    import re
    import os
    import sys
    from bs4 import BeautifulSoup
    from bs4 import NavigableString

### Creating the dowload URL by inserting the provided information
    URL = ("http://lighthouse.tamucc.edu/pd?stnlist="+stn_ID+"&"+
           "serlist="+"%2C".join(dwld_specs)+"&when="+begin_date+"-"+
           end_date+"&whentz=CST6CDT&-action=c&unit=metric&elev=msl"+
           "&interval=1800&datefmt=%25m-%25d-%25Y%20%25H%25M")

## Printing a URL update
    print('The URL used in the attempted download is as follows: \n'+URL+'\n\n')

### Obtaining the metadata from the website
    website = urllib.request.urlopen(URL)
    source_page = website.read()
    soup = BeautifulSoup(source_page)

### Obtaining the body of the metadata
    data = soup.body.string
    print('Have obtained data for the gaging station: '+stn_ID+' '+stn_name)

## Updating station name to have an underscore
    save_date = [begin_date[-4:]+'-'+begin_date[:-5].replace('.','-'),
                 end_date[-4:]+'-'+end_date[:-5].replace('.','-')]

### Creating a filename for the file to be saved
    if file_name == 'unspecified' and stn_name != 'unspecified':
        file_name = (stn_ID+'_'+stn_name.replace(' ','_')+'_data_from_'+
                     save_date[0]+'_to_'+save_date[1]+'.txt')
    elif file_name == 'unspecified'and stn_name == 'unspecified':
        file_name = (stn_ID+'_data_from_'+save_date[0]+'_to_'+
                     save_date[1]+'.txt') 

### Creating the file directory for saving purposes
    if file_directory == 'current' and folder_name == 'unknown':
        file_directory = os.getcwd()
    elif file_directory == 'current' and folder_name !='unknown':
        file_directory = os.getcwd()
        file_directory = file_directory + '\\' + folder_name
    elif file_directory != 'current' and folder_name != 'unknown':
        file_directory += '\\' + folder_name

### Re-write the data to replace the spacing to have a comma
### for ease of reading in matlab
    for num in [6,5,3,2]:
        data = data.replace(num*" ", ',')
    
        
### Writing the data (string) to the file
    # concatenate directory and filename to create full save path    
    path_full = file_directory + '\\' + file_name
    try:
        
        # checking to see if the file path exists, if not we create it.
        if not os.path.exists(file_directory):
            os.makedirs(file_directory)

        #  attempting to write the file
        with open(path_full, "w") as file_out:               
            file_out.write(data) # writing the data to the file
            print("The requested file has been written and saved. \n")

    # If the attempt to write the file fails, the script reports an error
    except IOError as e:
        print("\nCould not write to file. \n")
        sys.exit(1)


    
