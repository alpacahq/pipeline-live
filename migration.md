# Migrate your Pipeline from Quantopian
pipeline-live helps you run your algorithm outside of the Quantopian.
Although this project is an independent effort to provide the Pipeline
API using public/private data, this document is to describe the common
practices around how to migrate your pipeline code from the Quantopian
environment.

Along with these practices, you can migrate your Algorithm API from Quantopian
using [pylivetrader](https://github.com/alpacahq/pylivetrader), and
pylivetrader can run the pipeline object from this package.

## USEquityPricing
The most important class to think about first is the USEquityPricing class
and it is well covered by
`pipeline_live.data.alpaca.pricing.USEquityPricing` class.
This class gets the market-wide daily price data (OHLCV) up to the
previous day from [Alpaca data API](https://docs.alpaca.markets/api-documentation/api-v2/market-data/bars/).

## Factors
In order to use many of the builtin factors with this price data loader,
you need to use `pipeline_live.data.alpaca.factors` package which has
all the builtin factor classes ported from zipline. Use of the Alpaca data API
requires an Alpaca account, which you can sign up for [here](https://app.alpaca.markets/signup).

Once you have an Alpaca account, you will need to store your account info
from their dashboard as environment variables. You can find information about
how to do so on [this documentation page](https://docs.alpaca.markets/api-documentation/how-to/).

To use the Alpaca factors, import them from `pipeline_live.data.alpaca.factors`.
For example, if you have these lines on Quantopian,

```py
from quantopian.pipeline.factors import (
    AverageDollarVolume, SimpleMovingAverage,
)
from quantopian.pipeline.data.builtin import USEquityPricing
```

you can rewrite it to something like this.

```py
from pipeline_live.data.alpaca.factors import (
    AverageDollarVolume, SimpleMovingAverage,
)
from pipeline_live.data.alpaca.pricing import USEquityPricing
```

Of course, the builtin factor classes in the original zipline are mostly
pure functions and take inputs explicitly, so if you give the correct
ones, they also work with this `USEquityPricing`.

```py
from zipline.pipeline.factors import AverageDollarVolume
from pipeline_live.data.alpaca.pricing import USEquityPricing

dollar_volume = AverageDollarVolume(
    inputs=[USEquityPricing.close, USEquityPricing.volume],
    window_length=20,
)
```

The only difference in the factor classes in `pipeline_live.data.alpaca.factors`
is that some of the classes have Alpaca's USEquityPricing as the default
inputs, so you don't need to explicitly specify it.

## Fundamentals
The Quantopian platform allows you to retrieve various proprietary data
sources through pipeline, including Morningstar fundamentals. While the
intention of this pipline-live library is to add more such proprietary
data sources, the alternative at the moment is IEX. There are two
main dataset classes are builtin in this library, `IEXCompany` and
`IEXKeyStats`. Those both belong to the `pipeline_live.data.iex.fundamentals`
package.

Please note that, in order to use the IEX API data, you will need to sign up
for an IEX Cloud account [here](https://iexcloud.io/cloud-login#/register/) and set your IEX Cloud token in the
`IEX_TOKEN` environment variable. IEX limits your API messages per month. In
order to avoid running over your message quota, please make sure that you
filter your stock universe as much as possible before using IEX API data.
If you wish to use IEX data to frequently filter a larger set of symbols, you
may need to upgrade your IEX Cloud account.

### IEXCompany
This dataset class maps the basic stock information from the
[Company API](https://iextrading.com/developer/docs/#company).
If your Quantopian algorithm is using symbol filtering from Morningstar,
you can reference the `symbol` field from this class.

```py
    # not_wi = ~morningstar.share_class_reference.symbol.latest.endswith('.WI')
    not_wi = ~IEXCompany.symbol.latest.endswith('.WI')
```

Also you can filter out Limited Partners using the `companyName` field.
```py
    # not_lp_name = ~morningstar.company_reference.standard_name.latest.matches('.* L[. ]?P.?$')
    not_lp_name = ~IEXCompany.companyName.latest.matches('.* L[. ]?P.?$')
```

The `sector` and `industry` fields are good to use for classifiers as well.

### IEXKeyStats
This dataset class maps the detailed statistics for the stock from
the [Key Stats API](https://iextrading.com/developer/docs/#key-stats).
The most common use case of this class is the `marketcap` field.

```py
    # market_cap = morningstar.valuation.market_cap >= 100e6
    market_cap = IEXKeyStats.marketcap.latest >= 100e6
```

Note, all the fields under IEXKeyStats fields needs `.latest` access
to use the value, unlike the Quantopian's morningstar package.

While IEX's API provides three last quarter financial reports, currently
pipeline-live does not provide historical view of this data through
the pipeline interface.

## Primary Share
Many algorithms developed in the Quantopian platform uses the `IsPrimaryShare`
function to perform base filter. While this value is unique to Morningstar
and IEX does not provide this value, something similar can be filtered, at
least the following criteria.

- Has valid revenue value (excluding funds, non-corporate type of shares)
- Has the biggest marketcap/dollar volume within the same company name (choosing one of the shares between pairs such as GOOG/GOOGL, BRK.A/BRK.B)

The `pipeline_live.data.iex` package currently does not provide this
logic as a function, until we confirm the result is good enough for real
uses, but you can built your own function which implements something similar.

Within this library, you have access to Polygon fundamentals, which have
different set of stock info/details. If you have API key for Polygon,
you may want to look at the `pipeline_live.data.polygon.filters.IsPrimaryShareEmulation` class for
the replacement, too.

## ADR
While IEX Company API has a field called `issueType` and the API document
indicates this field can use for ADR check, this value has been
not very accurate, as of writing. If you have access to Polygon, you can
check out `PolygonCompany.country` field to filter out non-US companies.