import numpy as np
import logbook
import pandas as pd

from zipline.lib.adjusted_array import AdjustedArray
from zipline.pipeline.loaders.base import PipelineLoader
from zipline.utils.calendars import get_calendar
from zipline.errors import NoFurtherDataError

from pipeline_live.data.sources import iex


log = logbook.Logger(__name__)


class USEquityPricingLoader(PipelineLoader):
    """
    PipelineLoader for US Equity Pricing data
    """

    def __init__(self):
        cal = get_calendar('NYSE')

        self._all_sessions = cal.all_sessions

    def load_adjusted_array(self, columns, dates, symbols, mask):
        # load_adjusted_array is called with dates on which the user's algo
        # will be shown data, which means we need to return the data that would
        # be known at the start of each date.  We assume that the latest data
        # known on day N is the data from day (N - 1), so we shift all query
        # dates back by a day.
        start_date, end_date = _shift_dates(
            self._all_sessions, dates[0], dates[-1], shift=1,
        )

        sessions = self._all_sessions
        sessions = sessions[(sessions >= start_date) & (sessions <= end_date)]

        chart_range = '1m'
        timedelta = pd.Timestamp.utcnow() - start_date
        if timedelta > pd.Timedelta('730 days'):
            chart_range = '5y'
        elif timedelta > pd.Timedelta('365 days'):
            chart_range = '2y'
        elif timedelta > pd.Timedelta('180 days'):
            chart_range = '1y'
        elif timedelta > pd.Timedelta('90 days'):
            chart_range = '6m'
        elif timedelta > pd.Timedelta('30 days'):
            chart_range = '3m'
        log.info('chart_range={}'.format(chart_range))
        prices = iex.get_stockprices(chart_range)

        dfs = []
        for symbol in symbols:
            if symbol not in prices:
                df = pd.DataFrame(
                    {c.name: c.missing_value for c in columns},
                    index=sessions
                )
            else:
                df = prices[symbol]
                df = df.reindex(sessions, method='ffill')
            dfs.append(df)

        raw_arrays = {}
        for c in columns:
            colname = c.name
            raw_arrays[colname] = np.stack([
                df[colname].values for df in dfs
            ], axis=-1)
        out = {}
        for c in columns:
            c_raw = raw_arrays[c.name]
            out[c] = AdjustedArray(
                c_raw.astype(c.dtype),
                {},
                c.missing_value
            )
        return out


def _shift_dates(dates, start_date, end_date, shift):
    try:
        start = dates.get_loc(start_date)
    except KeyError:
        if start_date < dates[0]:
            raise NoFurtherDataError(
                msg=(
                    "Pipeline Query requested data starting on {query_start}, "
                    "but first known date is {calendar_start}"
                ).format(
                    query_start=str(start_date),
                    calendar_start=str(dates[0]),
                )
            )
        else:
            raise ValueError("Query start %s not in calendar" % start_date)

    # Make sure that shifting doesn't push us out of the calendar.
    if start < shift:
        raise NoFurtherDataError(
            msg=(
                "Pipeline Query requested data from {shift}"
                " days before {query_start}, but first known date is only "
                "{start} days earlier."
            ).format(shift=shift, query_start=start_date, start=start),
        )

    try:
        end = dates.get_loc(end_date)
    except KeyError:
        if end_date > dates[-1]:
            raise NoFurtherDataError(
                msg=(
                    "Pipeline Query requesting data up to {query_end}, "
                    "but last known date is {calendar_end}"
                ).format(
                    query_end=end_date,
                    calendar_end=dates[-1],
                )
            )
        else:
            raise ValueError("Query end %s not in calendar" % end_date)
    return dates[start - shift], dates[end - shift]
