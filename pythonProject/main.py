import sys
import requests
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy as np

def ExponentinalSmoothing (real_data, alpha):
    forecast = []
    forecast.append(real_data[0])
    for k in range(1, len(real_data)+1):
        forecast.append(alpha * real_data[k - 1] + (1 - alpha) * forecast[k - 1])
    forecast.pop(0)
    return forecast
def movingAverage(data, n):
        return pd.Series(data).rolling(window=n).mean().iloc[n - 1:].values

def loadDatafromBinance():
    TIME_start = 1684454400000
    # 01 MAY 2023 03:00
    TIME_end = 2000000000000
    payload = {}
    headers = {}
    symbol = "BATUSDT"
    url = f'https://api.binance.com/api/v1/klines?symbol={symbol}&interval=1m&startTime={TIME_start}&endTime={TIME_end}&limit=1000'
    print(url)
    response = requests.request("GET", url, headers=headers,data=payload)
    resList=pd.DataFrame.from_records(response.json()).values.tolist()
    for i in range(0, len(resList)):
        for j in range(0, len(resList[i])):
            if j==0:
                resList[i][j]=datetime.fromtimestamp(int(resList[i][j])/1000)
            else:
                resList[i][j] = float(resList[i][j])
    return resList
def RSME(real_data,forecast):
    RSME=0
    for i in range(0,len(real_data)):
        RSME+=(real_data[i]-forecast[i])**2
    RSME/=len(real_data)
    RSME**=1/2
    return RSME
def MAPE(real_data, forecast):
    MAPE=0
    for i in range(0,len(real_data)):
        MAPE+=abs(real_data[i]-forecast[i])/abs(real_data[i])
    MAPE*=100
    MAPE/=len(real_data)
    return MAPE
def TP (real_data,forecast):
    TP=0
    for i in range(1,len(real_data)):
        if (real_data[i]-real_data[i-1])>0 and (forecast[i]-forecast[i-1])>0:
            TP+=1
    return TP
def TN (real_data,forecast):
    TN=0
    for i in range(1,len(real_data)):
        if (real_data[i]-real_data[i-1])<0 and (forecast[i]-forecast[i-1])<0:
            TN+=1
    return TN
def FN (real_data,forecast):
    FN=0
    for i in range(1,len(real_data)):
        if (real_data[i]-real_data[i-1])>0 and (forecast[i]-forecast[i-1])<0:
            FN+=1
    return FN
def FP (real_data,forecast):
    FP=0
    for i in range(1,len(real_data)):
        if (real_data[i]-real_data[i-1])<0 and (forecast[i]-forecast[i-1])>0:
            FP+=1
    return FP
def MISC (real_data,forecast):
    Accuracy=((TP(real_data,forecast)+TN(real_data,forecast))/
              (TP(real_data,forecast)+TN(real_data,forecast)+FN(real_data,forecast)+FP(real_data,forecast)))
    return (1-Accuracy)*100
def StaticalCharacteristics(real_data,forecast):
    print("RSME: ", RSME(real_data,forecast))
    print("MAPE: ", MAPE(real_data,forecast))
    print("TP: ", TP(real_data,forecast))
    print("TN: ", TN(real_data,forecast))
    print("FP: ", FP(real_data,forecast))
    print("FN: ", FN(real_data,forecast))
    print("MISC: ", str(MISC(real_data,forecast))+"%")
def Forecast ():
    data=loadDatafromBinance()
    real_data=[row[1] for row in data[1:]]
    time = [row[0] for row in data[1:]]
    # The Best Alpha
    bestAlpha=0
    bestRSME=sys.float_info.max
    for alpha in np.arange(0, 1, 0.1):
        forecastExp = ExponentinalSmoothing(real_data, alpha)
        newRSME=RSME(real_data[1:],forecastExp[:-1])
        if newRSME<bestRSME:
            bestAlpha=alpha
            bestRSME=newRSME
    # Best MovingAverage
    best_window=0
    bestRSME = sys.float_info.max
    for window in range(5,40):
        forecastMovingAver = movingAverage(real_data, window)
        newRSME = RSME(real_data[window:], forecastMovingAver)
        if newRSME < bestRSME:
            best_window=window
            bestRSME=newRSME
    forecastExp=ExponentinalSmoothing(real_data,bestAlpha)
    forecastMovingAver=movingAverage(real_data,best_window)
    print("Moving Average: ")
    StaticalCharacteristics(real_data[best_window:],forecastMovingAver)
    print("Exponential Smothing: ")
    StaticalCharacteristics(real_data[1:],forecastExp)
    timeExp=time[1:]
    timeExp.append(datetime.fromtimestamp(datetime.timestamp(time[-1])
                   +datetime.timestamp(time[-1])
                   -datetime.timestamp(time[-2])))
    timeAver=time[best_window:]
    timeAver.append(datetime.fromtimestamp(datetime.timestamp(time[-1])
                   +datetime.timestamp(time[-1])
                   -datetime.timestamp(time[-2])))
    plt.plot(time, real_data, label='Real Data', color = 'grey')
    plt.title("")
    plt.plot( timeExp, forecastExp,label='Exponential smoothing', color = 'yellow')
    plt.plot(timeAver,forecastMovingAver,label='Moving Average', color = 'violet')
    plt.legend(loc='upper right')
    plt.xlabel("Time")
    plt.ylabel("Cost")
    plt.xticks(np.arange(min(time),max(time),timedelta(hours=3)))
    formatter = DateFormatter('%H:%M:%S')
    plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
    plt.show()
Forecast()