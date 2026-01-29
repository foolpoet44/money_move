"""
Base data collector abstract class
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class MarketData:
    """Market data structure"""
    symbol: str
    timestamp: datetime
    price: float
    volume: Optional[int] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    open: Optional[float] = None
    close: Optional[float] = None
    metadata: Optional[Dict] = None


class BaseCollector(ABC):
    """Abstract base class for data collectors"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.name = self.__class__.__name__
        logger.info(f"Initialized {self.name}")
    
    @abstractmethod
    async def collect(self, symbols: List[str]) -> List[MarketData]:
        """
        Collect data for given symbols
        
        Args:
            symbols: List of symbols to collect data for
            
        Returns:
            List of MarketData objects
        """
        pass
    
    @abstractmethod
    async def validate_connection(self) -> bool:
        """
        Validate connection to data source
        
        Returns:
            True if connection is valid, False otherwise
        """
        pass
    
    def _handle_error(self, error: Exception, symbol: str) -> None:
        """
        Handle collection errors
        
        Args:
            error: Exception that occurred
            symbol: Symbol that caused the error
        """
        logger.error(f"{self.name} error for {symbol}: {str(error)}")
    
    def _normalize_symbol(self, symbol: str) -> str:
        """
        Normalize symbol format for the data source
        
        Args:
            symbol: Raw symbol
            
        Returns:
            Normalized symbol
        """
        return symbol.upper().strip()
