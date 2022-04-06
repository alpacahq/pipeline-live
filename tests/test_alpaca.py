import pandas as pd
import numpy as np

from .datamock import mock_tradeapi

from pipeline_live.data.alpaca.pricing import USEquityPricing

def test_pricing_loader(refdata, alpaca_tradeapi, data_path):
    mock_tradeapi.list_assets(alpaca_tradeapi)
    mock_tradeapi.get_bars(alpaca_tradeapi)

    loader = USEquityPricing.get_loader()
    columns = [USEquityPricing.close]
    dates = [pd.Timestamp('2018-08-22', tz='UTC')]
    symbols = ['AA']
    mask = np.zeros((1, 1), dtype='bool')
    out = loader.load_adjusted_array(columns, dates, symbols, mask)

    assert out[USEquityPricing.close]._data.shape == (1, 1)
