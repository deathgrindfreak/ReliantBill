import sys
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog

# To make the script more general, accept the filenames as script arguments (e.g. python reliant_script.py bill.xlsx meter.xlsx)
_, BILL_DF_PATH, METER_DF_PATH = sys.argv

#import Reliant bill and Master ESID list into pandas
billdf = pd.read_excel(BILL_DF_PATH,
                       sheet_name='Final-Draft',
                       header=0,
                       skiprows=9,
                       skipfooter=18,
                       usecols=[
                           'ESID', 'FACILITY ID', 'START BILL PERIOD',
                           'END BILL PERIOD', 'PREV MET READ', 'CUR MET READ',
                           'KWH', 'KW', 'Total Due'
                       ],
                       dtype={'ESID': str})

meterdf = pd.read_excel(METER_DF_PATH, dtype={'ESID': str})

#print to excel list of ESID's not on the Master list
esidSet = set(billdf.ESID)
meterdf[~meterdf.ESID.isin(esidSet)].to_excel('wrongBill.xlsx')

# meters not in the master ESID list
meterEsidSet = set(meterdf.ESID)
billdf[~billdf.ESID.isin(meterEsidSet)].to_excel('wrongMeter.xlsx')

#find duplicate ESID's on the Reliant Bill
correctBills = billdf[billdf.ESID.isin(meterEsidSet)]
duplicatedf = correctBills[correctBills.duplicated(['ESID'], keep=False)].copy()

for esid in set(duplicatedf.ESID):
    dups = duplicatedf[duplicatedf.ESID == esid]
    d = len(dups.index)
    for idx in ['START BILL PERIOD', 'END BILL PERIOD', 'PREV MET READ', 'CUR MET READ']:
        if len(dups[idx].unique()) == d:
            print(dups)
