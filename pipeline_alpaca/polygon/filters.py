import numpy as np

from zipline.pipeline.filters import CustomFilter
from pipeline_alpaca.sources import polygon


class IsPrimaryShare(CustomFilter):
    inputs = ()
    window_length = 1

    def compute(self, today, symbols, out, *inputs):
        companies = polygon.companies()
        financials = polygon.financials()
        ary = np.array([
            symbol in companies and
            'country' in companies[symbol] and
            [companies[symbol].get('country') == 'us'] and
            symbol in financials and
            len(financials[symbol]) > 0 and
            financials[symbol][0].get('totalRevenue') is not None
            for symbol in symbols
        ], dtype=bool)
        out[:] = ary
