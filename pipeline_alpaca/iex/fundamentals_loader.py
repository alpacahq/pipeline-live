import numpy as np

from zipline.pipeline.data.sources import iex
from zipline.pipeline.loaders.base import PipelineLoader


class IEXKeyStatsLoader(PipelineLoader):

    def load_adjusted_array(self, columns, dates, symbols, mask):
        asset_finder = self._asset_finder

        key_stats = iex.key_stats()
        out = {}
        for c in columns:
            data = [
                key_stats.get(symbol, {}).get(c.name, c.missing_value)
                for symbol in symbols
            ]
            out[c] = np.tile(np.array(data, dtype=c.dtype), (len(dates), 1))
        return out
