'''
Duplicate builtin factor classes in zipline with IEX's USEquityPricing
'''

from zipline.pipeline.data import USEquityPricing as z_pricing
from zipline.pipeline import factors as z_factors

from .pricing import USEquityPricing as alpaca_pricing


def _replace_inputs(inputs):
    map = {
        z_pricing.open: alpaca_pricing.open,
        z_pricing.high: alpaca_pricing.high,
        z_pricing.low: alpaca_pricing.low,
        z_pricing.close: alpaca_pricing.close,
        z_pricing.volume: alpaca_pricing.volume,
    }

    if type(inputs) not in (list, tuple, set):
        return inputs
    return tuple([
        map.get(inp, inp) for inp in inputs
    ])


for name in dir(z_factors):
    factor = getattr(z_factors, name)
    if factor != z_factors.Factor and hasattr(
            factor, 'inputs') and issubclass(
            factor, z_factors.Factor):
        new_factor = type(factor.__name__, (factor,), {
            'inputs': _replace_inputs(factor.inputs)
        })
        locals()[factor.__name__] = new_factor
