from pipeline_live.data.sources import iex, polygon

from .datamock import mock_iex, mock_tradeapi


def test_polygon(tradeapi, data_path):
    mock_tradeapi.list_assets(tradeapi)
    mock_tradeapi.list_financials(tradeapi)

    data = polygon.financials()
    assert len(data['AA']) == 5
    assert data['AA'][-1]['totalCash'] > 10e7

    mock_tradeapi.list_companies(tradeapi)
    data = polygon.company()
    assert len(data) == 2
    assert data['AA']['name'] == 'Alcoa Corp'


def test_iex(iexfinance, data_path):
    mock_iex.get_available_symbols(iexfinance)
    mock_iex.get_key_stats(iexfinance)

    kstats = iex.key_stats()

    assert len(kstats) == 2
    assert kstats['AA']['latestEPSDate'] == '2017-12-30'

    # cached
    kstats = iex.key_stats()
    assert kstats['AA']['returnOnCapital'] is None

    mock_iex.get_financials(iexfinance)

    financials = iex.financials()
    assert len(financials) == 1
    assert len(financials['AA']) == 4

    ed = iex._ensure_dict(1, ['AA'])
    assert ed['AA'] == 1

    mock_iex.get_chart(iexfinance)

    data = iex.get_stockprices()
    assert len(data) == 1
    data['AA'].open[1] == 43.2
