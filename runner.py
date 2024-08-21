from ssi_fctrading import FCTradingClient
from fastapi import FastAPI
from examples import fc_client_ex as api
while True:
    command = input("enter command: ")
    if command == "T":
        print("Make a Trade: ")
        api.fc_new_order
