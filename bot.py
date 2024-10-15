from datetime import datetime, time
import pprint
import time as time_module
from setting import Settings
from log_warpper import logWrapper
from timing import Timing
from ssi_api import SsiAPI
from technicals import Technicals
from examples.fc_config import NONE, BUY, SELL
from trade_manager import TradeManager
SLEEP = 10.0
ROW_COUNT = 1000

class TradingBot:
    def __init__(self):
        self.log = logWrapper("Bot")
        self.tech_log = logWrapper("TechnicalsBot")
        self.trade_log = logWrapper("Trade")
        self.trade_pairs = Settings.get_pairs()
        self.settings = {setting.pair: setting for setting in Settings.load_settings()}
        self.api = SsiAPI()
        self.trade_manager = TradeManager(self.api, self.settings, self.trade_log)
        self.timings = {pair: Timing(self.api.last_complete_candle(pair)) for pair in self.trade_pairs}
        
        self.log_message(f"Bot started with\n{pprint.pformat(self.settings)}")
        self.log_message(f"Bot Timing with\n{pprint.pformat({pair: str(timing) for pair, timing in self.timings.items()})}")

    def log_message(self, msg):
        self.log.logger.debug(msg)

    def update_timings(self):
        for pair in self.trade_pairs:
            current = self.api.last_complete_candle(pair)
            if current > self.timings[pair].last_candle:
                self.timings[pair].ready = True
                self.timings[pair].last_candle = current
                self.log_message(f"{pair} new candle {current}")
            else:
                self.timings[pair].ready = False

    def process_pairs(self):
        trades_to_make = []
        for pair in self.trade_pairs:
            if pair not in self.settings:
                self.log_message(f"Pair {pair} not found in settings")
                continue
            if self.timings[pair].ready:
                self.log_message(f"Ready to trade {pair}")
                techs = Technicals(self.settings[pair], self.api, pair, log=self.tech_log)
                decision = techs.get_trade_decision(self.timings[pair].last_candle)

                units = decision * self.settings[pair].units
                if units != 0:
                    trades_to_make.append({
                        'instrumentID': pair,
                        'market': 'VN',
                        'buySell': 'B' if units > 0 else 'S',
                        'orderType': 'LIMIT',
                        'price': 0,
                        'quantity': abs(units),
                        'account': '7064691',
                        'stopOrder': False,
                        'stopPrice': 0,
                        'stopType': '',
                        'stopStep': 0,
                        'lossStep': 0,
                        'profitStep': 0
                    })
        if trades_to_make:
            print(trades_to_make)
            self.trade_manager.place_trades(trades_to_make)

    def run(self):
        while True:
            print("update time")
            self.update_timings()
            print("process time")
            self.process_pairs()
            time_module.sleep(SLEEP)

if __name__ == "__main__":
    b = TradingBot()
    b.run()
