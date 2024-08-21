import datetime
from dateutil.parser import parse

class SSITrade:
    def __init__(self, ssi_trade_info):
        self.uniqueID = int(ssi_trade_info['uniqueID'])
        self.orderID = int(ssi_trade_info['orderID'])
        self.buySell = ssi_trade_info['buySell']
        self.price = float(ssi_trade_info['price'])
        self.quantity = int(ssi_trade_info['quantity'])
        self.filledQty = int(ssi_trade_info['filledQty'])
        self.orderStatus = ssi_trade_info['orderStatus']
        self.marketID = ssi_trade_info['marketID']
        # self.inputTime = datetime.fromtimestamp(int(ssi_trade_info['inputTime']) / 1000)
        # self.modifiedTime = datetime.fromtimestamp(int(ssi_trade_info['modifiedTime']) / 1000)
        self.instrumentID = ssi_trade_info['instrumentID']
        self.orderType = ssi_trade_info['orderType']
        self.cancelQty = int(ssi_trade_info['cancelQty'])
        self.avgPrice = float(ssi_trade_info['avgPrice'])
        self.isForcesell = ssi_trade_info['isForcesell']
        self.isShortsell = ssi_trade_info['isShortsell']
        self.rejectReason = ssi_trade_info['rejectReason']

    def __repr__(self):
        return str(vars(self))

    @classmethod
    def TradeFromAPI(cls, api_object):
        return SSITrade(api_object)