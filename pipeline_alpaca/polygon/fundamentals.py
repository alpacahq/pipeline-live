import numpy as np
from zipline.utils.numpy_utils import (
    object_dtype, datetime64D_dtype, float64_dtype,
)
from zipline.pipeline.data.dataset import Column, DataSet

from .fundamentals_loader import PolygonCompanyLoader


class PolygonCompany(DataSet):

    '''
    "logo": "https://s3.polygon.io/logos/aapl/logo.png",
    "exchange": "Nasdaq Global Select",
    "name": "Apple Inc.",
    "symbol": "AAPL",
    "listdate": "2018-08-15",
    "cik": "0000320193",
    "bloomberg": "EQ0010169500001000",
    "figi": "string",
    "lei": "HWUPKR0MPOU8FGXBT394",
    "sic": 3571,
    "country": "us",
    "industry": "Computer Hardware",
    "sector": "Technology",
    "marketcap": 815604985500,
    "employees": 116000,
    "phone": "(408) 996-1010",
    "ceo": "Tim Cook",
    "url": "http://www.apple.com",
    "description": "Apple Inc. designs, manufactures, and markets mobile communication and media devices, personal computers, and portable digital music players to consumers...\n",
    '''  # noqa

    exchange = Column(object_dtype, missing_value='')
    name = Column(object_dtype, missing_value='')
    symbol = Column(object_dtype, missing_value='')
    listdate = Column(
        datetime64D_dtype,
        missing_value=np.datetime64('1970-01-01'))
    cik = Column(object_dtype, missing_value='')
    bloomberg = Column(object_dtype, missing_value='')
    figi = Column(object_dtype, missing_value='')
    lei = Column(object_dtype, missing_value='')
    sic = Column(float64_dtype, missing_value=np.nan)
    country = Column(object_dtype, missing_value='')
    industry = Column(object_dtype, missing_value='')
    sector = Column(object_dtype, missing_value='')
    marketcap = Column(float64_dtype, missing_value=np.nan)
    employees = Column(float64_dtype, missing_value=np.nan)
    phone = Column(object_dtype, missing_value='')
    ceo = Column(object_dtype, missing_value='')
    tags = Column(object_dtype, missing_value='')

    _loader = PolygonCompanyLoader()

    @classmethod
    def get_loader(cls):
        return cls._loader
