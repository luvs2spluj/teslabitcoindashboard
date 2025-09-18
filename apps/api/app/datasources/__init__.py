"""
Data source adapters for external APIs.
"""

from .base import DataSource
from .stooq import StooqDataSource
from .fred import FREDDataSource
from .bitcoin_data import BitcoinDataSource
from .bgeometrics import BGeometricsDataSource
from .ycharts import YChartsDataSource

__all__ = [
    "DataSource",
    "StooqDataSource", 
    "FREDDataSource",
    "BitcoinDataSource",
    "BGeometricsDataSource",
    "YChartsDataSource"
]
