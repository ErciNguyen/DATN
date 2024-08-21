import pandas as pd
from datetime import datetime, time
from examples.fc_config import SELL, BUY, NONE
import ssi_api

class Technicals:
    def __init__(self, settings, api, pair, log=None):
        self.settings = settings
        self.log = log
        self.api = api
        self.pair = pair
        
    def log_message(self, msg):
        if self.log is not None:
            self.log.logger.debug(msg)

    def fetch_candles(self, row_count, candle_time):
        current_date = datetime.now().strftime('%d/%m/%Y')
        try:
            # Gọi API để lấy dữ liệu nến
            df = self.api.fetch_candles(self.pair, current_date, current_date, 1, row_count, True, 1)
            
            # Kiểm tra xem dữ liệu nến có hợp lệ không
            if df is None:
                self.log_message(f"Error fetching candles for pair: {self.pair}, df None")
                return None
            elif df.empty:
                self.log_message(f"No data returned from fetch_candles for pair: {self.pair}")
                return None
            
        except TypeError as e:
            self.log_message(f"Error fetching candles for pair: {self.pair}, error: {e}")
            return None

        # Lấy thời gian của cây nến mới nhất từ hàm last_complete_candle
        last_candle_time = self.api.last_complete_candle(self.pair)
        last_candle_datetime = datetime.combine(datetime.now().date(), last_candle_time)
        candle_datetime = datetime.combine(datetime.now().date(), candle_time)

        if abs(pd.Timestamp(last_candle_datetime) - pd.Timestamp(candle_datetime)).seconds > 10:
            self.log_message(f"Error fetching candles for pair: {self.pair}, expected time: {candle_datetime}, actual time: {last_candle_datetime}")
            return None
        self.log_message(f"Fetched last candle time: {last_candle_time} for pair: {self.pair}")

        return df


    def process_candles(self, df):
        df.reset_index(drop=True, inplace=True)
                # Chuyển đổi các cột High và Low sang kiểu số
        df['High'] = pd.to_numeric(df['High'], errors='coerce')
        df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

        # Kiểm tra xem có giá trị nào bị chuyển thành NaN không
        if df['High'].isnull().any() or df['Low'].isnull().any():
            self.log_message(f"Data contains NaN after conversion: High - {df['High'].isnull().sum()} NaNs, Low - {df['Low'].isnull().sum()} NaNs")
            return None
        df['PAIR'] = self.pair
        df['SPREAD'] = df['High'] - df['Low']

        short_prev = 'PREV_SHORT'
        long_prev = 'PREV_LONG'

        short_col = f'MA_{self.settings.short_ma}'
        long_col = f'MA_{self.settings.long_ma}'

        df['mid_c'] = (df['High'] + df['Low'] + df['Close']) / 3

        df[short_col] = df['mid_c'].rolling(window=self.settings.short_ma).mean()
        df[long_col] = df['mid_c'].rolling(window=self.settings.long_ma).mean()

        df[short_prev] = df[short_col].shift(1)
        df[long_prev] = df[long_col].shift(1)

        df['D_PREV'] = df[short_prev] - df[long_prev]
        df['D_NOW'] = df[short_col] - df[long_col]

        last = df.iloc[-1]
        decision = NONE

        if last['D_NOW'] < 0 and last['D_PREV'] > 0:
            decision = SELL
        elif last['D_NOW'] > 0 and last['D_PREV'] < 0:
            decision = BUY

        log_cols = ['Time', 'Volume', 'mid_c', 'SPREAD', 'PAIR', short_col, long_col, short_prev, long_prev, 'D_PREV', 'D_NOW']
        self.log_message(f"Processed_df\n{df[log_cols].tail(2)}")
        self.log_message(f"Trade_decision: {decision}")
        self.log_message("")

        return decision

    def get_trade_decision(self, candle_time):
        max_rows = self.settings.long_ma + 2
        self.log_message("")
        self.log_message(f"get_trade_decision() pair: {self.pair} max_rows: {max_rows}")
      
        df = self.fetch_candles(max_rows,candle_time)
        if df is not None:
            return self.process_candles(df)
        return NONE
