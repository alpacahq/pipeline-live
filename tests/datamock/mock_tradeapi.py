from alpaca_trade_api.entity import Asset, BarSet
from alpaca_trade_api.entity_v2 import BarsV2, Bar


def list_assets(tradeapi):
    tradeapi.REST().list_assets.return_value = [
        Asset({'asset_class': 'us_equity',
               'exchange': 'NYSE',
               'id': '3ca0202f-01f4-41a0-bb0c-c8864e767ebd',
               'status': 'active',
               'symbol': 'AA',
               'tradable': True}),
        Asset({'asset_class': 'us_equity',
               'exchange': 'NYSE',
               'id': '7595a8d2-68a6-46d7-910c-6b1958491f5c',
               'status': 'active',
               'symbol': 'A',
               'tradable': True}),
    ]


def get_bars(tradeapi):
    tradeapi.REST().get_bars.return_value = BarsV2([
            {
                's': 'AA',
                "t": "2022-02-28T05:00:00Z",
                "o": 163.14,
                "h": 165.4,
                "l": 162.46,
                "c": 165.28,
                "v": 1386252,
                "n": 14053,
                "vw": 164.070877
            }
        ])
