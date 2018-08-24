import numpy as np

from zipline.utils.numpy_utils import (
    object_dtype, datetime64D_dtype, float64_dtype,
)
from zipline.pipeline.data.dataset import Column, DataSet

from .fundamentals_loader import IEXKeyStatsLoader, IEXCompanyLoader


class IEXKeyStats(DataSet):

    '''
  "companyName": "Apple Inc.",
  "marketcap": 760334287200,
  "beta": 1.295227,
  "week52high": 156.65,
  "week52low": 93.63,
  "week52change": 58.801903,
  "shortInterest": 55544287,
  "shortDate": "2017-06-15",
  "dividendRate": 2.52,
  "dividendYield": 1.7280395,
  "exDividendDate": "2017-05-11 00:00:00.0",
  "latestEPS": 8.29,
  "latestEPSDate": "2016-09-30",
  "sharesOutstanding": 5213840000,
  "float": 5203997571, "returnOnEquity": 0.08772939519857577,
  "consensusEPS": 3.22,
  "numberOfEstimates": 15,
  "symbol": "AAPL",
  "EBITDA": 73828000000,
  "revenue": 220457000000,
  "grossProfit": 84686000000,
  "cash": 256464000000,
  "debt": 358038000000,
  "ttmEPS": 8.55,
  "revenuePerShare": 42.2830389885382,
  "revenuePerEmployee": 1900491.3793103448, "peRatioHigh": 25.5,
  "peRatioLow": 8.7,
  "EPSSurpriseDollar": null,
  "EPSSurprisePercent": 3.9604,
  "returnOnAssets": 14.15,
  "returnOnCapital": null,
  "profitMargin": 20.73,
  "priceToSales": 3.6668503,
  "priceToBook": 6.19,
  "day200MovingAvg": 140.60541,
  "day50MovingAvg": 156.49678,
  "institutionPercent": 32.1,
  "insiderPercent": null,
  "shortRatio": 1.6915414,
  "year5ChangePercent": 0.5902546932200027,
  "year2ChangePercent": 0.3777449874142869,
  "year1ChangePercent": 0.39751716851558366,
  "ytdChangePercent": 0.36659492036160124,
  "month6ChangePercent": 0.12208398133748043,
  "month3ChangePercent": 0.08466584665846649,
  "month1ChangePercent": 0.009668596145283263,
  "day5ChangePercent": -0.005762605699968781
    '''

    companyName = Column(object_dtype)
    marketcap = Column(float64_dtype, missing_value=np.nan)
    beta = Column(float64_dtype, missing_value=np.nan)
    week52high = Column(float64_dtype, missing_value=np.nan)
    week52low = Column(float64_dtype, missing_value=np.nan)
    week52change = Column(float64_dtype, missing_value=np.nan)
    shortInterest = Column(float64_dtype, missing_value=np.nan)
    shortDate = Column(
        datetime64D_dtype,
        missing_value=np.datetime64('1970-01-01'))
    dividendRate = Column(float64_dtype, missing_value=np.nan)
    dividendYield = Column(float64_dtype, missing_value=np.nan)
    exDividendDate = Column(
        datetime64D_dtype,
        missing_value=np.datetime64('1970-01-01'))
    latestEPS = Column(float64_dtype, missing_value=np.nan)
    latestEPSDate = Column(
        datetime64D_dtype,
        missing_value=np.datetime64('1970-01-01'))
    sharesOutstanding = Column(float64_dtype, missing_value=np.nan)
    float = Column(float64_dtype, missing_value=np.nan)
    returnOnEquity = Column(float64_dtype, missing_value=np.nan)
    consensusEPS = Column(float64_dtype, missing_value=np.nan)
    numberOfEstimates = Column(float64_dtype, missing_value=np.nan)
    symbol = Column(object_dtype)
    EBITDA = Column(float64_dtype, missing_value=np.nan)
    revenue = Column(float64_dtype, missing_value=np.nan)
    grossProfit = Column(float64_dtype, missing_value=np.nan)
    cash = Column(float64_dtype, missing_value=np.nan)
    debt = Column(float64_dtype, missing_value=np.nan)
    ttmEPS = Column(float64_dtype, missing_value=np.nan)
    revenuePerShare = Column(float64_dtype, missing_value=np.nan)
    revenuePerEmployee = Column(float64_dtype, missing_value=np.nan)
    peRatioHigh = Column(float64_dtype, missing_value=np.nan)
    peRatioLow = Column(float64_dtype, missing_value=np.nan)
    EPSSurpriseDollar = Column(float64_dtype, missing_value=np.nan)
    EPSSurprisePercent = Column(float64_dtype, missing_value=np.nan)
    returnOnAssets = Column(float64_dtype, missing_value=np.nan)
    returnOnCapital = Column(float64_dtype, missing_value=np.nan)
    profitMargin = Column(float64_dtype, missing_value=np.nan)
    priceToSales = Column(float64_dtype, missing_value=np.nan)
    priceToBook = Column(float64_dtype, missing_value=np.nan)
    day200MovingAvg = Column(float64_dtype, missing_value=np.nan)
    day50MovingAvg = Column(float64_dtype, missing_value=np.nan)
    institutionPercent = Column(float64_dtype, missing_value=np.nan)
    insiderPercent = Column(float64_dtype, missing_value=np.nan)
    shortRatio = Column(float64_dtype, missing_value=np.nan)
    year5ChangePercent = Column(float64_dtype, missing_value=np.nan)
    year2ChangePercent = Column(float64_dtype, missing_value=np.nan)
    year1ChangePercent = Column(float64_dtype, missing_value=np.nan)
    ytdChangePercent = Column(float64_dtype, missing_value=np.nan)
    month6ChangePercent = Column(float64_dtype, missing_value=np.nan)
    month3ChangePercent = Column(float64_dtype, missing_value=np.nan)
    month1ChangePercent = Column(float64_dtype, missing_value=np.nan)
    day5ChangePercent = Column(float64_dtype, missing_value=np.nan)

    _loader = IEXKeyStatsLoader()

    @classmethod
    def get_loader(cls):
        return cls._loader


class IEXCompany(DataSet):

    symbol = Column(object_dtype, missing_value='')
    companyName = Column(object_dtype, missing_value='')
    exchange = Column(object_dtype, missing_value='')
    industry = Column(object_dtype, missing_value='')
    website = Column(object_dtype, missing_value='')
    description = Column(object_dtype, missing_value='')
    CEO = Column(object_dtype, missing_value='')
    issueType = Column(object_dtype, missing_value='')
    sector = Column(object_dtype, missing_value='')
    # tags = Column(object_dtype, missing_value='')

    _loader = IEXCompanyLoader()

    @classmethod
    def get_loader(cls):
        return cls._loader
