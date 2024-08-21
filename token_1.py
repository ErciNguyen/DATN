import config
from ssi_fc_data import fc_md_client , model # type: ignore
client = fc_md_client.MarketDataClient(config)
print(client.access_token(model.accessToken(config.consumerID, config.consumerSecret)))