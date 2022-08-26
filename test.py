import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('D:/Hackathons/Delta/water/water.csv',encoding= 'unicode_escape')
df
state = "UTTAR PRADESH"
city = "FIROZABAD"
df2 = df[df['State Name'] == state]
df2 = df2[df2['District Name'] == city]
print(df2)
print(df2["Quality Parameter"].value_counts().idxmax())
#df3 = df2["Quality Parameter"].value_counts().idmax()
#df3.columns = ['Quality Parameter','Count']
#print(df3)
#df3.idmax()