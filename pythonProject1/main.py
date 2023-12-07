import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def cm_to_inch(value):
    return value/2.54

df = pd.read_csv("C:/Users/karin/Downloads/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv")
df['Data_Value'] = df['Data_Value'] * 0.1
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month_Day'] = df['Date'].dt.strftime('%m-%d')
df = df[df['Month_Day'] != '02-29']
maximumdata = df[(df['Year'] >= 2005) & (df['Year'] < 2015) & (df['Element'] == 'TMAX')].groupby('Month_Day')['Data_Value'].max()
minimundata = df[(df['Year'] >= 2005) & (df['Year'] < 2015) & (df['Element'] == 'TMIN')].groupby('Month_Day')['Data_Value'].min()
maxof2015 = df[(df['Year'] == 2015) & (df['Data_Value'] > df['Max_temp'])]
minof2015 = df[(df['Year'] == 2015) & (df['Data_Value'] < df['Min_temp'])]
df = df.merge(maximumdata.reset_index(drop=False).rename(columns={'Data_Value': 'Max_temp'}), on='Month_Day', how='left')
df = df.merge(minimundata.reset_index(drop=False).rename(columns={'Data_Value': 'Min_temp'}), on='Month_Day', how='left')
plt.figure(figsize=(cm_to_inch(25), cm_to_inch(15)))
date_index = np.arange('2015-01-01','2016-01-01', dtype='datetime64[D]')
months = ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
plt.plot(date_index, maximumdata, c='red', linewidth=0.8)
plt.plot(date_index, minimundata, c='blue', linewidth=0.8)
plt.scatter(maxof2015['Date'].values, maxof2015['Data_Value'].values, s=4, color='red')
plt.scatter(minof2015['Date'].values, minof2015['Data_Value'].values, s=4, color='blue')
plt.fill_between(date_index,
                 maximumdata,
                 minimundata,
                 facecolor='violet',
                 alpha=0.15)
plt.title('Temperature records 2005 - 2014, Michigan(USA)')
plt.ylabel('Temperature (°C)')
plt.xlabel('Month')
plt.legend(['Record high','Record low','Record breaking high in 2015','Record breaking low in 2015'],frameon=False)
plt.show()