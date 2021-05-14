import time
import pyupbit
import datetime

access = "wDNJP9jHj8xWx3Oj7cL0TRJVqrtP8zdoKlaBi02a"
secret = "gDNjgJx4oB2cH099lrnNitJqSXxIKgmB8tEUa6bJ"


def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + \
        (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")


def buy(ticker, k):
    target_price = get_target_price(ticker, k)
    ma15 = get_ma15(ticker)
    current_price = get_current_price(ticker)
    # print(ticker)
    # print(target_price)
    # print(ma15)
    # print(current_price)
    if target_price < current_price and ma15 < current_price:
        krw = get_balance("KRW")
        if krw > 10000:
            upbit.buy_market_order(ticker, 60000)


# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-ETC")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            buy("KRW-ETC", 0.3)
            buy("KRW-EOS", 0.2)
            buy("KRW-QTUM", 0.2)

        else:
            etc = get_balance("ETC")
            if etc > 0.1:
                upbit.sell_market_order("KRW-ETC", etc*0.9995)

            eos = get_balance("EOS")
            if eos > 0.5:
                upbit.sell_market_order("KRW-EOS", eos*0.9995)

            gtum = get_balance("QTUM")
            if gtum > 0.2:
                upbit.sell_market_order("KRW-QTUM", gtum*0.9995)

        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
