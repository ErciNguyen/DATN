class TradeManager():
    def __init__(self, api, settings, log=None):
        self.api = api
        self.log = log
        self.settings = settings

    def log_message(self, msg):
        if self.log is not None:
            self.log.logger.debug(msg)
            
    async def close_trades(self, pairs_to_close):
        try:
            open_trades, ok = await self.api.open_trades()
            
            if not ok:
                self.log_message("Error fetching open trades!!!!")
                return
            
            ids_to_close = [x.orderID for x in open_trades if x.instrumentID in pairs_to_close]

            self.log_message(f"TradeManager:close_trades() pairs_to_close:{pairs_to_close} ")
            self.log_message(f"TradeManager:close_trades() open_trades:{open_trades} ")
            self.log_message(f"TradeManager:close_trades() ids_to_close:{ids_to_close} ")
            
            for t in ids_to_close:
                close_ok = await self.api.close_trade(t)
                if not close_ok:
                    self.log_message(f"TradeManager:close_trades() {t} FAILED TO CLOSE ")
                else:
                    self.log_message(f"TradeManager:close_trades() Closed")
        except Exception as e:
            self.log_message(f"TradeManager: Exception occurred while closing trades: {e}")

    async def create_trades(self, trades_to_make):
        for t in trades_to_make:
            try:
                response = await self.api.place_order(
                    t['instrumentID'],
                    t['market'],
                    t['buySell'],
                    t['orderType'],
                    t['price'],
                    t['quantity'],
                    t['account'],
                    t.get('stopOrder', False),
                    t.get('stopPrice', 0),
                    t.get('stopType', ''),
                    t.get('stopStep', 0),
                    t.get('lossStep', 0),
                    t.get('profitStep', 0)
                )
                if response:
                    self.log_message(f"TradeManager: Opened trade {response}: {t}")
                else:
                    self.log_message(f"TradeManager: FAILED TO OPEN {t}: {response}")
            except Exception as e:
                self.log_message(f"TradeManager: Exception occurred while opening trade {t}: {e}")

    async def place_trades(self, trades_to_make):
        self.log_message(f"TradeManager:place_trades() {trades_to_make}")
        pairs = [x['instrumentID'] for x in trades_to_make]
        await self.close_trades(pairs)
        await self.create_trades(trades_to_make)
