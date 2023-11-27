"""
Rename images to match excel file. A dictionary is created using the excel file

Input images: <ID>_<N>, where N is either 1 or 2


Dictionary Structure
Key: Names in the Einbett-ID column (string)
Value: new names, stored in newName column (string)

How to use: 
    1. Changes imageFolder to image folder path
    2. Change excelPath to where excel file is located
    3. Add more file types to acceptedFileTypes if necessary
    3. Run
"""
import pandas as pd
import os 
import sys
import numpy as np

imagesFolder = ""
excelPath = ""
acceptedFileTypes = ["png"]

#Column in excel file that stores images' current names
keyCol = 'Einbett-ID'

#Add check for multiple space characters
df = pd.read_excel(excelPath)
df[keyCol].replace('', np.nan, inplace=True) #replace any empty string with NaN
df.dropna(subset=[keyCol], inplace=True) #Remove all rows wtih NaN in keyCol

#New image names
df['newName'] = df['Versuch'].astype(str) + "_"+ df['Run'].astype(str).replace('\.0', '', regex=True) + "_"+ df["Position"]

#Create dictionary
kvDict = dict(zip(df[keyCol], df['newName']))

#Open image directory
dirPictures = os.listdir(imagesFolder)

#Check if directory contains files
if(len(dirPictures)  <= 0):
    print('The specified folder is empty or does not contain accepted file types.')
    sys.exit()
else:
    for filename in dirPictures:
        
        #Check if file is of accepted type
        if( '.' in filename and filename.split('.')[-1] in acceptedFileTypes):
            currName = filename.split('.')[0]
            newN = kvDict.get(currName)
            imgType = filename.split('.')[-1]
            
            
            if newN:
                os.rename(imagesFolder + '/' + filename, imagesFolder+ '/' + newN + "." + imgType)
            else:
                print('This image ' + currName + " does not have exist in the excel file.")
           
            
