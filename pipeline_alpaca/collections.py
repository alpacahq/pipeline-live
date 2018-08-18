import numpy as np

from zipline.assets.assets_alpaca import AssetFinderAlpaca
from zipline.pipeline.filters import CustomFilter
from zipline.pipeline.data.sources import polygon


class IsPrimaryShare(CustomFilter):
    inputs = ()
    window_length = 1

    def __init__(self, *args, **kwargs):
        super(IsPrimaryShare, self).__init__(*args, **kwargs)
        self._asset_finder = AssetFinderAlpaca()

    def compute(self, today, sids, out, *inputs):
        asset_finder = self._asset_finder
        assets = asset_finder.retrieve_all(sids)

        companies = polygon.companies()
        financials = polygon.financials()
        ary = np.array([
            a.symbol in companies and
            'country' in companies[a.symbol] and
            [companies[a.symbol].get('country') == 'us'] and
            a.symbol in financials and
            len(financials[a.symbol]) > 0 and
            financials[a.symbol][0].get('totalRevenue') is not None
            for a in assets
        ], dtype=bool)
        out[:] = ary
