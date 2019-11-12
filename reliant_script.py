import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog

#import Reliant bill and Master ESID list into pandas
billdf = pd.read_excel(r'C:\Users\bbell\OneDrive - CrownQuest Operating\Documents\Electric Bills\20190925_12.23.57_CROWNQUESTOPERATINGCOLLC_SMRY.xlsx', sheet_name='Final-Draft', header=0, skiprows=9, skipfooter=18, usecols=['ESID', 'FACILITY ID','START BILL PERIOD', 'END BILL PERIOD', 'PREV MET READ', 'CUR MET READ', 'KWH', 'KW', 'Total Due'])
meterdf = pd.read_excel(r'C:\Users\bbell\OneDrive - CrownQuest Operating\Documents\Electric Bills\Master ESID Sheet.xlsx')

#convert ESID's to float
billdf['ESID'] = billdf['ESID'].astype(float)
meterdf['ESID'] = meterdf['ESID'].astype(float)

#find ESID's that are not on Reliant's bill
nobilldf = mergedf.loc[mergedf['_merge'] == 'left_only'].copy()

#find ESID's that are not on the Master list
nomasterdf = mergedf.loc[mergedf['_merge'] == 'right_only'].copy()

#print to excel list of ESID's not on the Master list
nomasterdf['ESID'] = nomasterdf['ESID'].map('{:.0f}'.format)
nomasterdf.to_excel('wrongbill.xlsx')

#find duplicate ESID's on the Reliant Bill
duplicatedf = billdf[billdf.duplicated(['ESID'], keep=False)].copy()
duplicatedf['ESID'] = duplicatedf['ESID'].astype(float)

#filter out all dupliacates not on the master ESID list
duplicatemergedf = pd.merge(duplicatedf, meterdf, how='inner', indicator=True)
duplicatemergedf.sort_values(by=['START BILL PERIOD'])


#find ESID's from duplicate list that have conflicting start/end dates and start/end meter readings
meterlist = np.array(meterdf['ESID'])

for meterlist in duplicatemergedf['ESID']:  #don't exactly understand how you can loop an array into a dataframe column
    slicedf = duplicatemergedf.loc[duplicatemergedf['ESID'] == meterlist].copy()  #don't quite understand how this isolates each ESID
    slicedf.sort_values(by=['START BILL PERIOD'])
    if slicedf.iat[0,3] >= slicedf.iat[1,2] and slicedf.iat[0,5] > slicedf.iat[1,4]:
            #slicedf.drop_duplicates(subset="ESID", keep='first', inplace=True)
            #slicedf.to_excel('duplicates.xlsx')
            #evenslicedf = slicedf.iloc[::4,:].copy()
            #newevenslicedf = [evenslicedf.drop_duplicates(subset="ESID", keep='first', inplace=True)].copy()
            #oddslicedf = slicedf.iloc[1::4,:]
            #mergeslicedf = pd.merge(evenslicedf, oddslicedf, how='outer')
            #print(newevenslicedf)
            #newmeterlist = meterlist[::2]
            print(meterlist)

#This outputs a dataframe with 4 rows per ESID, it should only output 2 rows (2 months worth of billing). However I try to slice the result, I either get a "None" output or I get 4 rows of data per ESID.
