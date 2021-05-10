import numpy as np
import pandas as pd

from pipeline_live.data.iex.fundamentals import IEXKeyStats
from pipeline_live.data.iex.pricing import USEquityPricing

from .datamock import mock_iex


def test_IEXKeyStats(refdata, stocks, data_path):

    mock_iex.get_available_symbols(refdata)
    mock_iex.get_key_stats(stocks)

    domains = None
    marketcap = IEXKeyStats.marketcap
    loader = marketcap.dataset.get_loader()
    date = pd.Timestamp('2018-08-20', tz='utc')
    out = loader.load_adjusted_array(domains, [marketcap], [date], ['AA'], [])

    assert out[marketcap][0][0] != 0.0


def test_pricing_loader(refdata, stocks, data_path):
    mock_iex.get_available_symbols(refdata)
    mock_iex.get_chart(stocks)

    loader = USEquityPricing.get_loader()
    columns = [USEquityPricing.close]
    domains = None
    dates = [pd.Timestamp('2018-08-22', tz='UTC')]
    symbols = ['AA']
    mask = np.zeros((1, 1), dtype='bool')
    out = loader.load_adjusted_array(domains, columns, dates, symbols, mask)

    assert out[USEquityPricing.close]._data.shape == (1, 1)
