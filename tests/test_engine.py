from pipeline_live.engine import LivePipelineEngine
from pipeline_live.data.iex.pricing import USEquityPricing
from pipeline_live.data.iex.classifiers import Sector
from pipeline_live.data.iex.factors import AverageDollarVolume
from zipline.pipeline import Pipeline


from .datamock import mock_iex


def test_engine(iexfinance, data_path):
    def list_symbols():
        return ['A', 'AA']

    mock_iex.get_available_symbols(iexfinance)
    mock_iex.get_key_stats(iexfinance)
    mock_iex.get_chart(iexfinance)

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
