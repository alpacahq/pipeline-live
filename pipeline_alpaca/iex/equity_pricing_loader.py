# Copyright 2015 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from numpy import (
    iinfo,
    uint32,
)

import concurrent.futures
import numpy as np

import iexfinance
import pandas as pd
from zipline.data.us_equity_pricing import (
    BcolzDailyBarReader,
    SQLiteAdjustmentReader,
)
from zipline.lib.adjusted_array import AdjustedArray
from zipline.errors import NoFurtherDataError
from zipline.utils.calendars import get_calendar

from .base import PipelineLoader

UINT32_MAX = iinfo(uint32).max


def get_stockprices(symbols, chart_range='1y'):
    '''Get stock data (key stats and previous) from IEX.
    Just deal with IEX's 99 stocks limit per request.
    '''

    def get_chart(symbols):
        charts = iexfinance.Stock(symbols).get_chart(range=chart_range)
        result = {}
        for symbol, obj in charts.items():
            df = pd.DataFrame(
                obj,
                columns=('date', 'open', 'high', 'low', 'close', 'volume'),
            ).set_index('date')
            df.index = pd.to_datetime(df.index, utc=True)
            result[symbol] = df
        return result

    result = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        tasks = []
        partlen = 99
        for i in range(0, len(symbols), partlen):
            part = symbols[i:i + partlen]
            task = executor.submit(get_chart, part)
            tasks.append(task)

        total_count = len(symbols)
        report_percent = 10
        processed = 0
        for task in concurrent.futures.as_completed(tasks):
            symbol_charts = task.result()
            result.update(symbol_charts)
            processed += len(symbol_charts)
            percent = processed / total_count * 100
            if percent >= report_percent:
                print('{:.2f}% completed'.format(percent))
                report_percent = (percent + 10.0) // 10 * 10

    return result


class USEquityPricingLoader(PipelineLoader):
    """
    PipelineLoader for US Equity Pricing data

    Delegates loading of baselines and adjustments.
    """

    def __init__(self, asset_finder):
        self._asset_finder = asset_finder
        cal = get_calendar('NYSE')

        self._all_sessions = cal.all_sessions

    def load_adjusted_array(self, columns, dates, assets, mask):
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

        iex_symbols = [
            symbol['symbol'] for symbol in iexfinance.get_available_symbols()
        ]
        asset_finder = self._asset_finder
        asset_symbols = [
            a.symbol for a in asset_finder.retrieve_all(assets)
        ]
        symbols = list(set(iex_symbols) & set(asset_symbols))
        print('len(symbols) = {}'.format(len(symbols)))
        # TODO: dynamic "range"
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
        print('chart_range={}'.format(chart_range))
        prices = get_stockprices(symbols, chart_range=chart_range)

        dfs = []
        for symbol in asset_symbols:
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
                mask,
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
