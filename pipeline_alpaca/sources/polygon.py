import alpaca_trade_api as tradeapi

from .util import (
    daily_cache, parallelize
)


def list_symbols():
    return [
        a.symbol for a in tradeapi.REST().list_assets()
        if a.tradable and a.status == 'active'
    ]


def company():
    all_symbols = list_symbols()
    return _company(all_symbols)


@daily_cache(filename='polygon_company.pkl')
def _company(all_symbols):
    def fetch(symbols):
        api = tradeapi.REST()
        params = {
            'symbols': ','.join(symbols),
        }
        response = api.polygon.get('/meta/symbols/company', params=params)
        return {
            o['symbol']: o for o in response
        }

    return parallelize(fetch, workers=25, splitlen=50)(all_symbols)


def financials():
    all_symbols = list_symbols()
    return _financials(all_symbols)


@daily_cache(filename='polygon_financials.pkl')
def _financials(all_symbols):
    def fetch(symbols):
        api = tradeapi.REST()
        params = {
            'symbols': ','.join(symbols),
        }
        return api.polygon.get('/meta/symbols/financials', params=params)

    return parallelize(fetch, workers=25, splitlen=50)(all_symbols)
