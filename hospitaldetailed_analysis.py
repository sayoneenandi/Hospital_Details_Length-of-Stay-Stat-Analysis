# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 12:48:02 2022

@author: Sayonee
"""

import pandas as pd
import datetime as dt
import numpy as np
from datetime import datetime
import matplotlib.pyplot as mt
from matplotlib import figure
import seaborn as sns
import math
from sklearn import linear_model

'''read the data as dataframe 
'''
hospital_Details=pd.read_csv("hospital_details.csv")
#print(hospital_Details)
hospital_Details = pd.DataFrame(data = hospital_Details)
print("###############")
print(hospital_Details['SERVICE'].nunique())
#print (hospital_Details) #print(hotel data)
icd=pd.read_csv("ICD Codes.csv")
#print(icd)
icd = pd.DataFrame(data = icd)
#print (icd) #print(hotel data)
'''
rename icd columns
'''
print(icd.columns)
icd.columns = ['Prefix', 'Suffix', 'Old Values','Cause of illness by abbreviation', 'Cause of Illness','Type of Illness' ]
#print(icd.columns)
'''concat icd columns
'''
icd["ICDCODE"] = icd['Prefix'] +"."+ icd["Suffix"]
#print(icd)
'''
drop prefix, suffix and old values 
'''
icd=icd.drop(['Suffix', 'Old Values','Cause of illness by abbreviation'], axis=1)
print(icd)

'''
group the icd codes by type
'''

'''
combine dataframes
'''

#hospital_Details = pd.concat([hospital_Details, icd], axis=1)# merging the two data frames 
#hospital_Details=hospital_Details.join(icd, lsuffix="ICD",rsuffix="ICD CODE",how="left")
hospital_Details=pd.merge(left=hospital_Details, right=icd, left_on="ICD",right_on="ICDCODE",how="left")
#hospital_Details.to_csv("D:\hospital_Details.csv")

'''
clean data by icd, admisson and discharge'''
hospital_Details=hospital_Details.dropna(subset=["DISCHARGE.DATE"])
#hospital_Details=hospital_Details.dropna(subset=["ICDCODE"])
#print(hospital_Details)
#print("5555")
print(hospital_Details['SERVICE'].nunique())
'''
subtract and calculate duration
'''
hospital_Details["ADMISSION.DATE"]=pd.to_datetime(hospital_Details["ADMISSION.DATE"])
hospital_Details["DISCHARGE.DATE"]=pd.to_datetime(hospital_Details["DISCHARGE.DATE"])
hospital_Details["Duration"]=''
#hospital_Details["Duration"]=pd.to_datetime(hospital_Details["Duration"])
hospital_Details["Duration"]=(hospital_Details["DISCHARGE.DATE"]-hospital_Details["ADMISSION.DATE"])
'''
csv files do not take into consideration format
'''
'''
median by service group
'''
hospital_Details['Duration'] = hospital_Details['Duration'].dt.days
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print(hospital_Details['SERVICE'].nunique())
hospital_Details.groupby(by="SERVICE")
print("hhhhhh")
print(hospital_Details)
#hospital_Details.to_csv("D:\hospital_Details1.csv")
#item_counts = hospital_Details["SERVICE"].value_counts()
#print(item_counts)

'''
group data by service and find central tendency age duration groupby doctor and count'''
Service_grp_duration=hospital_Details.groupby(['SERVICE'])['Duration']
mean=Service_grp_duration.mean()
#age_var=hospital_Details.groupby(['SERVICE'])['AGE'].std()
age_mean=hospital_Details.groupby(['SERVICE'])['AGE'].mean()
#newDF=pd.concat([mean, age_var], axis=1).reset_index()
#sex_group=hospital_Details.groupby(['SERVICE'])['SEX']
doctor_count=hospital_Details.groupby(['SERVICE'])['DOCTOR'].count()
patient_inSer=hospital_Details.groupby(['SERVICE'])["PROTOCOL.NUMBER"].count()
Type_inSer=hospital_Details.groupby(['SERVICE'])["Prefix"].count()

newDF=pd.concat([mean,age_mean,doctor_count,patient_inSer,Type_inSer], axis=1).reset_index()

figure.Figure( figsize =(2000,1500) )
ax=sns.barplot(data=hospital_Details.round(), x="SERVICE", y="Duration", hue='SEX',errwidth=0)
mt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
mt.tight_layout()
mt.show()

'''linear regression for multi variate data
X = newDF[['AGE', 'DOCTOR']]
y = newDF['Duration']
regr = linear_model.LinearRegression()
regr.fit(X, y) '''
'''
mt.plot(X, y, 'o')
m, b = np.polyfit(X, y, 1)
#mt.plot(X, m*X+b, color='red')
'''
#print(regr.coef_) 
# Plot sepal width as a function of sepal_length across days
g = sns.lmplot( data=newDF.round(),x="AGE", y="Duration", hue="SERVICE",height=5)
# Use more informative axis labels than are provided by default
g.set_axis_labels("AGE", "Duration")
doc = sns.lmplot( data=newDF.round(),x="DOCTOR", y="Duration", hue="SERVICE",height=5)
# Use more informative axis labels than are provided by default
doc.set_axis_labels("DOCTOR", "Duration")
fig, ax = mt.subplots()
sns.regplot(x='Duration', y='DOCTOR', data=newDF.round(), ax=ax)
ax2 = ax.twinx()
sns.regplot(x='Duration', y='AGE', data=newDF.round(), ax=ax2, color='r')
mt.show()

# Use more informative axis labels than are provided by default



'''
plot with comorbidity'''
figure.Figure( figsize =(2000,1500) )
ax=sns.barplot(data=hospital_Details.round(), x="SERVICE", y="Duration", hue='COMORBIDITIES',errwidth=0)
mt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
mt.tight_layout()
mt.show()


typ = sns.lmplot( data=newDF.round(),x="Prefix", y="Duration", hue="SERVICE",height=5)
typ.set_axis_labels("Prefix", "Duration")

##################################################################################################################################