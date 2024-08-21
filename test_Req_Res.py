# import ssi_fc_trading
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ssi_fc_data import fc_md_client , model
import config
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

client = fc_md_client.MarketDataClient(config)
def md_access_token():
	print(client.access_token(model.accessToken(config.consumerID, config.consumerSecret)))
     
def md_get_securities_list():
    req = model.securities('HOSE', 1, 1000)
    securities = client.securities(config, req)
    securities_data = securities['data']
    securities_df = pd.DataFrame(securities_data, columns=['Market', 'Symbol', 'StockName', 'StockEnName'])
    securities_df['StockName'] = securities_df['StockName'].str.lower().str.strip().str.title()
    print("Total records:", len(securities_df))
    print(securities_df)

def md_get_securities_details_OHLC():
    req = model.securities_details('HOSE', 'ACB', 1, 100)
    response = client.securities_details(config, req)
    securities_details_OHLC_data = response.get('data', [])
    
    if securities_details_OHLC_data:
        securities_details_OHLC_df = pd.DataFrame(securities_details_OHLC_data[0].get('RepeatedInfo', []))
    
        if not securities_details_OHLC_df.empty:
            securities_details_OHLC_df = securities_details_OHLC_df.transpose()
            securities_details_OHLC_df.columns = securities_details_OHLC_df.iloc[0]
            securities_details_OHLC_df = securities_details_OHLC_df[1:]
            print("Total records:", len(securities_details_OHLC_df))
            print(securities_details_OHLC_df)
            return securities_details_OHLC_df
        else:
            print("No data available.")
    else:
        print("No data available.")

def md_get_index_components():
	return(client.index_components(config, model.index_components('vn100', 1, 100)))

def md_get_index_list():
	return client.index_list(config, model.index_list('hnx', 1, 100))
import datetime

def md_get_intraday_OHLC1():
    # Lấy ngày hôm nay
    today = datetime.datetime.now().strftime("%d/%m/%Y")
    
    # Lấy dữ liệu intraday OHLC cho ngày hôm nay
    daily = client.intraday_ohlc(config, model.intraday_ohlc('VND', '11/06/2024', '11/06/2024', 1, 1000, True, 1))
    
    # Tạo DataFrame từ dữ liệu và lưu vào tệp JSON
    data = pd.DataFrame(daily)
    data.to_json('./static/data5.json')
    return data
    # In dữ liệu
    print(data)


# def md_get_intraday_OHLC1():
#     daily= client.intraday_ohlc(config, model.intraday_ohlc('SSI', '02/05/2024', '04/05/2024', 1, 100, True, 1))
#     data = pd.DataFrame(daily)
#     data.to_json('data8.json')
#     print (data)
def md_get_daily_OHLC():
    response = client.daily_ohlc(config, model.daily_ohlc('SSI', '01/05/2024', '03/06/2024', 1, 100, True))
    daily_OHLC_data = response['data']
    daily_OHLC_df = pd.DataFrame(daily_OHLC_data, columns=['Symbol', 'Market', 'TradingDate', 'Open', 'High', 'Low', 'Close', 'Volume', 'Value'])
    daily_OHLC_df['TradingDate'] = pd.to_datetime(daily_OHLC_df['TradingDate'], format='%d/%m/%Y')
    daily_OHLC_df.to_json('./static/data5.json')

    return daily_OHLC_df

def md_get_daily_OHLC1():
    daily_OHLC_df= client.daily_ohlc(config, model.daily_ohlc('ssi','01/05/2024', '03/06/2024', 1, 100, True))
    a = pd.DataFrame(daily_OHLC_df)
    a.to_json('./static/data5.json')                                 
     
import logging

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG)

def md_get_intraday_OHLC(symbol: str, from_date: str, to_date: str, page_index: int = 1, page_size: int = 100, option: bool = True, interval: int = 1) -> pd.DataFrame:
    try:
        # Gửi yêu cầu và nhận phản hồi từ API
        response = client.intraday_ohlc(config, model.intraday_ohlc(symbol, from_date, to_date, page_index, page_size, option, interval))
        
        # Log phản hồi từ API
        logging.debug("Phản hồi từ API: %s", response)
        
        # Kiểm tra sự tồn tại của khóa 'data'
        if 'data' in response:
            if response['data'] is not None and isinstance(response['data'], list):
                intraday_OHLC_data = response['data']
            else:
                logging.error("Khóa 'data' không phải là danh sách hoặc có giá trị None.")
                return pd.DataFrame()  # Trả về DataFrame rỗng nếu không có dữ liệu hợp lệ
        else:
            logging.error("Khóa 'data' không tồn tại trong phản hồi của API.")
            return pd.DataFrame()  # Trả về DataFrame rỗng nếu không có khóa 'data'

        # Chuyển đổi dữ liệu thành DataFrame
        intraday_OHLC_df = pd.DataFrame(intraday_OHLC_data, columns=['Symbol', 'Value', 'TradingDate', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
        
        # Chuyển đổi các cột ngày và thời gian
        intraday_OHLC_df['TradingDate'] = pd.to_datetime(intraday_OHLC_df['TradingDate'], format='%d/%m/%Y')
        intraday_OHLC_df['Time'] = pd.to_datetime(intraday_OHLC_df['Time'], format='%H:%M:%S').dt.strftime('%H:%M:%S')
        
        return intraday_OHLC_df

    except Exception as e:
        # Xử lý các lỗi khác
        logging.error("Đã xảy ra lỗi: %s", e)
        return pd.DataFrame()  # Trả về DataFrame rỗng nếu có lỗi








def md_get_daily_index():
	print(client.daily_index(config, model.daily_index( '123', 'VN100', '29/05/2024', '29/05/2024', 1, 1000, '', '')))

def md_get_stock_price():
	return(client.daily_stock_price(config, model.daily_stock_price ('SSI',  '29/05/2024',  '31/05/2024', 1, 1000, 'hose')))



def main():
    
    while True:
        print('11  - Securities List')
        print('12  - Securities Details')
        print('13  - Index Components')
        print('14  - Index List')
        print('15  - Daily OHLC')
        print('16  - Intraday OHLC')
        print('17  - Daily index')
        print('18  - Stock price')
        value = input('Enter your choice: ')

        if value == '11':
            md_get_securities_list()
        elif value == '12':
            md_get_securities_details_OHLC()
        elif value == '13':
            md_get_index_components()
        elif value == '14':
            md_get_index_list()
        elif value == '15':
            md_get_daily_OHLC()
        elif value == '16':
            md_get_intraday_OHLC()
        elif value == '17':
            md_get_daily_index()
        elif value == '18':
            md_get_stock_price()

if __name__ == '__main__':
	main()