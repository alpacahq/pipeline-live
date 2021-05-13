import pandas as pd
from pipeline_live.data.polygon.fundamentals import PolygonCompany
from pipeline_live.data.polygon.filters import (
    IsPrimaryShareEmulation, StaticSymbols
)

from .datamock import mock_tradeapi


def test_PolygonCompany(tradeapi, data_path):
    mock_tradeapi.list_assets(tradeapi)
    mock_tradeapi.list_companies(tradeapi)

    domains = None
    marketcap = PolygonCompany.marketcap
    loader = marketcap.dataset.get_loader()
    date = pd.Timestamp('2018-08-20', tz='utc')
    out = loader.load_adjusted_array(domains, [marketcap], [date], ['AA'], [])

    assert out[marketcap][0][0] > 10e6


def test_IsPrimaryShareEmulation(tradeapi, data_path):
    mock_tradeapi.list_companies(tradeapi)
    mock_tradeapi.list_financials(tradeapi)

    emu = IsPrimaryShareEmulation()

    today = object()
    symbols = ['A', 'AA']
    out = [None, None]
    emu.compute(today, symbols, out)
    assert not out[0]


def test_StaticSymbols(tradeapi, data_path):
    symbols = ('A', 'BB')
    emu = StaticSymbols(symbols=symbols)

    today = object()
    assets = ['A', 'AA', 'BB']
    out = [None, None, None]
    emu.compute(today, assets, out, symbols)
    assert not out[1]
