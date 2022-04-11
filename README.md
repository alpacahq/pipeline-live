# ⚠️ This is software is very outdated and is not recommended for use in new setups ⚠️

We will keep this project up and with the documentation for the parts that remain
for those users who are still using this, but we suggest migrating to another tool
until we perform a major refactoring of this project to bring it up to speed. If this
is something you'd like to see please reach out to us to let us know!

The docs below still talk about zipline and Quantopian however Quantopian has since
gone out of business and the below hasn't yet been updated to reflect this.

If you're looking for another modern alternative to zipline, we recommend checking
out [zipline-reloaded](https://github.com/stefan-jansen/zipline-reloaded) in the meantime
while we review committing to a major refactor of this project.

## Zipline Pipeline Extension for Live Trading
`pipeline-live` is an extension for zipline pipeline independently usable
for live trading, outside of zipline. While zipline is a great backtesting
library, the default Pipeline API requires complicated setup for data bundle,
which is often challenging to average users. Quantopian's proprietary data
sources such as Morningstar is also not available to many. This library is
to address this issue by using online API data sources and simplify the interface
for live trading usage.
The interface complies the original zipline/pipeline for the most part.  For more
details about the Pipeline API, please see
[Quantopian's tutorial](https://www.quantopian.com/tutorials/pipeline) and
[zipline document](https://www.zipline.io/).

If you are looking to use this library for your Quantopian algorithm,
check out the [migration document](./migration.md).

## Data Sources
This library predominantly relies on the [Alpaca Data API](https://docs.alpaca.markets/api-documentation/api-v2/market-data/) for daily
price data. [IEX Cloud](https://iexcloud.io/docs/api/) data is also supported, though if too much
data is requested, it stops being free. (See the note in the IEX section below.)


## Install

`pipeline-live` is a PyPI module and you can install it using `pip` command.

```sh
$ pip install pipeline-live
```

This module is tested and expected to work with python 3.6 and later

## Example
Here is a simple pipeline example.
Please make sure to first set your API keys to these environment variables:

using python
```py
import os
os.environ["APCA_API_KEY_ID"] = <ALPACA_API_KEY>
os.environ["APCA_API_SECRET_KEY"] = <ALPACA_SECRET_KEY>
# if you use the paper endpoint:
os.environ["APCA_API_BASE_URL"] = "https://paper-api.alpaca.markets"
```

(or do it with bash if you prefer)

```py
from pipeline_live.engine import LivePipelineEngine
from pipeline_live.data.sources.alpaca import list_symbols
from pipeline_live.data.alpaca.pricing import USEquityPricing
from pipeline_live.data.alpaca.factors import AverageDollarVolume
from zipline.pipeline import Pipeline

eng = LivePipelineEngine(list_symbols)
top5 = AverageDollarVolume(window_length=20).top(5)
pipe = Pipeline({
    'close': USEquityPricing.close.latest,
}, screen=top5)

df = eng.run_pipeline(pipe)

'''
        close
AAPL   215.49
AMZN  1902.90
FB     172.90
QQQ    180.80
SPY    285.79
'''
```

## Data Cache
Since most of the data does not change during the day, the data access layer
caches the dataset on disk.  In case you need to purge the cache, the cache
data is located in `$ZIPLINE_ROOT/data/daily_cache`.

## Pipeline API

### pipeline_live.engine.LivePipelineEngine
This class provides the similar interface to `zipline.pipeline.engine.SimplePipelineEngine`.
The main difference is its `run_pipeline` does not require the start and end dates as parameters,
and returns a DataFrame with the data for the current date (US/Eastern time).
Its constructor accepts `list_symbol` function that is supposed to return the full set of
symbols as a string list, which is used as the maximum universe inside the engine.

## Alpaca Data API
The [Alpaca Data API](https://docs.alpaca.markets/api-documentation/api-v2/market-data/) is currently the least-limited source of pricing data
supported by pipeline-live. In order to use the Alpaca Data API, you'll need to
register for an Alpaca account [here](https://app.alpaca.markets/signup) and generate API key information with
the dashboard. Once you have your keys generated, you need to store them in
the following environment variables:

```
APCA_API_BASE_URL
APCA_API_KEY_ID
APCA_API_SECRET_KEY
```

### pipeline_live.data.alpaca.pricing.USEquityPricing
This class provides the basic price information retrieved from
[Alpaca Data API](https://docs.alpaca.markets/api-documentation/api-v2/market-data/bars/).

## Where Did the Polygon integration go?
Alpaca used to offer an integration with polygon, however with the removal of
that integration from the Alpaca api we removed the polygon integration here as well.

## IEX Data Source API
To use IEX-source data, you need to sign up for an IEX Cloud account and save
your IEX token as an environment variable called `IEX_TOKEN`.

IMPORTANT NOTE: IEX data is now limited for free accounts. In order to
avoid using more messages than you are allotted each month, please
be sure that you are not using IEX-sourced factors too frequently
or on too many securities. For more information about how many messages
each method will cost, please refer to [this part](https://iexcloud.io/docs/api/#data-weighting) of the IEX Cloud documentation.

### pipeline_live.data.iex.pricing.USEquityPricing
This class provides the basic price information retrieved from
[IEX Chart API](https://iextrading.com/developer/docs/#chart).

### pipeline_live.data.iex.fundamentals.IEXCompany
This provides the DataSet interface using
[IEX Company API](https://iextrading.com/developer/docs/#company).

### pipeline_live.data.iex.fundamentals.IEXKeyStats
This provides the DataSet interface using
[IEX Key Stats API](https://iextrading.com/developer/docs/#key-stats).

### pipeline_live.data.iex.factors
It is important to note that the original builtin factors from zipline does
not work here as is, since some of them rely on zipline's USEquityPricing class.
This package provides the same set of zipline's builtin factor classes using
`pipeline_live.data.iex.pricing.USEquityPricing` class. For the complete
list of builtin factors, please refer [zipline document](https://www.zipline.io/appendix.html#built-in-factors)

### pipeline_live.data.iex.classifiers.Sector()
A shortcut for `IEXCompany.sector.latest`

### pipeline_live.data.iex.classifiers.Industry()
A shortcut for `IEXCompany.industry.latest`
