import datetime
import pyupbit
import numpy as np

# OHLCV(open, high, low, close, volume)
df = pyupbit.get_ohlcv("krw-ETC", count=7)
df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1)

df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'],
                     1)

df['hpr'] = df['ror'].cumprod()
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD(%): ", df['dd'].max())
df.to_excel("dd.xlsx")

now = datetime.datetime.now()


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


start_time = get_start_time("KRW-ETC")
end_time = start_time + datetime.timedelta(days=1)

print(start_time < now)
print(now < end_time - datetime.timedelta(seconds=10))
