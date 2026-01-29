"""Data collection package"""
from .collectors.base_collector import BaseCollector, MarketData
from .collectors.yahoo_finance_collector import YahooFinanceCollector
from .collectors.fred_collector import FREDCollector

__all__ = [
    'BaseCollector',
    'MarketData',
    'YahooFinanceCollector',
    'FREDCollector'
]
