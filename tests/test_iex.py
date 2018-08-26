import numpy as np
import pandas as pd

from pipeline_live.data.iex.fundamentals import IEXKeyStats
from pipeline_live.data.iex.pricing import USEquityPricing

from .datamock import mock_iex


def test_IEXKeyStats(iexfinance, data_path):

    mock_iex.get_available_symbols(iexfinance)
    mock_iex.get_key_stats(iexfinance)

    marketcap = IEXKeyStats.marketcap
    loader = marketcap.dataset.get_loader()
    date = pd.Timestamp('2018-08-20', tz='utc')
    out = loader.load_adjusted_array([marketcap], [date], ['AA'], [])

    assert out[marketcap][0][0] != 0.0


def test_pricing_loader(iexfinance, data_path):
    mock_iex.get_available_symbols(iexfinance)
    mock_iex.get_chart(iexfinance)

    loader = USEquityPricing.get_loader()
    columns = [USEquityPricing.close]
    dates = [pd.Timestamp('2018-08-22', tz='UTC')]
    symbols = ['AA']
    mask = np.zeros((1, 1), dtype='bool')
    out = loader.load_adjusted_array(columns, dates, symbols, mask)

    assert out[USEquityPricing.close]._data.shape == (1, 1)
