#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 22:34:40 2023

@author: amarabbani
"""


import streamlit as st
st.title("Diabetes Patient Readmission: Addressing the Cost and Quality Challenges")



#Loading libraries 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#loading Dataset
df = pd.read_csv("/Users/amarabbani/Downloads/diabetic_data.csv")

print(df)

#displaying first 10 rows of data
df.head(10).T


#checking shape of the dataset
df.shape


#Checking data types of each variable
df.dtypes


#Checking for missing values in dataset
#In the dataset missing values are represented as '?' sign
for col in df.columns:
    if df[col].dtype == object:
         print(col,df[col][df[col] == '?'].count())
         
         
# gender was coded differently so we use a custom count for this one            
print('gender', df['gender'][df['gender'] == 'Unknown/Invalid'].count())  


#dropping columns with large number of missing values
df = df.drop(['weight','payer_code','medical_specialty'], axis = 1)
print(df)

import matplotlib.pyplot as plt


drop_Idx = set(df[(df['diag_1'] == '?') & (df['diag_2'] == '?') & (df['diag_3'] == '?')].index)

drop_Idx = drop_Idx.union(set(df['diag_1'][df['diag_1'] == '?'].index))
drop_Idx = drop_Idx.union(set(df['diag_2'][df['diag_2'] == '?'].index))
drop_Idx = drop_Idx.union(set(df['diag_3'][df['diag_3'] == '?'].index))
drop_Idx = drop_Idx.union(set(df['race'][df['race'] == '?'].index))
drop_Idx = drop_Idx.union(set(df[df['discharge_disposition_id'] == 11].index))
drop_Idx = drop_Idx.union(set(df['gender'][df['gender'] == 'Unknown/Invalid'].index))
new_Idx = list(set(df.index) - set(drop_Idx))
df = df.iloc[new_Idx]




df = df.drop(['citoglipton', 'examide'], axis = 1)


#Checking for missing values in the data
for col in df.columns:
    if df[col].dtype == object:
         print(col,df[col][df[col] == '?'].count())
            
print('gender', df['gender'][df['gender'] == 'Unknown/Invalid'].count())  



df['service_utilization'] = df['number_outpatient'] + df['number_emergency'] + df['number_inpatient']



keys = ['metformin', 'repaglinide', 'nateglinide', 'chlorpropamide', 'glimepiride', 'glipizide', 'glyburide', 'pioglitazone', 'rosiglitazone', 'acarbose', 'miglitol', 'insulin', 'glyburide-metformin', 'tolazamide', 'metformin-pioglitazone','metformin-rosiglitazone', 'glimepiride-pioglitazone', 'glipizide-metformin', 'troglitazone', 'tolbutamide', 'acetohexamide']
for col in keys:
    colname = str(col) + 'temp'
    df[colname] = df[col].apply(lambda x: 0 if (x == 'No' or x == 'Steady') else 1)
df['numchange'] = 0
for col in keys:
    colname = str(col) + 'temp'
    df['numchange'] = df['numchange'] + df[colname]
    del df[colname]
    
df['numchange'].value_counts() 



# re-encoding admission type, discharge type and admission source into fewer categories

df['admission_type_id'] = df['admission_type_id'].replace(2,1)
df['admission_type_id'] = df['admission_type_id'].replace(7,1)
df['admission_type_id'] = df['admission_type_id'].replace(6,5)
df['admission_type_id'] = df['admission_type_id'].replace(8,5)

df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(6,1)
df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(8,1)
df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(9,1)
df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(13,1)
df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(3,2)
df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(4,2)
df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(5,2)
df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(14,2)
df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(22,2)
df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(23,2)
df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(24,2)
df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(12,10)
df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(15,10)
df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(16,10)
df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(17,10)
df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(25,18)
df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(26,18)

df['admission_source_id'] = df['admission_source_id'].replace(2,1)
df['admission_source_id'] = df['admission_source_id'].replace(3,1)
df['admission_source_id'] = df['admission_source_id'].replace(5,4)
df['admission_source_id'] = df['admission_source_id'].replace(6,4)
df['admission_source_id'] = df['admission_source_id'].replace(10,4)
df['admission_source_id'] = df['admission_source_id'].replace(22,4)
df['admission_source_id'] = df['admission_source_id'].replace(25,4)
df['admission_source_id'] = df['admission_source_id'].replace(15,9)
df['admission_source_id'] = df['admission_source_id'].replace(17,9)
df['admission_source_id'] = df['admission_source_id'].replace(20,9)
df['admission_source_id'] = df['admission_source_id'].replace(21,9)
df['admission_source_id'] = df['admission_source_id'].replace(13,11)
df['admission_source_id'] = df['admission_source_id'].replace(14,11)





df['change'] = df['change'].replace('Ch', 1)
df['change'] = df['change'].replace('No', 0)
df['gender'] = df['gender'].replace('Male', 1)
df['gender'] = df['gender'].replace('Female', 0)
df['diabetesMed'] = df['diabetesMed'].replace('Yes', 1)
df['diabetesMed'] = df['diabetesMed'].replace('No', 0)
# keys is the same as before
for col in keys:
    df[col] = df[col].replace('No', 0)
    df[col] = df[col].replace('Steady', 1)
    df[col] = df[col].replace('Up', 1)
    df[col] = df[col].replace('Down', 1)
    
    
    
    
df['A1Cresult'] = df['A1Cresult'].replace('>7', 1)
df['A1Cresult'] = df['A1Cresult'].replace('>8', 1)
df['A1Cresult'] = df['A1Cresult'].replace('Norm', 0)
df['A1Cresult'] = df['A1Cresult'].replace('None', -99)
df['max_glu_serum'] = df['max_glu_serum'].replace('>200', 1)
df['max_glu_serum'] = df['max_glu_serum'].replace('>300', 1)
df['max_glu_serum'] = df['max_glu_serum'].replace('Norm', 0)
df['max_glu_serum'] = df['max_glu_serum'].replace('None', -99)




# code age intervals [0-10) - [90-100) from 1-10
for i in range(0,10):
    df['age'] = df['age'].replace('['+str(10*i)+'-'+str(10*(i+1))+')', i+1)
df['age'].value_counts()




df2 = df.drop_duplicates(subset= ['patient_nbr'], keep = 'first')
df2.shape
(70442, 55)


df.head().T




df['readmitted'].value_counts()



df['readmitted'] = df['readmitted'].replace('>30', 0)
df['readmitted'] = df['readmitted'].replace('<30', 1)
df['readmitted'] = df['readmitted'].replace('NO', 0)



# Creating additional columns for diagnosis# Creati 
df['level1_diag1'] = df['diag_1']
df['level2_diag1'] = df['diag_1']
df['level1_diag2'] = df['diag_2']
df['level2_diag2'] = df['diag_2']
df['level1_diag3'] = df['diag_3']
df['level2_diag3'] = df['diag_3']



df.loc[df['diag_1'].str.contains('V'), ['level1_diag1', 'level2_diag1']] = 0
df.loc[df['diag_1'].str.contains('E'), ['level1_diag1', 'level2_diag1']] = 0
df.loc[df['diag_2'].str.contains('V'), ['level1_diag2', 'level2_diag2']] = 0
df.loc[df['diag_2'].str.contains('E'), ['level1_diag2', 'level2_diag2']] = 0
df.loc[df['diag_3'].str.contains('V'), ['level1_diag3', 'level2_diag3']] = 0
df.loc[df['diag_3'].str.contains('E'), ['level1_diag3', 'level2_diag3']] = 0
df['level1_diag1'] = df['level1_diag1'].replace('?', -1)
df['level2_diag1'] = df['level2_diag1'].replace('?', -1)
df['level1_diag2'] = df['level1_diag2'].replace('?', -1)
df['level2_diag2'] = df['level2_diag2'].replace('?', -1)
df['level1_diag3'] = df['level1_diag3'].replace('?', -1)
df['level2_diag3'] = df['level2_diag3'].replace('?', -1)



df['level1_diag1'] = df['level1_diag1'].astype(float)
df['level2_diag1'] = df['level2_diag1'].astype(float)
df['level1_diag2'] = df['level1_diag2'].astype(float)
df['level2_diag2'] = df['level2_diag2'].astype(float)
df['level1_diag3'] = df['level1_diag3'].astype(float)
df['level2_diag3'] = df['level2_diag3'].astype(float)




for index, row in df.iterrows():
    if (row['level1_diag1'] >= 390 and row['level1_diag1'] < 460) or (np.floor(row['level1_diag1']) == 785):
        df.loc[index, 'level1_diag1'] = 1
    elif (row['level1_diag1'] >= 460 and row['level1_diag1'] < 520) or (np.floor(row['level1_diag1']) == 786):
        df.loc[index, 'level1_diag1'] = 2
    elif (row['level1_diag1'] >= 520 and row['level1_diag1'] < 580) or (np.floor(row['level1_diag1']) == 787):
        df.loc[index, 'level1_diag1'] = 3
    elif (np.floor(row['level1_diag1']) == 250):
        df.loc[index, 'level1_diag1'] = 4
    elif (row['level1_diag1'] >= 800 and row['level1_diag1'] < 1000):
        df.loc[index, 'level1_diag1'] = 5
    elif (row['level1_diag1'] >= 710 and row['level1_diag1'] < 740):
        df.loc[index, 'level1_diag1'] = 6
    elif (row['level1_diag1'] >= 580 and row['level1_diag1'] < 630) or (np.floor(row['level1_diag1']) == 788):
        df.loc[index, 'level1_diag1'] = 7
    elif (row['level1_diag1'] >= 140 and row['level1_diag1'] < 240):
        df.loc[index, 'level1_diag1'] = 8
    else:
        df.loc[index, 'level1_diag1'] = 0
        
    if (row['level1_diag2'] >= 390 and row['level1_diag2'] < 460) or (np.floor(row['level1_diag2']) == 785):
        df.loc[index, 'level1_diag2'] = 1
    elif (row['level1_diag2'] >= 460 and row['level1_diag2'] < 520) or (np.floor(row['level1_diag2']) == 786):
        df.loc[index, 'level1_diag2'] = 2
    elif (row['level1_diag2'] >= 520 and row['level1_diag2'] < 580) or (np.floor(row['level1_diag2']) == 787):
        df.loc[index, 'level1_diag2'] = 3
    elif (np.floor(row['level1_diag2']) == 250):
        df.loc[index, 'level1_diag2'] = 4
    elif (row['level1_diag2'] >= 800 and row['level1_diag2'] < 1000):
        df.loc[index, 'level1_diag2'] = 5
    elif (row['level1_diag2'] >= 710 and row['level1_diag2'] < 740):
        df.loc[index, 'level1_diag2'] = 6
    elif (row['level1_diag2'] >= 580 and row['level1_diag2'] < 630) or (np.floor(row['level1_diag2']) == 788):
        df.loc[index, 'level1_diag2'] = 7
    elif (row['level1_diag2'] >= 140 and row['level1_diag2'] < 240):
        df.loc[index, 'level1_diag2'] = 8
    else:
        df.loc[index, 'level1_diag2'] = 0
        
    if (row['level1_diag3'] >= 390 and row['level1_diag3'] < 460) or (np.floor(row['level1_diag3']) == 785):
        df.loc[index, 'level1_diag3'] = 1
    elif (row['level1_diag3'] >= 460 and row['level1_diag3'] < 520) or (np.floor(row['level1_diag3']) == 786):
        df.loc[index, 'level1_diag3'] = 2
    elif (row['level1_diag3'] >= 520 and row['level1_diag3'] < 580) or (np.floor(row['level1_diag3']) == 787):
        df.loc[index, 'level1_diag3'] = 3
    elif (np.floor(row['level1_diag3']) == 250):
        df.loc[index, 'level1_diag3'] = 4
    elif (row['level1_diag3'] >= 800 and row['level1_diag3'] < 1000):
        df.loc[index, 'level1_diag3'] = 5
    elif (row['level1_diag3'] >= 710 and row['level1_diag3'] < 740):
        df.loc[index, 'level1_diag3'] = 6
    elif (row['level1_diag3'] >= 580 and row['level1_diag3'] < 630) or (np.floor(row['level1_diag3']) == 788):
        df.loc[index, 'level1_diag3'] = 7
    elif (row['level1_diag3'] >= 140 and row['level1_diag3'] < 240):
        df.loc[index, 'level1_diag3'] = 8
    else:
        df.loc[index, 'level1_diag3'] = 0
        
        
        
for index, row in df.iterrows():
    if (row['level2_diag1'] >= 390 and row['level2_diag1'] < 399):
        df.loc[index, 'level2_diag1'] = 1
    elif (row['level2_diag1'] >= 401 and row['level2_diag1'] < 415):
        df.loc[index, 'level2_diag1'] = 2
    elif (row['level2_diag1'] >= 415 and row['level2_diag1'] < 460):
        df.loc[index, 'level2_diag1'] = 3
    elif (np.floor(row['level2_diag1']) == 785):
        df.loc[index, 'level2_diag1'] = 4
    elif (row['level2_diag1'] >= 460 and row['level2_diag1'] < 489):
        df.loc[index, 'level2_diag1'] = 5
    elif (row['level2_diag1'] >= 490 and row['level2_diag1'] < 497):
        df.loc[index, 'level2_diag1'] = 6
    elif (row['level2_diag1'] >= 500 and row['level2_diag1'] < 520):
        df.loc[index, 'level2_diag1'] = 7
    elif (np.floor(row['level2_diag1']) == 786):
        df.loc[index, 'level2_diag1'] = 8
    elif (row['level2_diag1'] >= 520 and row['level2_diag1'] < 530):
        df.loc[index, 'level2_diag1'] = 9
    elif (row['level2_diag1'] >= 530 and row['level2_diag1'] < 544):
        df.loc[index, 'level2_diag1'] = 10
    elif (row['level2_diag1'] >= 550 and row['level2_diag1'] < 554):
        df.loc[index, 'level2_diag1'] = 11
    elif (row['level2_diag1'] >= 555 and row['level2_diag1'] < 580):
        df.loc[index, 'level2_diag1'] = 12
    elif (np.floor(row['level2_diag1']) == 787):
        df.loc[index, 'level2_diag1'] = 13
    elif (np.floor(row['level2_diag1']) == 250):
        df.loc[index, 'level2_diag1'] = 14
    elif (row['level2_diag1'] >= 800 and row['level2_diag1'] < 1000):
        df.loc[index, 'level2_diag1'] = 15
    elif (row['level2_diag1'] >= 710 and row['level2_diag1'] < 740):
        df.loc[index, 'level2_diag1'] = 16
    elif (row['level2_diag1'] >= 580 and row['level2_diag1'] < 630):
        df.loc[index, 'level2_diag1'] = 17
    elif (np.floor(row['level2_diag1']) == 788):
        df.loc[index, 'level2_diag1'] = 18
    elif (row['level2_diag1'] >= 140 and row['level2_diag1'] < 240):
        df.loc[index, 'level2_diag1'] = 19
    elif row['level2_diag1'] >= 240 and row['level2_diag1'] < 280 and (np.floor(row['level2_diag1']) != 250):
        df.loc[index, 'level2_diag1'] = 20
    elif (row['level2_diag1'] >= 680 and row['level2_diag1'] < 710) or (np.floor(row['level2_diag1']) == 782):
        df.loc[index, 'level2_diag1'] = 21
    elif (row['level2_diag1'] >= 290 and row['level2_diag1'] < 320):
        df.loc[index, 'level2_diag1'] = 22
    else:
        df.loc[index, 'level2_diag1'] = 0
        
    if (row['level2_diag2'] >= 390 and row['level2_diag2'] < 399):
        df.loc[index, 'level2_diag2'] = 1
    elif (row['level2_diag2'] >= 401 and row['level2_diag2'] < 415):
        df.loc[index, 'level2_diag2'] = 2
    elif (row['level2_diag2'] >= 415 and row['level2_diag2'] < 460):
        df.loc[index, 'level2_diag2'] = 3
    elif (np.floor(row['level2_diag2']) == 785):
        df.loc[index, 'level2_diag2'] = 4
    elif (row['level2_diag2'] >= 460 and row['level2_diag2'] < 489):
        df.loc[index, 'level2_diag2'] = 5
    elif (row['level2_diag2'] >= 490 and row['level2_diag2'] < 497):
        df.loc[index, 'level2_diag2'] = 6
    elif (row['level2_diag2'] >= 500 and row['level2_diag2'] < 520):
        df.loc[index, 'level2_diag2'] = 7
    elif (np.floor(row['level2_diag2']) == 786):
        df.loc[index, 'level2_diag2'] = 8
    elif (row['level2_diag2'] >= 520 and row['level2_diag2'] < 530):
        df.loc[index, 'level2_diag2'] = 9
    elif (row['level2_diag2'] >= 530 and row['level2_diag2'] < 544):
        df.loc[index, 'level2_diag2'] = 10
    elif (row['level2_diag2'] >= 550 and row['level2_diag2'] < 554):
        df.loc[index, 'level2_diag2'] = 11
    elif (row['level2_diag2'] >= 555 and row['level2_diag2'] < 580):
        df.loc[index, 'level2_diag2'] = 12
    elif (np.floor(row['level2_diag2']) == 787):
        df.loc[index, 'level2_diag2'] = 13
    elif (np.floor(row['level2_diag2']) == 250):
        df.loc[index, 'level2_diag2'] = 14
    elif (row['level2_diag2'] >= 800 and row['level2_diag2'] < 1000):
        df.loc[index, 'level2_diag2'] = 15
    elif (row['level2_diag2'] >= 710 and row['level2_diag2'] < 740):
        df.loc[index, 'level2_diag2'] = 16
    elif (row['level2_diag2'] >= 580 and row['level2_diag2'] < 630):
        df.loc[index, 'level2_diag2'] = 17
    elif (np.floor(row['level2_diag2']) == 788):
        df.loc[index, 'level2_diag2'] = 18
    elif (row['level2_diag2'] >= 140 and row['level2_diag2'] < 240):
        df.loc[index, 'level2_diag2'] = 19
    elif row['level2_diag2'] >= 240 and row['level2_diag2'] < 280 and (np.floor(row['level2_diag2']) != 250):
        df.loc[index, 'level2_diag2'] = 20
    elif (row['level2_diag2'] >= 680 and row['level2_diag2'] < 710) or (np.floor(row['level2_diag2']) == 782):
        df.loc[index, 'level2_diag2'] = 21
    elif (row['level2_diag2'] >= 290 and row['level2_diag2'] < 320):
        df.loc[index, 'level2_diag2'] = 22
    else:
        df.loc[index, 'level2_diag2'] = 0
        
    if (row['level2_diag3'] >= 390 and row['level2_diag3'] < 399):
        df.loc[index, 'level2_diag3'] = 1
    elif (row['level2_diag3'] >= 401 and row['level2_diag3'] < 415):
        df.loc[index, 'level2_diag3'] = 2
    elif (row['level2_diag3'] >= 415 and row['level2_diag3'] < 460):
        df.loc[index, 'level2_diag3'] = 3
    elif (np.floor(row['level2_diag3']) == 785):
        df.loc[index, 'level2_diag3'] = 4
    elif (row['level2_diag3'] >= 460 and row['level2_diag3'] < 489):
        df.loc[index, 'level2_diag3'] = 5
    elif (row['level2_diag3'] >= 490 and row['level2_diag3'] < 497):
        df.loc[index, 'level2_diag3'] = 6
    elif (row['level2_diag3'] >= 500 and row['level2_diag3'] < 520):
        df.loc[index, 'level2_diag3'] = 7
    elif (np.floor(row['level2_diag3']) == 786):
        df.loc[index, 'level2_diag3'] = 8
    elif (row['level2_diag3'] >= 520 and row['level2_diag3'] < 530):
        df.loc[index, 'level2_diag3'] = 9
    elif (row['level2_diag3'] >= 530 and row['level2_diag3'] < 544):
        df.loc[index, 'level2_diag3'] = 10
    elif (row['level2_diag3'] >= 550 and row['level2_diag3'] < 554):
        df.loc[index, 'level2_diag3'] = 11
    elif (row['level2_diag3'] >= 555 and row['level2_diag3'] < 580):
        df.loc[index, 'level2_diag3'] = 12
    elif (np.floor(row['level2_diag3']) == 787):
        df.loc[index, 'level2_diag3'] = 13
    elif (np.floor(row['level2_diag3']) == 250):
        df.loc[index, 'level2_diag3'] = 14
    elif (row['level2_diag3'] >= 800 and row['level2_diag3'] < 1000):
        df.loc[index, 'level2_diag3'] = 15
    elif (row['level2_diag3'] >= 710 and row['level2_diag3'] < 740):
        df.loc[index, 'level2_diag3'] = 16
    elif (row['level2_diag3'] >= 580 and row['level2_diag3'] < 630):
        df.loc[index, 'level2_diag3'] = 17
    elif (np.floor(row['level2_diag3']) == 788):
        df.loc[index, 'level2_diag3'] = 18
    elif (row['level2_diag3'] >= 140 and row['level2_diag3'] < 240):
        df.loc[index, 'level2_diag3'] = 19
    elif row['level2_diag3'] >= 240 and row['level2_diag3'] < 280 and (np.floor(row['level2_diag3']) != 250):
        df.loc[index, 'level2_diag3'] = 20
    elif (row['level2_diag3'] >= 680 and row['level2_diag3'] < 710) or (np.floor(row['level2_diag3']) == 782):
        df.loc[index, 'level2_diag3'] = 21
    elif (row['level2_diag3'] >= 290 and row['level2_diag3'] < 320):
        df.loc[index, 'level2_diag3'] = 22
    else:
        df.loc[index, 'level2_diag3'] = 0
        

        
        
        
import seaborn as sns

#1
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Define the custom color palette
custom_palette = ["#AFA8E2", "#9DDAC6"]

# Create a slider widget to adjust the bar width
bar_width = st.slider('Bar Width', min_value=0.1, max_value=1.0, step=0.1, value=0.8)

# Create the countplot using seaborn with the custom color palette
sns.set_palette(custom_palette)

# Assuming you have a DataFrame named 'df' with a column 'readmitted'
fig, ax = plt.subplots()
sns.countplot(data=df, x='readmitted', ax=ax)

# Set the bar width
for bar in ax.patches:
    bar.set_width(bar_width)

# Set the title of the plot
ax.set_title('Distribution of Readmission')

# Display the plot
st.pyplot(fig)








#2
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Set the style and palette
sns.set_style("darkgrid")
custom_palette = ["#AFA8E2", "#9DDAC6"]
sns.set_palette(custom_palette)

# Create a range slider for filtering the data
time_range = st.slider('Time Range', min_value=0, max_value=14, step=1, value=(0, 14))

# Filter the DataFrame based on the selected time range
filtered_df = df[(df['time_in_hospital'] >= time_range[0]) & (df['time_in_hospital'] <= time_range[1])]

# Create the KDE plot using seaborn
fig = plt.figure(figsize=(13, 7))
ax = sns.kdeplot(filtered_df.loc[df['readmitted'] == 0, 'time_in_hospital'], color=custom_palette[0], shade=True, label='Not Readmitted')
ax = sns.kdeplot(filtered_df.loc[df['readmitted'] == 1, 'time_in_hospital'], color=custom_palette[1], shade=True, label='Readmitted')

# Set labels and title
ax.set(xlabel='Time in Hospital', ylabel='Frequency')
plt.title('Time in Hospital VS. Readmission')

# Display the plot
st.pyplot(fig)












#3
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Set the style and palette
sns.set_style("darkgrid")
custom_palette = ["#AFA8E2", "#9DDAC6"]
sns.set_palette(custom_palette)

# Create a checkbox to show or hide the legend
show_legend = st.checkbox('Show Legend', value=True)

# Create the countplot using seaborn
fig = plt.figure(figsize=(15, 10))
ax = sns.countplot(y=df['age'], hue=df['readmitted'])

# Set title and labels
plt.title('Age of Patient VS. Readmission')
plt.xlabel('Count')
plt.ylabel('Age')

# Show or hide the legend based on the checkbox value
if not show_legend:
    ax.legend_.remove()

# Display the plot
st.pyplot(fig)




# Set the style and palette
sns.set_style("darkgrid")
sns.set_palette(custom_palette)

# Create the countplot using seaborn
fig = plt.figure(figsize=(15, 10))
sns.countplot(y=df['age'], hue=df['readmitted'])

# Set title and labels
plt.title('Age of Patient VS. Readmission')
plt.xlabel('Count')
plt.ylabel('Age')

# Display the plot
plt.show()










#4
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Set the style and palette
sns.set_style("darkgrid")
custom_palette = ["#AFA8E2", "#9DDAC6"]
sns.set_palette(custom_palette)

# Create a selectbox to choose the column for the y-axis
y_axis = st.selectbox('Y-Axis', options=df.columns)

# Create the countplot using seaborn
fig = plt.figure(figsize=(8, 8))
ax = sns.countplot(y=df[y_axis], hue=df['readmitted'])

# Set title and labels
plt.title('Ethnicity of Patient and Readmission')
plt.xlabel('Count')
plt.ylabel(y_axis)

# Display the plot
st.pyplot(fig)


# Set the style and palette
sns.set_style("darkgrid")
sns.set_palette(custom_palette)

# Create the countplot using seaborn
fig = plt.figure(figsize=(8, 8))
sns.countplot(y=df['race'], hue=df['readmitted'])

# Set title and labels
plt.title('Ethnicity of Patient and Readmission')
plt.xlabel('Count')
plt.ylabel('Ethnicity')

# Display the plot in a separate window
plt.show()



import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Set the style and palette
custom_palette = ["#AFA8E2", "#9DDAC6"]
plt.style.use("seaborn-darkgrid")
colors = custom_palette

# Create a selectbox to choose the column for the y-axis
y_axis = st.selectbox('Y-Axis', options=df.columns)

# Group the data by the selected column and count the occurrences
data_counts = df[y_axis].value_counts()

# Extract the labels and counts from the grouped data
labels = data_counts.index
counts = data_counts.values

# Create the countplot using matplotlib and pyplot
fig, ax = plt.subplots(figsize=(8, 8))
y_pos = np.arange(len(labels))
ax.barh(y_pos, counts, color=colors)
ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.set_xlabel('Count')
ax.set_ylabel(y_axis)
plt.title('Ethnicity of Patient and Readmission')

# Display the plot
st.pyplot(fig)



#4
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Set the style and palette
sns.set_style("darkgrid")
custom_palette = ["#AFA8E2", "#9DDAC6"]
sns.set_palette(custom_palette)

# Create a selectbox to choose the column for the y-axis
y_axis = st.selectbox('Y-Axis', options=df.columns)

# Create the countplot using seaborn
fig = plt.figure(figsize=(8, 8))
ax = sns.countplot(y=df[y_axis], hue=df['readmitted'])

# Set title and labels
plt.title('Ethnicity of Patient and Readmission')
plt.xlabel('Count')
plt.ylabel(y_axis)

# Display the plot
st.pyplot(fig)


# Set the style and palette
sns.set_style("darkgrid")
sns.set_palette(custom_palette)

# Create the countplot using seaborn
fig = plt.figure(figsize=(8, 8))
sns.countplot(y=df['race'], hue=df['readmitted'])

# Set title and labels
plt.title('Ethnicity of Patient and Readmission')
plt.xlabel('Count')
plt.ylabel('Ethnicity')

# Display the plot in a separate window
plt.show()


import streamlit as st
import matplotlib.pyplot as plt

# Set the style and palette
custom_palette = ["#AFA8E2", "#9DDAC6"]
plt.style.use("darkgrid")
colors = custom_palette

# Create a selectbox to choose the column for the y-axis
y_axis = st.selectbox('Y-Axis', options=df.columns)

# Create the countplot using matplotlib and pyplot
fig, ax = plt.subplots(figsize=(8, 8))

# Assuming you have a DataFrame named 'df' with columns 'readmitted' and 'y_axis'
y_axis_counts = df[y_axis].value_counts()
labels = y_axis_counts.index
counts = y_axis_counts.values

# Assuming you have a DataFrame named 'df' with a column 'readmitted'
readmitted_counts = df[df['readmitted'] == 1][y_axis].value_counts()
not_readmitted_counts = df[df['readmitted'] == 0][y_axis].value_counts()

bar_width = 0.35
bar_positions1 = range(len(labels))
bar_positions2 = [x + bar_width for x in bar_positions1]

ax.bar(bar_positions1, not_readmitted_counts, color=colors[0], width=bar_width, label='Not Readmitted')
ax.bar(bar_positions2, readmitted_counts, color=colors[1], width=bar_width, label='Readmitted')

ax.set_xticks([x + bar_width/2 for x in bar_positions1])
ax.set_xticklabels(labels, rotation=90)

# Set title and labels
ax.set_title('Ethnicity of Patient and Readmission')
ax.set_xlabel('Count')
ax.set_ylabel(y_axis)
ax.legend()

# Display the plot
st.pyplot(fig)


#5
import streamlit as st
import matplotlib.pyplot as plt

# Set the colors
colors = ["#D4C6F1", "#9DDAC6"]

# Create the countplot using matplotlib and pyplot
fig, ax = plt.subplots(figsize=(8, 8))

# Assuming you have a DataFrame named 'df' with columns 'gender' and 'readmitted'
gender_counts = df['gender'].value_counts()
labels = gender_counts.index

# Assuming you have a DataFrame named 'df' with columns 'gender' and 'readmitted'
readmitted_counts = df[df['readmitted'] == 1]['gender'].value_counts()
not_readmitted_counts = df[df['readmitted'] == 0]['gender'].value_counts()

bar_width = 0.35
bar_positions1 = range(len(labels))
bar_positions2 = [x + bar_width for x in bar_positions1]

ax.bar(bar_positions1, not_readmitted_counts, color=colors[0], width=bar_width, label='Not Readmitted')
ax.bar(bar_positions2, readmitted_counts, color=colors[1], width=bar_width, label='Readmitted')

ax.set_xticks([x + bar_width/2 for x in bar_positions1])
ax.set_xticklabels(labels)

# Set title and labels
ax.set_title('Gender of Patient VS. Readmission')
ax.set_xlabel('Gender')
ax.set_ylabel('Count')
ax.legend()

# Display the plot
st.pyplot(fig)



#6
import streamlit as st
import matplotlib.pyplot as plt

# Set the colors
colors = ["#9DDAC6", "#D4C6F1"]

# Create the barplot using matplotlib and pyplot
fig, ax = plt.subplots(figsize=(8, 8))

# Assuming you have a DataFrame named 'df' with columns 'readmitted' and 'num_medications'
readmitted_data = df[df['readmitted'] == 1]['num_medications']
not_readmitted_data = df[df['readmitted'] == 0]['num_medications']

bar_positions1 = [0]
bar_positions2 = [1]

ax.bar(bar_positions1, not_readmitted_data.mean(), color=colors[0], width=0.5, yerr=not_readmitted_data.std(), label='Not Readmitted')
ax.bar(bar_positions2, readmitted_data.mean(), color=colors[1], width=0.5, yerr=readmitted_data.std(), label='Readmitted')

ax.set_xticks([0, 1])
ax.set_xticklabels(['Not Readmitted', 'Readmitted'])

# Set title and labels
ax.set_title('Number of Medications Used VS. Readmission')
ax.set_xlabel('Readmission')
ax.set_ylabel('Number of Medications')
ax.legend()

# Display the plot
st.pyplot(fig)





