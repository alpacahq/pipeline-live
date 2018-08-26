from pipeline_alpaca.data.iex import factors
from pipeline_alpaca.data.iex.pricing import USEquityPricing


def test_factors():
    assert factors.AverageDollarVolume.inputs[0] == USEquityPricing.close
