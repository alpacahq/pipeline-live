import numpy as np

from zipline.pipeline.filters import CustomFilter
from pipeline_alpaca.sources import polygon


class IsPrimaryShareEmulation(CustomFilter):
    inputs = ()
    window_length = 1

    def compute(self, today, symbols, out, *inputs):
        company = polygon.company()
        financials = polygon.financials()
        ary = np.array([
            symbol in company and
            'country' in company[symbol] and
            [company[symbol].get('country') == 'us'] and
            symbol in financials and
            len(financials[symbol]) > 0 and
            financials[symbol][0].get('totalRevenue') is not None
            for symbol in symbols
        ], dtype=bool)
        out[:] = ary
