"""
Yahoo Finance data collector
"""
import yfinance as yf
from typing import List, Dict
from datetime import datetime
import asyncio
from .base_collector import BaseCollector, MarketData
import logging

logger = logging.getLogger(__name__)


class YahooFinanceCollector(BaseCollector):
    """Collector for Yahoo Finance data"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.rate_limit_delay = config.get('rate_limit_delay', 0.5)
    
    async def collect(self, symbols: List[str]) -> List[MarketData]:
        """
        Collect real-time data from Yahoo Finance
        
        Args:
            symbols: List of ticker symbols
            
        Returns:
            List of MarketData objects
        """
        results = []
        
        for symbol in symbols:
            try:
                normalized_symbol = self._normalize_symbol(symbol)
                data = await self._fetch_ticker_data(normalized_symbol)
                
                if data:
                    results.append(data)
                
                # Rate limiting
                await asyncio.sleep(self.rate_limit_delay)
                
            except Exception as e:
                self._handle_error(e, symbol)
        
        logger.info(f"Collected {len(results)}/{len(symbols)} symbols from Yahoo Finance")
        return results
    
    async def _fetch_ticker_data(self, symbol: str) -> MarketData:
        """
        Fetch data for a single ticker
        
        Args:
            symbol: Ticker symbol
            
        Returns:
            MarketData object
        """
        # Run in executor to avoid blocking
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, yf.Ticker, symbol)
        
        # Get current data
        info = await loop.run_in_executor(None, lambda: ticker.info)
        hist = await loop.run_in_executor(
            None, 
            lambda: ticker.history(period="1d", interval="1m")
        )
        
        if hist.empty:
            logger.warning(f"No data available for {symbol}")
            return None
        
        latest = hist.iloc[-1]
        
        return MarketData(
            symbol=symbol,
            timestamp=datetime.now(),
            price=float(latest['Close']),
            volume=int(latest['Volume']) if 'Volume' in latest else None,
            high=float(latest['High']),
            low=float(latest['Low']),
            open=float(latest['Open']),
            close=float(latest['Close']),
            metadata={
                'source': 'yahoo_finance',
                'market_cap': info.get('marketCap'),
                'currency': info.get('currency', 'USD')
            }
        )
    
    async def validate_connection(self) -> bool:
        """
        Validate Yahoo Finance connection
        
        Returns:
            True if connection is valid
        """
        try:
            test_data = await self.collect(['SPY'])
            return len(test_data) > 0
        except Exception as e:
            logger.error(f"Yahoo Finance connection validation failed: {e}")
            return False
    
    async def get_etf_flows(self, symbol: str, period: str = "5d") -> Dict:
        """
        Get ETF flow data (volume analysis)
        
        Args:
            symbol: ETF symbol
            period: Historical period
            
        Returns:
            Flow analysis data
        """
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, yf.Ticker, symbol)
        hist = await loop.run_in_executor(
            None,
            lambda: ticker.history(period=period)
        )
        
        if hist.empty:
            return None
        
        # Calculate flow metrics
        avg_volume = hist['Volume'].mean()
        latest_volume = hist['Volume'].iloc[-1]
        volume_ratio = latest_volume / avg_volume if avg_volume > 0 else 0
        
        # Price change
        price_change = (hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0] * 100
        
        return {
            'symbol': symbol,
            'avg_volume': float(avg_volume),
            'latest_volume': float(latest_volume),
            'volume_ratio': float(volume_ratio),
            'price_change_pct': float(price_change),
            'net_flow_indicator': 'inflow' if volume_ratio > 1.2 and price_change > 0 else 'outflow' if volume_ratio > 1.2 and price_change < 0 else 'neutral'
        }
