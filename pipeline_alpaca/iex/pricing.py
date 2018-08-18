from zipline.pipeline.data.dataset import Column, DataSet
from zipline.utils.numpy_utils import float64_dtype

from .pricing_loader import USEquityPricingLoader


class USEquityPricing(DataSet):
    """
    Dataset representing daily trading prices and volumes.
    """
    open = Column(float64_dtype)
    high = Column(float64_dtype)
    low = Column(float64_dtype)
    close = Column(float64_dtype)
    volume = Column(float64_dtype)

    @staticmethod
    def get_loader():
        return USEquityPricingLoader()