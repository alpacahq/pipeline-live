import pandas as pd
from pipeline_alpaca.polygon.fundamentals import PolygonCompany

from .datamock import mock_tradeapi


def test_PolygonCompany(tradeapi, data_path):
    mock_tradeapi.list_assets(tradeapi)
    mock_tradeapi.list_companies(tradeapi)

    marketcap = PolygonCompany.marketcap
    loader = marketcap.dataset.get_loader()
    date = pd.Timestamp('2018-08-20', tz='utc')
    out = loader.load_adjusted_array([marketcap], [date], ['AA'], [])

    assert out[marketcap][0][0] > 10e6
