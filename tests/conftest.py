import pytest
import tempfile
from unittest.mock import patch

from pipeline_live.data.sources import polygon as sources_polygon
from pipeline_live.data.sources import iex as sources_iex


@pytest.fixture
def tradeapi():
    with patch.object(sources_polygon, 'tradeapi') as tradeapi:
        yield tradeapi


@pytest.fixture
def iexfinance():
    with patch.object(sources_iex, 'iexfinance') as iexfinance:
        yield iexfinance


@pytest.fixture
def data_path():
    with patch('zipline.utils.paths.data_path') as data_path:
        with tempfile.TemporaryDirectory() as t:
            data_path.return_value = t
            yield data_path
