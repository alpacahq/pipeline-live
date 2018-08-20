import pandas as pd
from pipeline_alpaca.iex.fundamentals import IEXKeyStats
import pytest
import tempfile
from unittest.mock import patch

from pipeline_alpaca.sources import iex as sources_iex


@pytest.fixture
def iexfinance():
    with patch.object(sources_iex, 'iexfinance') as iexfinance:
        yield iexfinance


@pytest.fixture
def data_path():
    with patch('zipline.utils.paths.data_path') as data_path:
        with tempfile.TemporaryDirectory() as t:
            data_path.return_value = t
            yield data_path


def test_IEXKeyStats(iexfinance, data_path):
    iexfinance.get_available_symbols.return_value = [
        {
            "symbol": "A",
            "name": "AGILENT TECHNOLOGIES INC",
            "date": "2017-04-19",
            "isEnabled": True,
            "type": "cs",
            "iexId": "1"
        },
        {
            "symbol": "AA",
            "name": "ALCOA CORP",
            "date": "2017-04-19",
            "isEnabled": True,
            "type": "cs",
            "iexId": "12042"
        }
    ]

    iexfinance.Stock().get_key_stats.return_value = {
        'A': {
            'companyName': 'Agilent Technologies Inc.',
            'marketcap': 20626540000,
            'beta': 1.369553,
            'week52high': 75,
            'week52low': 60.42,
            'week52change': 7.1948,
            'shortInterest': 5255310,
            'shortDate': '2018-07-31',
            'dividendRate': 0.596,
            'dividendYield': 0.9217445,
            'exDividendDate': '2018-07-02 00:00:00.0',
            'latestEPS': 2.1,
            'latestEPSDate': '2017-10-31',
            'sharesOutstanding': 319000000,
            'float': 315254758,
            'returnOnEquity': 6.5,
            'consensusEPS': 0.65,
            'numberOfEstimates': 10,
            'EPSSurpriseDollar': None,
            'EPSSurprisePercent': 0,
            'symbol': 'A',
            'EBITDA': 865000000,
            'revenue': 3514000000,
            'grossProfit': 1916000000,
            'cash': 8128000000,
            'debt': 6237000000,
            'ttmEPS': 2.57,
            'revenuePerShare': 11,
            'revenuePerEmployee': 251000,
            'peRatioHigh': 48.9,
            'peRatioLow': 7.8,
            'returnOnAssets': 3.59,
            'returnOnCapital': None,
            'profitMargin': 6.2,
            'priceToSales': 4.344874,
            'priceToBook': 4.47,
            'day200MovingAvg': 66.93319,
            'day50MovingAvg': 64.37124,
            'institutionPercent': 91.3,
            'insiderPercent': 1.2,
            'shortRatio': 2.8348546,
            'year5ChangePercent': 1.0195710363653967,
            'year2ChangePercent': 0.3607160068267285,
            'year1ChangePercent': 0.07194782502018399,
            'ytdChangePercent': -0.039041716824944034,
            'month6ChangePercent': -0.08608936423423595,
            'month3ChangePercent': 0.019282183212267934,
            'month1ChangePercent': 0.025697969543147167,
            'day5ChangePercent': -0.0194115862905672,
            'day30ChangePercent': 0.024397972116603283},
        'AA': {
            'companyName': 'Alcoa Corporation',
            'marketcap': 7837461871,
            'beta': 0.596731,
            'week52high': 62.35,
            'week52low': 38.05,
            'week52change': 11.1905,
            'shortInterest': 9035385,
            'shortDate': '2018-07-31',
            'dividendRate': 0,
            'dividendYield': 0,
            'exDividendDate': 0,
            'latestEPS': 1.16,
            'latestEPSDate': '2017-12-30',
            'sharesOutstanding': 186473040,
            'float': 186017718,
            'returnOnEquity': 2.59,
            'consensusEPS': 1.33,
            'numberOfEstimates': 5,
            'EPSSurpriseDollar': None,
            'EPSSurprisePercent': 14.2857,
            'symbol': 'AA',
            'EBITDA': 940000000,
            'revenue': 6138000000,
            'grossProfit': 1418000000,
            'cash': 1119000000,
            'debt': 1401000000,
            'ttmEPS': 4.05,
            'revenuePerShare': 33,
            'revenuePerEmployee': 420411,
            'peRatioHigh': 0,
            'peRatioLow': 0,
            'returnOnAssets': 0.85,
            'returnOnCapital': None,
            'profitMargin': 4.82,
            'priceToSales': 0.6035221,
            'priceToBook': 1.56,
            'day200MovingAvg': 47.8935,
            'day50MovingAvg': 45.0584,
            'institutionPercent': 86.9,
            'insiderPercent': 0.2,
            'shortRatio': 2.0121994,
            'year5ChangePercent': 0.8747240101162838,
            'year2ChangePercent': 0.8747240101162838,
            'year1ChangePercent': 0.11190476190476202,
            'ytdChangePercent': -0.23817292006525287,
            'month6ChangePercent': -0.1256500936134803,
            'month3ChangePercent': -0.17116939459672648,
            'month1ChangePercent': -0.12473969179508541,
            'day5ChangePercent': -0.05444319460067495,
            'day30ChangePercent': -0.12963346448540067}}

    marketcap = IEXKeyStats.marketcap
    loader = marketcap.dataset.get_loader()
    date = pd.Timestamp('2018-08-20', tz='utc')
    out = loader.load_adjusted_array([marketcap], [date], ['AA'], [])

    assert out[marketcap][0][0] != 0.0
