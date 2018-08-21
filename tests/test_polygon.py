import pandas as pd
from pipeline_alpaca.polygon.fundamentals import PolygonCompany
from alpaca_trade_api.entity import Asset


def test_PolygonCompany(tradeapi, data_path):
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

    tradeapi.REST().polygon.get.return_value = [
        {'_id': '5a77fa83333c4e001174b898',
         'listdate': '1990-01-02',
         'cik': '0001675149',
         'bloomberg': 'EQ0000000045469815',
         'figi': None,
         'lei': 'ABPN11VOHLHX6QR7XQ48',
         'sic': 3334,
         'country': 'us',
         'industry': 'Metals & Mining',
         'sector': 'Basic Materials',
         'marketcap': 7837461871,
         'employees': 60000,
         'phone': '412-315-2900',
         'ceo': 'Roy C. Harvey',
         'url': 'http://www.alcoa.com',
         'description': 'Alcoa Corporation produces and sells bauxite, alumina, and aluminum products. It operates through six segments, Bauxite, Alumina, Aluminum, Cast Products, Energy, and Rolled Products. The company also offers aluminum cast products; and aluminum sheets for the production of cans for beverage, food, and pet food. In addition, it engages in the generation and sale of renewable energy, as well as provision of ancillary services. The company was formerly known as Alcoa Upstream Corporation and changed its name to Alcoa Corporation in October 2016. Alcoa Corporation is based in New York, New York.',  # noqa
         'exchange': 'New York Stock Exchange',
         'name': 'Alcoa Corp',
         'symbol': 'AA',
         '__v': 19,
         'logo': 'https://s3.polygon.io/logos/aa/logo.png',
         'created': '2018-02-05T06:32:35.464Z',
         'updated': '2018-02-05T06:32:35.464Z',
         'tags': ['Basic Materials', 'Aluminum', 'Metals & Mining'],
         'similar': ['BBL', 'CENX', 'KALU', 'BHP', 'ACH']}
    ]

    marketcap = PolygonCompany.marketcap
    loader = marketcap.dataset.get_loader()
    date = pd.Timestamp('2018-08-20', tz='utc')
    out = loader.load_adjusted_array([marketcap], [date], ['AA'], [])

    assert out[marketcap][0][0] > 10e6
