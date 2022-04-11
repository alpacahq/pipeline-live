from pipeline_live.data.sources import alpaca, iex

from .datamock import mock_iex, mock_tradeapi


def test_alpaca(alpaca_tradeapi, data_path):
    mock_tradeapi.list_assets(alpaca_tradeapi)
    mock_tradeapi.get_bars(alpaca_tradeapi)

    data = alpaca.get_stockprices(2)
    assert data['AA'].iloc[0].close == 165.28


def test_iex(refdata, stocks, data_path):
    mock_iex.get_available_symbols(refdata)
    mock_iex.get_key_stats(stocks)

    kstats = iex.key_stats()

    assert len(kstats) == 2
    assert kstats['AA']['latestEPSDate'] == '2017-12-30'

    # cached
    kstats = iex.key_stats()
    assert kstats['AA']['returnOnCapital'] is None

    mock_iex.get_financials(stocks)

    financials = iex.financials()
    assert len(financials) == 1
    assert len(financials['AA']) == 4

    ed = iex._ensure_dict(1, ['AA'])
    assert ed['AA'] == 1

    mock_iex.get_chart(stocks)

    data = iex.get_stockprices()
    assert len(data) == 1
    data['AA'].open[1] == 43.2
