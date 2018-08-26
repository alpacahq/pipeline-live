# Zipline Pipeline Extension for Live Trading
`pipeline-alpaca` is an extension for zipline pipeline independently usable
for live trading, outside of zipline. While zipline is a great backtesting
library, the default Pipeline API requires complicated setup for data bundle,
which is often challenging to average users. Quantopian's proprietary data
sources such as Morningstar is also not available to many. This library is
to address this issue by using online API data sources and simplify the interface
for live trading usage.
The interface complies the original zipline/pipeline for the most part.  For more
details about the Pipeline API, please refer the zipline document.

## Data Sources
This library premoninantly relies on the IEX public data API for daily
prices and fundamentals, but aims to connect to other data sources over
the time. Currently supported data sources include the following.

- Alpaca/Polygon

## Install

`pipeline-alpaca` is a PyPI module and you can install it using `pip` command.

```sh $ pip install pipeline-alpaca ```

This module is tested and expected to work with python 3.6 and later

## Example
Here is a simple pipeline example.

```py
from pipeline_alpaca.engine import LivePipelineEngine
from pipeline_alpaca.data.sources.iex import list_symbols
from pipeline_alpaca.data.iex.pricing import USEquityPricing
from pipeline_alpaca.data.iex.fundamentals import IEXKeyStats
from pipeline_alpaca.data.iex.factors import AverageDollarVolume

eng = LivePipelineEngine(list_symbols)
top5 = AverageDollarVolume(window_length=20).top(5)
pipe = Pipeline({
    'close': USEquityPricing.close.latest,
    'marketcap': IEXKeyStats.marketcap.latest,
}, screen=top5)

df = eng.run_pipeline(pipe)
```

## Key Classes and Functions

### pipeline_alpaca.engine.LivePipelineEngine
This class provides the similar interface to `zipline.pipeline.engine.SimplePipelineEngine`.
The main difference is its `run_pipeline` does not require the start and end dates as parameters, and returns a DataFrame with the data for the current date (US/Eastern time). Its constructor accepts `list_symbol` function that
is supposed to return the full set of symbols as a string list, which is
used as the maximum universe inside the engine.

### pipeline_alpaca.data.iex.pricing.USEquityPricing
This class provides the basic price information retrieved from IEX Chart API.

### pipeline_alpaca.data.iex.fundamentals.IEXCompany
This provides the DataSet interface using [IEX Company API](https://iextrading.com/developer/docs/#company).

### pipeline_alpaca.data.iex.fundamentals.IEXKeyStats
This provides the DataSet interface using [IEX Key Stats API](https://iextrading.com/developer/docs/#key-stats).

### pipeline_alpaca.data.iex.factors
It is important to note that the original builtin factors from zipline does
not work here as is, since some of them rely on zipline's USEquityPricing class.
This package provides the same set of zipline's builtin factor classes using
`pipeline_alpaca.data.iex.pricing.USEquityPricing` class. For the complete
list of builtin factors, please refer [zipline document](https://www.zipline.io/appendix.html#built-in-factors)

### pipeline_alpaca.data.iex.classifiers.Sector()
A shortcut for `IEXCompany.sector.latest`

### pipeline_alpaca.data.iex.classifiers.Industry()
A shortcut for `IEXCompany.industry.latest`