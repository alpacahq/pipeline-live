from zipline.pipeline.data.dataset import Column, DataSet
from zipline.utils.numpy_utils import float64_dtype

from .pricing_loader import USEquityPricingLoader


# In order to use it as a cache key, we have to make it singleton
_loader = USEquityPricingLoader()


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
        return _loader
