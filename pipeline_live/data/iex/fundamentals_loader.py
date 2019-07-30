import logging

import numpy as np

from pipeline_live.data.sources import iex
from zipline.pipeline.loaders.base import PipelineLoader
from zipline.utils.numpy_utils import object_dtype

log = logging.getLogger(__name__)

class IEXBaseLoader(PipelineLoader):

    flatten = False

    def load_adjusted_array(self, columns, dates, symbols, mask):
        log.deubg('Load Adjusted Array')

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
        log.info('Loading Key Stats')
        return iex.key_stats()


class IEXCompanyLoader(IEXBaseLoader):

    def _load(self):
        log.info('Loading Company Stats')
        return iex.company()


class IEXFinancialsLoader(IEXBaseLoader):

    flatten = True
    flatten_field = 'financials'

    def _load(self):
        log.info('Loading Financials')
        return iex.financials()


class IEXEarningsLoader(IEXBaseLoader):

    flatten = True
    flatten_field = 'earnings'

    def _load(self):
        log.info('Loading Earnings')
        return iex.earnings()
