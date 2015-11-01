__author__ = 'yanliu'

import Quandl
import csv
import numpy as np
import pandas as pd
import numpy.linalg as npl

#This program downloads data from Quandl--Yahoo
QUANDL_KEY = "R9YJNzLp6f8cwCb6hhQ3"


if __name__ == "__main__":

    tickers = [] #array container for tickers
    stock_tickers=[] #arrary container for download data from quandl

    with open('symbols.csv') as csvfile: #read the csv file
        readCSV = csv.reader(csvfile, delimiter=',')

        for row in readCSV:
            ticker = row[0]
            stock_ticker = "YAHOO/"+ticker
            tickers.append(ticker) #stock the data in the CSV file in a array
            stock_tickers.append(stock_ticker)

    data = Quandl.get(stock_tickers, authtoken="R9YJNzLp6f8cwCb6hhQ3", trim_start="2014-08-09", trim_end="2015-08-09")
    #download data from Quandl, then store it into dataframe
    my_df = pd.DataFrame(data)

    prices = my_df.iloc[:,::6].as_matrix() #only take every 6th columns of the dataframe and convert it into matrix

    i = prices.shape[0]
    j = prices.shape[1] #obtain number of rows and number of columns

    s_return = np.zeros((i-1, j))
    average_return = np.zeros((i-1, j))
    for ii in xrange(i-1):
        for jj in xrange(j):
            s_return[ii][jj] = (prices[ii+1][jj]-prices[ii][jj]) / prices[ii][jj]
    #calculate the relative return

   # print s_return

    average = np.mean(s_return, axis=0)

    for jj in xrange(j):
        for ii in xrange(i-1):
            average_return[ii][jj] = s_return[ii][jj] - average[jj] #calculate the average return

  #  print average_return

    s_cov = (1.0/(i - 1.0)) * np.dot(average_return.transpose(), average_return)    #calculate it's covariance

  #  print s_cov

    s_inv = npl.inv(s_cov)  #calculae it's inverse

   # print s_inv

    one = np.ones((len(tickers), 1)) #declare the matrix with ones
    t_one = one.transpose()

    A_temp = np.dot(t_one, s_inv)
    A = np.dot(A_temp, one)    #calculate A

    w = np.dot(s_inv , one) / A

    results = [["O" for ii in range(2)]for jj in range(j)]

    for jj in xrange(j): #combine the tickers column and the weightes column
        results[jj][0] = tickers[jj]
        results[jj][1] = str(w[jj]*100).strip('[]')+"%"

    print results
    col = ["Ticker", "weight in percent"]
    final_result = pd.DataFrame(results, columns = col)#convert to dataframe and outFile

    final_result.to_csv("minvarport.csv")
    print "Also check the result in the file calls minvarport.csv"


