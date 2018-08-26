from .fundamentals import IEXCompany


def Sector():
    return IEXCompany.sector.latest


def Industry():
    return IEXCompany.industry.latest
