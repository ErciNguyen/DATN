from ssi_fctrading import FCTradingClient
from ssi_fctrading.models import fcmodel_requests
from . import fc_config
from typing import Union
import os
from fastapi.responses import FileResponse
from fastapi import FastAPI
app = FastAPI()

import random
client = FCTradingClient(fc_config.Url, fc_config.ConsumerID,
	fc_config.ConsumerSecret, fc_config.PrivateKey, fc_config.TwoFAType)
print('Read token: ' + client.get_access_token())

# @app.get("/getdata")
# async def get_data():
	
# 	return ##
# @app.get("/favicon.ico", include_in_schema=False)
# async def favicon():
#     file_path = os.path.join(os.path.dirname(__file__), 'favicon.ico')
#     return FileResponse(file_path)

@app.get("/getOtp")
async def fc_get_otp():
	fc_req = fcmodel_requests.GetOTP(fc_config.ConsumerID, fc_config.ConsumerSecret)
	return client.get_otp(fc_req)

@app.get("/verifyCode")
async def fc_get_otp(code: str):
	"""Verify OTP or PIN (with TwoFAType in your config), if you use SMS OTP or Email OTP please get call getOtp to receive OTP before verify.
	 This function auto save OTP and accesstoken for New/Modify/Cancel order

	Returns:
		string: response json string
	"""
	return client.verifyCode(code)

@app.get("/newOrder")
async def fc_new_order(instrumentID: str, market: str, buySell: str, orderType: str
    , price: float, quantity: int, account: str, stopOrder: bool = False, stopPrice: float = 0, 
      stopType: str = '', stopStep: float = 0, lossStep: float = 0, profitStep: float = 0, deviceId: str = FCTradingClient.get_deviceid(), userAgent: str = FCTradingClient.get_user_agent()):
	
	"""Place new order

	Args:
	```	
	instrumentID (str): Mã chứng khoán
	market (str): Thị trường ('VN' hoặc 'VNFE')
	buySell (str): 'B' or 'S'
	orderType (str): Loại lệnh
	price (float): Giá. Với các lệnh điều kiện price=0
	quantity (int): Khối lượng
	account (str): Tài khoản
	stopOrder (bool, optional): Lệnh điều kiện (chỉ áp dụng với phái sinh). Defaults to False.
	stopPrice (float, optional): Giá trigger của lệnh điều kiện. Defaults to 0.
	stopType (str, optional): Loại lệnh điều kiện. Defaults to ''.
	stopStep (float, optional): . Defaults to 0.
	lossStep (float, optional): . Defaults to 0.
	profitStep (float, optional): . Defaults to 0.
	deviceId (str, optional): Định danh của thiết bị đặt lệnh
	userAgent (str, optional): Người dùng
	```
	"""
	fc_req = fcmodel_requests.NewOrder(str(account).upper()
	, str(random.randint(0, 99999999))
	, str(instrumentID).upper(), str(market).upper(), str(buySell).upper(), str(orderType).upper()
	, float(price), int(quantity), bool(stopOrder), float(stopPrice), str(stopType), float(stopStep)
 	, float(lossStep), float(profitStep),deviceId= str(deviceId), userAgent = str(userAgent))
	

	res = client.new_order(fc_req)
	return res

@app.get("/modifyOrder")
async def fc_modify_order(orderID: str, instrumentID: str, marketID: str, buySell: str, orderType: str
    , price: float, quantity: int, account: str, deviceId: str = FCTradingClient.get_deviceid(), userAgent: str = FCTradingClient.get_user_agent()):
	"""Modify order

	Args:
	```
	orderID (str): OrderID to modify
	instrumentID (str): Mã chứng khoán
	marketID (str): Thị trường ('VN' for stock 'VNFE' for derviratives)
	buySell (str): 'B' or 'S'
	orderType (str): Loại lệnh
	price (float): Giá
	quantity (int): Khối lượng
	account (str): Tài khoản
	deviceId (str, optional): Định danh thiết bị
	userAgent (str, optional): Định danh người dùng
	```
	Returns:
		Str: json string response
	"""
	fc_rq = fcmodel_requests.ModifyOrder(str(account)
	, str(random.randint(0, 99999999)), str(orderID)
	, str(marketID), str(instrumentID), float(price), int(quantity), str(buySell), str(orderType), deviceId= str(deviceId), userAgent= str(userAgent))

	res = client.modify_order(fc_rq)
	return res

@app.get("/cancelOrder")
async def fc_cancel_order(orderID: str, instrumentID: str, marketID: str, buySell: str, account: str, deviceId: str = FCTradingClient.get_deviceid(), userAgent: str = FCTradingClient.get_user_agent()):
	"""Cancel order

	Args:
	```
	orderID (str): Số hiệu lệnh cần hủy
	instrumentID (str): Mã chứng khoán
	marketID (str): Thị trường 'VN' (cơ sở) hay 'VNFE' (phái sinh)
	buySell (str): 'B' or 'S'
	account (str): Tài khoản
	deviceId (str, optional): Định danh thiết bị đặt lệnh. Defaults to ''.
	userAgent (str, optional): Định danh người dùng. Defaults to ''.
	```
	Returns:
		str: JSON string
	"""
	fc_rq = fcmodel_requests.CancelOrder(str(account), str(random.randint(0, 99999999))
	, str(orderID), str(marketID), str(instrumentID), str(buySell), deviceId=str(deviceId), userAgent=str(userAgent))

	res = client.cancle_order(fc_rq)
	return res

@app.get("/derNewOrder")
async def fc_der_new_order(instrumentID: str, market: str, buySell: str, orderType: str
    , price: float, quantity: int, account: str, stopOrder: bool = False, stopPrice: float = 0, 
      stopType: str = '', stopStep: float = 0, lossStep: float = 0, profitStep: float = 0, deviceId: str = FCTradingClient.get_deviceid(), userAgent: str = FCTradingClient.get_user_agent()):
	
	"""Place new derivatives order

	Args:
	```	
	instrumentID (str): Mã chứng khoán
	market (str): Thị trường ('VN' hoặc 'VNFE')
	buySell (str): 'B' or 'S'
	orderType (str): Loại lệnh
	price (float): Giá. Với các lệnh điều kiện price=0
	quantity (int): Khối lượng
	account (str): Tài khoản
	stopOrder (bool, optional): Lệnh điều kiện (chỉ áp dụng với phái sinh). Defaults to False.
	stopPrice (float, optional): Giá trigger của lệnh điều kiện. Defaults to 0.
	stopType (str, optional): Loại lệnh điều kiện. Defaults to ''.
	stopStep (float, optional): . Defaults to 0.
	lossStep (float, optional): . Defaults to 0.
	profitStep (float, optional): . Defaults to 0.
	deviceId (str, optional): Định danh của thiết bị đặt lệnh
	userAgent (str, optional): Người dùng
	```
	"""
	fc_req = fcmodel_requests.NewOrder(str(account).upper()
	, str(random.randint(0, 99999999))
	, str(instrumentID).upper(), str(market).upper(), str(buySell).upper(), str(orderType).upper()
	, float(price), int(quantity), bool(stopOrder), float(stopPrice), str(stopType), float(stopStep)
 	, float(lossStep), float(profitStep),deviceId= str(deviceId), userAgent = str(userAgent))
	

	res = client.der_new_order(fc_req)
	return res

@app.get("/derModifyOrder")
async def fc_der_modify_order(orderID: str, instrumentID: str, marketID: str, buySell: str, orderType: str
    , price: float, quantity: int, account: str, deviceId: str = FCTradingClient.get_deviceid(), userAgent: str = FCTradingClient.get_user_agent()):
	"""Derivative Modify order

	Args:
	```
	orderID (str): OrderID to modify
	instrumentID (str): Mã chứng khoán
	marketID (str): Thị trường ('VN' for stock 'VNFE' for derviratives)
	buySell (str): 'B' or 'S'
	orderType (str): Loại lệnh
	price (float): Giá
	quantity (int): Khối lượng
	account (str): Tài khoản
	deviceId (str, optional): Định danh thiết bị
	userAgent (str, optional): Định danh người dùng
	```
	Returns:
		Str: json string response
	"""
	fc_rq = fcmodel_requests.ModifyOrder(str(account)
	, str(random.randint(0, 99999999)), str(orderID)
	, str(marketID), str(instrumentID), float(price), int(quantity), str(buySell), str(orderType), deviceId= str(deviceId), userAgent= str(userAgent))

	res = client.der_modify_order(fc_rq)
	return res

@app.get("/derCancelOrder")
async def fc_der_cancel_order(orderID: str, instrumentID: str, marketID: str, buySell: str, account: str, deviceId: str = FCTradingClient.get_deviceid(), userAgent: str = FCTradingClient.get_user_agent()):
	"""Derivative cancel order

	Args:
	```
	orderID (str): Số hiệu lệnh cần hủy
	instrumentID (str): Mã chứng khoán
	marketID (str): Thị trường 'VN' (cơ sở) hay 'VNFE' (phái sinh)
	buySell (str): 'B' or 'S'
	account (str): Tài khoản
	deviceId (str, optional): Định danh thiết bị đặt lệnh. Defaults to ''.
	userAgent (str, optional): Định danh người dùng. Defaults to ''.
	```
	Returns:
		str: JSON string
	"""
	fc_rq = fcmodel_requests.CancelOrder(str(account), str(random.randint(0, 99999999))
	, str(orderID), str(marketID), str(instrumentID), str(buySell), deviceId=str(deviceId), userAgent=str(userAgent))

	res = client.der_cancle_order(fc_rq)
	return res

@app.get("/stockAccountBalance")
async def fc_stock_account_balance(account: str):
	"""Get stock account balance

	Args:
	```
 	account (str): stock account id
  	```
	Returns:
	```
 	str: Json str
  	```
	"""	
	
	fc_rq = fcmodel_requests.StockAccountBalance(str(account))

	res = client.get_stock_account_balance(fc_rq)
	return res

@app.get("/derivativeAccountBalance")
async def fc_derivative_account_balance(account: str):
	"""Get derivative account balance

	Args:
		account (str): derivative account id

	Returns:
		str: Json str
	"""	
	
	fc_rq = fcmodel_requests.DerivativeAccountBalance(str(account))

	res = client.get_derivative_account_balance(fc_rq)
	return res

@app.get("/ppmmrAccount")
async def fc_pp_mmr_account(account: str):
	"""Get pp and mmr of account

	Args:
		account (str): stock account id

	Returns:
		str: Json str
	"""	
	
	fc_rq = fcmodel_requests.PPMMRAccount(str(account))

	res = client.get_pp_mmr_account(fc_rq)
	return res

@app.get("/stockPosition")
async def fc_stock_position(account: str):
	"""Get stock position of account

	Args:
		account (str): stock account id

	Returns:
		str: Json str
	"""	
	
	fc_rq = fcmodel_requests.StockPosition(str(account))

	res = client.get_stock_position(fc_rq)
	return res

@app.get("/derivativePosition")
async def fc_derivative_position(account: str):
	"""Get derivative position of account

	Args:
		account (str): derivative account id

	Returns:
		str: Json str
	"""	
	
	fc_rq = fcmodel_requests.DerivativePosition(str(account))

	res = client.get_derivative_position(fc_rq)
	return res

@app.get("/maxBuyQty")
async def fc_max_buy_qty(account: str, instrumentID: str, price: float):
	"""Get max buy qty

	Args:
		account (str): account id
		instrumentID (str): buy instrument
		price (float): buy price

	Returns:
		str: json string
	"""
	
	fc_rq = fcmodel_requests.MaxBuyQty(str(account), str(instrumentID), float(price))

	res = client.get_max_buy_qty(fc_rq)
	return res

@app.get("/maxSellQty")
async def fc_max_sell_qty(account: str, instrumentID: str, price: float =0):
	"""Get max sell qty

	Args:
		account (str): account id
		instrumentID (str): sell instrument
		price (float): sell price ( for dervatives exchange )

	Returns:
		str: json string
	"""
	
	fc_rq = fcmodel_requests.MaxSellQty(str(account), str(instrumentID), float(price))

	res = client.get_max_sell_qty(fc_rq)
	return res

@app.get("/orderHistory")
async def fc_order_history(account: str, startDate: str, endDate: str):
	"""Get order history

	Args:
		account (str): account id
		startDate (str): from date (format 'DD/MM/YYYY' ex: 21/05/2021)
		endDate (str): end date (format 'DD/MM/YYYY' ex: 21/05/2021)

	Returns:
		[str]: json string
	"""
	
	fc_rq = fcmodel_requests.OrderHistory(str(account), str(startDate), str(endDate))

	res = client.get_order_history(fc_rq)
	return res

@app.get("/orderBook")
async def fc_order_book(account: str):
	"""Get order book

	Args:
		account (str): account id

	Returns:
		[str]: json string
	"""
	
	fc_rq = fcmodel_requests.OrderBook(str(account))

	res = client.get_order_book(fc_rq)
	return res

@app.get("/auditOrderBook")
async def fc_audit_order_book(account: str):
	"""Get audit order book ( include order error)

	Args:
		account (str): account id

	Returns:
		[str]: json string
	"""
	
	fc_rq = fcmodel_requests.AuditOrderBook(str(account))

	res = client.get_audit_order_book(fc_rq)
	return res