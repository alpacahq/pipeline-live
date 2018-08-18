import numpy as np
from zipline.utils.numpy_utils import (
    object_dtype, datetime64D_dtype, float64_dtype,
)
from .dataset import Column, DataSet


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

    exchange = Column(object_dtype)
    name = Column(object_dtype)
    symbol = Column(object_dtype)
    listdate = Column(
        datetime64D_dtype,
        missing_value=np.datetime64('1970-01-01'))
    cik = Column(object_dtype)
    bloomberg = Column(object_dtype)
    figi = Column(object_dtype)
    lei = Column(object_dtype)
    sic = Column(float64_dtype, missing_value=np.nan)
    country = Column(object_dtype)
    industry = Column(object_dtype)
    sector = Column(object_dtype)
    marketcap = Column(float64_dtype, missing_value=np.nan)
    employees = Column(float64_dtype, missing_value=np.nan)
    phone = Column(object_dtype)
    ceo = Column(object_dtype)
    tags = Column(object_dtype)
