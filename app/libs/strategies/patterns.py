import datetime
import pandas as pd
import numpy as np
import yfinance as yf
from pprint import pprint
import matplotlib.pyplot as plt


class PatternRecognizing(object):
    def __init__(self, data):
        datas = self.PPSR(data)
        pprint(datas)
        # print(datas.keys())

        plt.plot(data['Close'].values, color='black', label='Price')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend()
        # plt.show()
        datetime.timedelta(weeks=+1)

    def PPSR(self, data):
        # data = datas.resample('1M').mean()
        PP = pd.Series((data['High'] + data['Low'] + data['Close']) / 3)
        R1 = pd.Series(2 * PP - data['Low'])
        S1 = pd.Series(2 * PP - data['High'])
        R2 = pd.Series(PP + data['High'] - data['Low'])
        S2 = pd.Series(PP - data['High'] + data['Low'])
        R3 = pd.Series(data['High'] + 2 * (PP - data['Low']))
        S3 = pd.Series(data['Low'] - 2 * (data['High'] - PP))
        psr = {'PP': PP, 'R1': R1, 'S1': S1, 'R2': R2, 'S2': S2, 'R3': R3, 'S3': S3}
        PSR = pd.DataFrame(psr)

        # PSR = PSR.index + datetime.timedelta(days=30)
        df = pd.concat([data, PSR], axis=1)

        # for column, i in df.items():
        #     value = 0
        #     for index, i in enumerate(df[column]):
        #         if str(i) == "nan":
        #             df[column][index] = value
        #         else:
        #             value = i
        #
        # days = list()
        # start_date = df.index[-1]
        # end_day = start_date + datetime.timedelta(days=30)
        # test = {'PP': [], 'R1': [], 'S1': [], 'R2': [], 'S2': [], 'R3': [] ,'S3': []}
        # for n in range(int((end_day - start_date).days)):
        #     day = start_date + datetime.timedelta(n + 1)
        #     test['PP'].append(df['PP'].iloc[-1])
        #     test['R1'].append(df['R1'].iloc[-1])
        #     test['S1'].append(df['S1'].iloc[-1])
        #     test['R2'].append(df['R2'].iloc[-1])
        #     test['S2'].append(df['S2'].iloc[-1])
        #     test['R3'].append(df['R3'].iloc[-1])
        #     test['S3'].append(df['S3'].iloc[-1])
        #     days.append(day)
        #
        # last_df = pd.DataFrame(test)
        # last_df.index = pd.DatetimeIndex(days)
        #
        # df = df.append(last_df)

        return df


    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            return start_date + datetime.timedelta(n)

    def _PPSR(self, datas):
        data = datas.resample('1M').mean()
        PP = pd.Series((data['High'] + data['Low'] + data['Close']) / 3)
        R1 = pd.Series(2 * PP - data['Low'])
        S1 = pd.Series(2 * PP - data['High'])
        R2 = pd.Series(PP + data['High'] - data['Low'])
        S2 = pd.Series(PP - data['High'] + data['Low'])
        R3 = pd.Series(data['High'] + 2 * (PP - data['Low']))
        S3 = pd.Series(data['Low'] - 2 * (data['High'] - PP))
        psr = {'PP': PP, 'R1': R1, 'S1': S1, 'R2': R2, 'S2': S2, 'R3': R3, 'S3': S3}
        PSR = pd.DataFrame(psr)
        data = data.join(PSR)

        df = pd.concat([datas, data], axis=1)
        pprint(df.keys())

        all_pivots = dict()
        for column, i in df.items():
            if column in ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']:
                continue
            value = 0
            test = list()
            for inde, i in enumerate(df[column]):
                if str(i) != "nan":
                    value = i
                test.append(value)
            all_pivots[column] = test

        dat = pd.DataFrame(all_pivots)
        dat.set_index(datas.index)

        return dat


if __name__ == '__main__':
    tick = "GLE.PA"
    ticker = yf.Ticker(tick)
    data = ticker.history(period="1y", interval="1mo", start="2008-01-01")
    pre = PatternRecognizing(data=data)
