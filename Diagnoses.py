# Clean Text Columns

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re

cardiac=pd.read_csv('CleanData/CardiacM_clean.csv')
archive=pd.read_csv('CleanData/ArchiveClean.csv')
archive.shape
cardiac=cardiac.drop('Unnamed: 0',axis=1)
archive=archive.drop('Unnamed: 0',axis=1)

def lower_errors(x):
    try:
        return x.lower()
    except:
        return ""

def find_unique_diag(df_diag_column):
    """
    Within text Diagnosis Columns, returns a list of the Unique Diagnoses,
    removing the combinations of diagnoses
    """
    all_diag=df_diag_column.apply(lambda x: lower_errors(x)).unique()
    all_diag[7].split(' , ')
    unique_diag=[]
    for diag in all_diag:
        if len(diag)==0:
            continue
        else:
            unique_diag.append(diag.split(' , '))
    flat_list = [item for sublist in unique_diag for item in sublist]
    unique_diag=pd.Series(flat_list).unique()
    return unique_diag

test=find_unique_diag(archive.Diagnosis_1)
df=archive[['patient_link','Diagnosis_1']].sample(10)

def dummify_diagnoses(df,unique_diag,diagnosis_col='Diagnosis_1'):
    """
    Takes Diagnoses and dummifies them for patients. If a patient has multiple
    diagnoses, will put a 1 in all relevant Diagnoses.
    The kth column is NA, no diagnosis. Maybe we will impute with the mode?
    """
    header=unique_diag.tolist().append('patient_link')
    dummy_diag=pd.DataFrame(columns=header)

    for row in range(df.shape[0]):
        pat_diag=lower_errors(df.iloc[row][diagnosis_col]).split(' , ')
        # print(pat_diag)
        dict_dummy_diag=dict(zip(unique_diag,np.zeros(len(unique_diag))))
        # dict_dummy_diag['patient_link']=df.iloc[row]['patient_link']
        #pd.DataFrame(np.zeros(len(unique_diag)).reshape(-1),columns=unique_diag)
        for diag in pat_diag:
            if diag in unique_diag:
                dict_dummy_diag[diag]=1
            else:
                continue
        tmp_dummy_diag=pd.DataFrame(dict_dummy_diag, index=[row])
        tmp_dummy_diag['patient_link']=df.iloc[row]['patient_link']
        dummy_diag = pd.concat([dummy_diag,tmp_dummy_diag], axis=0)

    return dummy_diag

dummify_diagnoses(cardiac,test)
