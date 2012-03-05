import datetime
import pytz
import zipline.util as qutil
import zipline.finance.risk as risk
import zipline.protocol as zp


def create_trade(sid, price, amount, datetime):
    row = {
        'source_id' : "test_factory",
        'type'      : zp.DATASOURCE_TYPE.TRADE,
        'sid'       : sid,
        'dt'        : datetime,
        'price'     : price,
        'volume'    : amount
    }
    return row

def create_trade_history(sid, prices, amounts, start_time, interval):
    i = 0
    trades = []
    current = start_time.replace(tzinfo = pytz.utc)

    for price, amount in zip(prices, amounts):

        if(risk.trading_calendar.is_trading_day(current)):
            trade = create_trade(sid, price, amount, current)
            trades.append(trade)

            current = current + interval
        else:
            current = current + datetime.timedelta(days=1)

    return trades

def createTxn(sid, price, amount, datetime, btrid=None):
    txn = Transaction(sid=sid, amount=amount, dt = datetime,
                      price=price, transaction_cost=-1*price*amount)
    return txn

def createTxnHistory(sid, priceList, amtList, startTime, interval):
    txns = []
    current = startTime

    for price, amount in zip(priceList, amtList):

        if risk.trading_calendar.is_trading_day(current):
            txns.append(createTxn(sid, price, amount, current))
            current = current + interval

        else:
            current = current + datetime.timedelta(days=1)

    return txns