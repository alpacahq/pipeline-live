import numpy as np

from pipeline_live.data.sources import iex
from zipline.pipeline.loaders.base import PipelineLoader
from zipline.utils.numpy_utils import object_dtype


class IEXBaseLoader(PipelineLoader):

    def load_adjusted_array(self, columns, dates, symbols, mask):
        symbol_dict = self._load()
        out = {}
        for c in columns:
            data = np.array([
                symbol_dict.get(symbol, {}).get(c.name, c.missing_value)
                for symbol in symbols
            ], dtype=c.dtype)
            if c.dtype == object_dtype:
                data[data == None] = c.missing_value  # noqa
            out[c] = np.tile(data, (len(dates), 1))
        return out


class IEXKeyStatsLoader(IEXBaseLoader):

    def _load(self):
        return iex.key_stats()


class IEXCompanyLoader(IEXBaseLoader):

    def _load(self):
        return iex.company()
