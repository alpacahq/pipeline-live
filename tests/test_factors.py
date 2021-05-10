from pipeline_live.data.iex import factors
from pipeline_live.data.iex.pricing import USEquityPricing


def test_factors():
    factor = factors.AverageDollarVolume(
        window_length=30,
        inputs=[USEquityPricing.close, USEquityPricing.volume])

    assert factor.inputs[0] == USEquityPricing.close
