import numpy as np

from zipline.pipeline.loaders.base import PipelineLoader

from pipeline_live.data.sources import polygon


class PolygonCompanyLoader(PipelineLoader):

    def load_adjusted_array(self, columns, dates, symbols, mask):

        company = polygon.company()
        out = {}
        for c in columns:
            data = [
                company.get(symbol, {}).get(c.name, c.missing_value)
                for symbol in symbols
            ]
            out[c] = np.tile(np.array(data, dtype=c.dtype), (len(dates), 1))

        return out
