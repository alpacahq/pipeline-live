import pytest

from pipeline_live.engine import LivePipelineEngine
from pipeline_live.data.iex.pricing import USEquityPricing
from pipeline_live.data.iex.classifiers import Sector

from pipeline_live.data.alpaca.factors import AverageDollarVolume
from zipline.pipeline import Pipeline


from .datamock import mock_iex
from .datamock import mock_tradeapi


@pytest.mark.skip("Need to fix test for eng.run_pipeline(pipe)")
def test_engine(refdata, stocks, alpaca_tradeapi):
    def list_symbols():
        return ['A', 'AA']

    mock_iex.get_available_symbols(refdata)
    mock_iex.get_key_stats(stocks)
    mock_iex.get_chart(stocks)
    mock_tradeapi.list_assets(alpaca_tradeapi)

    eng = LivePipelineEngine(list_symbols)
    ADV = AverageDollarVolume(window_length=20,)
    top5 = ADV.top(5, groupby=Sector())
    pipe = Pipeline({
        'top5': top5,
        'close': USEquityPricing.close.latest,
    }, screen=top5)

    df = eng.run_pipeline(pipe)
    assert sorted(df.columns) == ['close', 'top5']

    pipe = Pipeline({
        'close': USEquityPricing.close.latest,
    })

    df = eng.run_pipeline(pipe)
    assert df.shape == (2, 1)
    assert df.close['AA'] > 40
