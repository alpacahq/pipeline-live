import numpy as np

from zipline.utils.numpy_utils import (
    object_dtype, datetime64ns_dtype, datetime64D_dtype, float64_dtype,
)
from zipline.pipeline.data.dataset import Column, DataSet

from .fundamentals_loader import (
    IEXKeyStatsLoader,
    IEXCompanyLoader,
    IEXFinancialsLoader,
    IEXEarningsLoader,
)



class IEXEarnings(DataSet):

    '''
        "actualEPS": 2.46,
        "consensusEPS": 2.36,
        "announceTime": "AMC",
        "numberOfEstimates": 34,
        "EPSSurpriseDollar": 0.1,
        "EPSReportDate": "2019-04-30",
        "fiscalPeriod": "Q1 2019",
        "fiscalEndDate": "2019-03-31",
        "yearAgo": 2.73,
        "yearAgoChangePercent": -0.0989
    '''

    announceTime = Column(object_dtype, missing_value='')
    fiscalPeriod = Column(object_dtype, missing_value='')
    EPSReportDate = Column(
        datetime64ns_dtype,
        missing_value=np.datetime64('1970-01-01'))
    fiscalEndDate = Column(
        datetime64ns_dtype,
        missing_value=np.datetime64('1970-01-01'))
    actualEPS = Column(float64_dtype, missing_value=np.nan)
    consensusEPS = Column(float64_dtype, missing_value=np.nan)
    numberOfEstimates = Column(float64_dtype, missing_value=np.nan)
    EPSSurpriseDollar = Column(float64_dtype, missing_value=np.nan)
    yearAgo = Column(float64_dtype, missing_value=np.nan)
    yearAgoChangePercent = Column(float64_dtype, missing_value=np.nan)

    _loader = IEXEarningsLoader()

    @classmethod
    def get_loader(cls):
        return cls._loader

class IEXFinancials(DataSet):

    '''
        "reportDate": "2019-03-31",
        "grossProfit": 21648000000,
        "costOfRevenue": 36270000000,
        "operatingRevenue": 57918000000,
        "totalRevenue": 57918000000,
        "operatingIncome": 13242000000,
        "netIncome": 11561000000,
        "researchAndDevelopment": 3948000000,
        "operatingExpense": 44676000000,
        "currentAssets": 123346000000,
        "totalAssets": 341998000000,
        "totalLiabilities": 236138000000,
        "currentCash": 38329000000,
        "currentDebt": 22429000000,
        "shortTermDebt": 22429000000,
        "longTermDebt": 90201000000,
        "totalCash": 80433000000,
        "totalDebt": 112630000000,
        "shareholderEquity": 105860000000,
        "cashChange": -4954000000,
        "cashFlow": 11155000000
    '''

    reportDate = Column(float64_dtype, missing_value=np.nan)
    grossProfit = Column(float64_dtype, missing_value=np.nan)
    costOfRevenue = Column(float64_dtype, missing_value=np.nan)
    operatingRevenue = Column(float64_dtype, missing_value=np.nan)
    totalRevenue = Column(float64_dtype, missing_value=np.nan)
    operatingIncome = Column(float64_dtype, missing_value=np.nan)
    netIncome = Column(float64_dtype, missing_value=np.nan)
    researchAndDevelopment = Column(float64_dtype, missing_value=np.nan)
    operatingExpense = Column(float64_dtype, missing_value=np.nan)
    currentAssets = Column(float64_dtype, missing_value=np.nan)
    totalAssets = Column(float64_dtype, missing_value=np.nan)
    totalLiabilities = Column(float64_dtype, missing_value=np.nan)
    currentCash = Column(float64_dtype, missing_value=np.nan)
    currentDebt = Column(float64_dtype, missing_value=np.nan)
    shortTermDebt = Column(float64_dtype, missing_value=np.nan)
    longTermDebt = Column(float64_dtype, missing_value=np.nan)
    totalCash = Column(float64_dtype, missing_value=np.nan)
    totalDebt = Column(float64_dtype, missing_value=np.nan)
    shareholderEquity = Column(float64_dtype, missing_value=np.nan)
    cashChange = Column(float64_dtype, missing_value=np.nan)
    cashFlow = Column(float64_dtype, missing_value=np.nan)

    _loader = IEXFinancialsLoader()

    @classmethod
    def get_loader(cls):
        return cls._loader


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
        datetime64ns_dtype,
        missing_value=np.datetime64('1970-01-01'))
    dividendRate = Column(float64_dtype, missing_value=np.nan)
    dividendYield = Column(float64_dtype, missing_value=np.nan)
    exDividendDate = Column(
        datetime64ns_dtype,
        missing_value=np.datetime64('1970-01-01'))
    latestEPS = Column(float64_dtype, missing_value=np.nan)
    latestEPSDate = Column(
        datetime64ns_dtype,
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
    peRatio = Column(float64_dtype, missing_value=np.nan)
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
