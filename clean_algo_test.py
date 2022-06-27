import yfinance as yf
import pandas as pd
import statistics
import time
import datetime
import os
from cfonts import render, say

cool_header = render('stonkBot', colors=['green', 'red'])


mult12= 2/(12+1)
mult26= 2/(26+1)
mult9= 2/(9+1)

shortEMAList = [0,0,0,0,0,0,0,0,0,0,0]
longEMAList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
MACDList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
signalList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
precentage_list = []

buyPrice = 0.00
sellPrice = 0.00
account = 100
total_profit = 0.00
profit = 0.00
account_growth = 0.00


Data = yf.download(tickers = "BTC-USD",interval = "30m", period= "1mo")
closeData = Data['Close']


shortMean = closeData[0:12].mean()
shortEMAList.append(shortMean)

longMean = closeData[0:26].mean()
longEMAList.append(longMean)


closeData = closeData.to_list()
del Data

def populateEMAs(data, position, mean, mult, list):
    for i in data[position:]:
        mean = (i - mean) * mult + mean
        list.append(mean)

populateEMAs(closeData, 12, shortMean, mult12,shortEMAList)
populateEMAs(closeData, 26, longMean, mult26, longEMAList)

counter = 25
for i in closeData[25:]:
    MACD = shortEMAList[counter] - longEMAList[counter]
    MACDList.append(MACD)
    counter = counter + 1
signalMean = statistics.mean(MACDList[25:34])
signalList.append(signalMean)

populateEMAs(MACDList, 34,signalMean, mult9, signalList)


def getCurrentData():
    global mult12
    global mult26
    global mult9
    global shortEMAList
    global longEMAList
    global  MACDList
    global signalList
    global cool_header

    print(cool_header)
    print(f'\n\nTotal profit: ${total_profit:.2f}')
    print(f'Account Growth: %{account_growth:.2f}')

    time.sleep(10)
    newData = yf.download(tickers = "BTC-USD", interval = "30m", period= "5h")
    updatedClose = newData['Close'].tail(1).item()

    del newData

    closeData.append(updatedClose)
    shortEMAList.append(((updatedClose - shortEMAList[-1])*mult12)+ shortEMAList[-1])
    longEMAList.append(((updatedClose - longEMAList[-1])*mult26)+ longEMAList[-1])
    MACDList.append(shortEMAList[-1] - longEMAList[-1])
    signalList.append(((MACDList[-1] - signalList[-1])*mult9)+ signalList[-1])
    print(f'Total profit: {total_profit:.2f}')
    print(f'Account Growth: {account_growth:.2f}')

    


def startTest():
    os.system('clear')
    if(MACDList[-1] > signalList[-1]):
        print("Trying startTest again")
        getCurrentData()
        startTest()
    else:
        print("startTest Complete! Goint go buyTest")
        getCurrentData()
        buyTest()

def buyTest():
    os.system('clear')
    global account
    global buyPrice
    global shares_bought
    if(MACDList[-1] > signalList[-1]):
        buyPrice = closeData[-1]
        shares_bought = account / buyPrice



        sellTest()
    else:
        getCurrentData()
        buyTest()

def sellTest():
    os.system('clear')
    global profit
    global total_profit
    global account_growth
    global account
    

    if(MACDList[-1] < signalList[-1]):
        sellPrice = closeData[-1]

        profit = (shares_bought * sellPrice) - account

        account = sellPrice * shares_bought
        total_profit += profit
        account_growth = (account-100)/100

        date_time()
        log()
        buyTest()
    else:
        print("Waiting to sell...")
        getCurrentData()
        sellTest()

def date_time():
    global date_now
    global time_now
    now = datetime.datetime.now()
    date_now = now.strftime("%m-%d-%Y")
    time_now = now.strftime("%H:%M")

def log():
    with open('results.txt', 'a') as fp:
        fp.write(f"Sold stonk on {date_now} at {time_now}.\n")
        if profit > 0:
            fp.write(f"Made a profit of {profit}. Stonks!\n")
        else:
            fp.write(f"took a loss of {profit} :(\n\n")

        fp.write(f"Total profit: ${total_profit}")
        fp.write(f"Account growth: %{account_growth:.2f}")
        fp.write("\n***************************************\n\n")


date_time()
file = open('results.txt', 'w')
file.write(f"Starting Log on {date_now}, at {time_now}\n")
file.close()
time.sleep(1)
startTest()