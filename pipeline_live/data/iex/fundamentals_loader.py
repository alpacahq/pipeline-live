import logging

import numpy as np
from interface import implements
from pipeline_live.data.sources import iex
from zipline.pipeline.loaders.base import PipelineLoader
from zipline.utils.numpy_utils import object_dtype

log = logging.getLogger(__name__)


class IEXEventLoader(implements(PipelineLoader)):

    def _safe_flat_getter(self, symbol, symbols, column):
        data = symbols.get(symbol, None)
        out = column.missing_value
        if data:
            out = data[0].get(column.name, column.missing_value)
        return out


    def load_adjusted_array(self, domain, columns, dates, sids, mask):
        symbol_dict = self._load()
        out = {}
        for c in columns:
            data = np.array([
                self._safe_flat_getter(symbol, symbol_dict, c)
                for symbol in sids
            ], dtype=c.dtype)
            if c.dtype == object_dtype:
                data[data == None] = c.missing_value  # noqa
            out[c] = np.tile(data, (len(dates), 1))
        return out


class IEXBaseLoader(implements(PipelineLoader)):

    def load_adjusted_array(self, domain, columns, dates, sids, mask):
        symbol_dict = self._load()
        out = {}
        for c in columns:
            data = np.array([
                symbol_dict.get(symbol, {}).get(c.name, c.missing_value)
                for symbol in sids
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


class IEXFinancialsLoader(IEXEventLoader):

    def _load(self):
        log.info('Loading Financials')
        return iex.financials()


class IEXEarningsLoader(IEXEventLoader):

    def _load(self):
        log.info('Loading Earnings')
        return iex.earnings()
