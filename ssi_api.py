import http
import json
import requests
from datetime import datetime
import pandas as pd
from test_Req_Res import md_get_intraday_OHLC
from SSI_Trade import SSITrade
from ssi_fctrading import FCTradingClient
from ssi_fctrading.models import fcmodel_requests
import httpx
from ssi_fc_data import fc_md_client, model
import config
from examples import fc_config
import logging

# Cấu hình ghi nhật ký
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = FCTradingClient(fc_config.Url, fc_config.ConsumerID, fc_config.ConsumerSecret, fc_config.PrivateKey, fc_config.TwoFAType)
print('Read token: ' + client.get_access_token())
client = fc_md_client.MarketDataClient(config)

def md_access_token():
    print(client.access_token(model.accessToken(config.consumerID, config.consumerSecret)))

async def get_access_token():
    return fc_config.PrivateKey

class SsiAPI:
    def __init__(self):
        self.session = requests.Session()   

    def make_request(self, url, params=None):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.status_code, response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
        return None, None

    def fetch_candles(self, symbol: str, from_date: str, to_date: str, page_index: int = 1, page_size: int = 100, option: bool = True, interval: int = 1) -> pd.DataFrame:
        try:
            response = client.intraday_ohlc(config, model.intraday_ohlc(symbol, from_date, to_date, page_index, page_size, option, interval))
            intraday_OHLC_data = response['data']
            if not intraday_OHLC_data:
                logger.debug(f"No data returned for fetch_candles with symbol: {symbol}")
                return pd.DataFrame()
            
            intraday_OHLC_df = pd.DataFrame(intraday_OHLC_data, columns=['Symbol', 'Value', 'TradingDate', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            intraday_OHLC_df['TradingDate'] = pd.to_datetime(intraday_OHLC_df['TradingDate'], format='%d/%m/%Y')
            logger.debug(f"Fetched candles for {symbol}:\n{intraday_OHLC_df.tail()}")
            return intraday_OHLC_df 
        except Exception as e:
            logger.error(f"Error in fetch_candles: {e}")
            return pd.DataFrame()
    


    from datetime import datetime

    def last_complete_candle(self, pair_name):
        # Lấy dữ liệu OHLC intraday
        intraday_OHLC_df = md_get_intraday_OHLC(pair_name, datetime.now().strftime('%d/%m/%Y'), datetime.now().strftime('%d/%m/%Y'), 1, 1000)
        
        if intraday_OHLC_df is not None and not intraday_OHLC_df.empty:
            # Lấy thời gian của nến cuối cùng
            last_candle_time = intraday_OHLC_df.iloc[-1]['Time']
            
            # Kiểm tra kiểu dữ liệu của last_candle_time
            if isinstance(last_candle_time, str):
                try:
                    # Chuyển đổi thời gian từ chuỗi
                    last_candle_datetime = datetime.strptime(last_candle_time, '%H:%M:%S').time()
                except ValueError:
                    # Xử lý lỗi nếu định dạng không đúng
                    print(f"Invalid time format: {last_candle_time}")
                    last_candle_datetime = None
            else:
                # Xử lý trường hợp last_candle_time không phải là chuỗi
                print(f"Expected string but got: {type(last_candle_time)}")
                last_candle_datetime = None
            
            return last_candle_datetime
        
        return None


    async def close_trade(orderID, instrumentID, marketID, buySell, account, deviceId=None, userAgent=None):
        if deviceId is None:
            deviceId = FCTradingClient.get_deviceid()
        if userAgent is None:
            userAgent = FCTradingClient.get_user_agent()

        url = "https://fc-tradeapi.ssi.com.vn/api/v2/Trading/CancelOrder"
        data = {
            "orderID": orderID,
            "instrumentID": instrumentID,
            "marketID": marketID,
            "buySell": buySell,
            "account": account,
            "deviceId": deviceId,
            "userAgent": userAgent
        }

        access_token = await get_access_token()

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()  # Check for HTTP errors
        print(data)
        return response.json()  # Return the response JSON data

    async def open_trades(self, account='7064691', version=2):
        url = f"http://127.0.0.1:8000/orderBook"
        params = {'account': account}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            
            logger.debug(f"Response status code: {response.status_code}")

            if response.status_code != 200:
                logger.error("Failed to fetch order book")
                return [], False
            
            data = response.json()

            logger.debug(f"Response data: {data}")

            if 'data' not in data or 'orders' not in data['data']:
                logger.error("No orders found in response data")
                return [], True
            
            orders = [SSITrade.TradeFromAPI(x) for x in data['data']['orders']]
            logger.debug(f"Orders: {orders}")
            
            return orders, True

    @staticmethod
    def candles_to_df(candles):
        df = pd.DataFrame(candles)
        if not df.empty:
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.set_index('time', inplace=True)
            return df
        return None

    async def place_order(instrumentID, market, buySell, orderType, price, quantity, account, stopOrder=False,
                      stopPrice=0, stopType='', stopStep=0, lossStep=0, profitStep=0,
                      deviceId=None, userAgent=None):
        if deviceId is None:
            deviceId = FCTradingClient.get_deviceid()
        if userAgent is None:
            userAgent = FCTradingClient.get_user_agent()

        url = "https://fc-tradeapi.ssi.com.vn/api/v2/Trading/NewOrder"
        data = {
            "instrumentID": instrumentID,
            "market": market,
            "buySell": buySell,
            "orderType": orderType,
            "price": price,
            "quantity": quantity,
            "account": account,
            "stopOrder": stopOrder,
            "stopPrice": stopPrice,
            "stopType": stopType,
            "stopStep": stopStep,
            "lossStep": lossStep,
            "profitStep": profitStep,
            "deviceId": deviceId,
            "userAgent": userAgent
        }

        access_token = await get_access_token()

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data, headers=headers)
            response.raise_for_status()  # Check for HTTP errors
        logger.debug(data)
        return response  # Return the entire response object

# Mã chính để chạy và kiểm tra các chức năng trên
import asyncio

async def main():
    instance = SsiAPI()
    
    orders, success = await instance.open_trades()
    if success:
        logger.debug("Orders retrieved successfully:")
        for order in orders:
            logger.debug(order)
    else:
        logger.error("Failed to retrieve orders")

asyncio.run(main())
